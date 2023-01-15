#! /usr/bin/env python3
# coding=utf-8
# Copyright (c) 2021 NVIDIA CORPORATION. All rights reserved.
# Copyright 2021 The MLPerf Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from base import BASE_3DUNET_SUT

import tensorflow as tf
import numpy as np


class _3DUNET_TensorFlow_SimplifedSUT(BASE_3DUNET_SUT):
    """
    A class to represent SUT (System Under Test) for MLPerf.
    This inherits BASE_3DUNET_SUT and builds functionality for TensorFlow.

    Attributes
    ----------
    model_path: str or PosixPath object
        path to the model for TensorFlow
    model: object
        TensorFlow model instance that does inference
    output_name: str
        output tensor nameof the TensorFlow inference model instance

    Methods
    -------
    do_infer(input_tensor):
        Perform inference upon input_tensor with TensorFlow
    """

    def __init__(self, model_path):
        """
        Constructs all the necessary attributes for TensorFlow specific 3D UNet SUT

        Parameters
        ----------
            model_path: str or PosixPath object
                path to the model for TensorFlow
        """
        print("Loading TensorFlow model...")
        assert Path(model_path, "saved_model.pb").is_file(),\
            "Cannot find the model file {:}!".format(model_path)
        loaded_model = tf.saved_model.load(model_path)
        self.model = loaded_model.signatures["serving_default"]
        self.output_name = list(self.model.structured_outputs)[0]

    def do_infer(self, input_tensor):
        """
        Perform inference upon input_tensor with TensorFlow
        """
        return self.model(tf.constant(input_tensor))[self.output_name].numpy()

    def predict(self, query):
        return self.issue_queries(query)

def get_sut(model_path):
    """
    Redirect the call for instantiating SUT to TensorFlow specific SUT
    """
    return _3DUNET_TensorFlow_SimplifedSUT(model_path)

if __name__ == "__main__":
    sut = get_sut("/models/3dunet/3dunet_kits19_128x128x128.tf")
    query = np.array(np.load('/sample.pkl', allow_pickle=True))
    ans = sut.issue_queries(query)
    print(ans)
