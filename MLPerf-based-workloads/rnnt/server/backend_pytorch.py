# Copyright (c) 2020, Cerebras Systems, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import array
import torch
import backend
from scipy.io import wavfile
import numpy as np
import toml
from tqdm import tqdm

from decoders import ScriptGreedyDecoder
from helpers import add_blank_label
from preprocessing import AudioPreprocessing
from model_separable_rnnt import RNNT

class BackendPytorchNative(backend.Backend):
    def __init__(self, use_gpu=False, mini_batch_size=1):
        super(BackendPytorchNative, self).__init__()
        self.sess = None
        self.model = None

        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = "cuda:0" if self.use_gpu else "cpu"

        if self.use_gpu:
            print("Using GPU")
        else:
            print("Using CPU")
    def version(self):
        return torch.__version__

    def name(self):
        return "pytorch-native-rnnt"

    def load(self, config_path, model_path):
        config = toml.load(config_path)
        self.dataset_vocab = config['labels']['labels']
        rnnt_vocab = add_blank_label(self.dataset_vocab)
        featurizer_config = config['input_eval']

        self.audio_preprocessor = AudioPreprocessing(**featurizer_config)
        self.audio_preprocessor = self.audio_preprocessor.eval().to(self.device)

        model = RNNT(
            feature_config=featurizer_config,
            rnnt=config['rnnt'],
            device=self.device,
            num_classes=len(rnnt_vocab)
        )
        def load_and_migrate_checkpoint(model_path, device):
            checkpoint = torch.load(model_path, map_location=device)
            migrated_state_dict = {}
            for key, value in checkpoint['state_dict'].items():
                key = key.replace("joint_net", "joint.net")
                migrated_state_dict[key] = value
            del migrated_state_dict["audio_preprocessor.featurizer.fb"]
            del migrated_state_dict["audio_preprocessor.featurizer.window"]
            return migrated_state_dict
        model.load_state_dict(load_and_migrate_checkpoint(model_path, self.device),
                              strict=True)
        self.greedy_decoder = ScriptGreedyDecoder(len(rnnt_vocab) - 1, model, self.device)
        self.greedy_decoder = self.greedy_decoder.eval().to(self.device)
        #print("model init done")

    def predict(self, raw_data):
        waveform = torch.tensor(raw_data, dtype=torch.float)
        assert waveform.ndim == 1
        waveform_length = np.array(waveform.shape[0], dtype=np.int64)
        waveform = np.expand_dims(waveform, 0)
        waveform_length = np.expand_dims(waveform_length, 0)
        with torch.no_grad():
            waveform = torch.from_numpy(waveform).to(self.device)
            waveform_length = torch.from_numpy(waveform_length).to(self.device)
            feature, feature_length = self.audio_preprocessor.forward((waveform, waveform_length))
            assert feature.ndim == 3
            assert feature_length.ndim == 1
            feature = feature.permute(2, 0, 1)

            _, _, transcript = self.greedy_decoder.forward(feature, feature_length)

        assert len(transcript) == 1
        response_array = array.array('q', transcript[0])
        ans = [self.dataset_vocab[idx] for idx in response_array]
        return ans 

if __name__ == "__main__":
    backend = BackendPytorchNative(use_gpu=True)
    backend.load(config_path = "configs/rnnt.toml", model_path = "rnnt.pt")
    sample_rate, raw_data = wavfile.read('en.wav')
    import time
    start = time.time()
    backend.predict(raw_data)
    print("elapsed time:", time.time()-start)
