"""
tensorflow backend (https://github.com/tensorflow/tensorflow)
"""

# pylint: disable=unused-argument,missing-docstring,useless-super-delegation

import tensorflow as tf
from tensorflow import dtypes
from tensorflow.python.tools.optimize_for_inference_lib import optimize_for_inference

import os
import backend

class BackendTensorflow(backend.Backend):
    def __init__(self):
        super(BackendTensorflow, self).__init__()

    def version(self):
        return tf.__version__ + "/" + tf.__git_version__

    def name(self):
        return "tensorflow"

    def image_format(self):
        # By default tensorflow uses NHWC (and the cpu implementation only does NHWC)
        return "NHWC"

    def load(self, model_path, inputs=None, outputs=None):
        # there is no input/output meta data i the graph so it need to come from config.
        if not inputs:
            raise ValueError("BackendTensorflow needs inputs")
        if not outputs:
            raise ValueError("BackendTensorflow needs outputs")
        self.outputs = outputs
        self.inputs = inputs

        infer_config = tf.compat.v1.ConfigProto()
        infer_config.intra_op_parallelism_threads = int(os.environ['TF_INTRA_OP_PARALLELISM_THREADS']) \
                if 'TF_INTRA_OP_PARALLELISM_THREADS' in os.environ else os.cpu_count()
        infer_config.inter_op_parallelism_threads = int(os.environ['TF_INTER_OP_PARALLELISM_THREADS']) \
                if 'TF_INTER_OP_PARALLELISM_THREADS' in os.environ else os.cpu_count()
        infer_config.use_per_session_threads = 1

        graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v1.gfile.FastGFile(model_path, "rb") as f:
            graph_def.ParseFromString(f.read())
            g = tf.compat.v1.import_graph_def(graph_def, name='')
        self.sess = tf.compat.v1.Session(graph=g, config=infer_config)
        return self

    def predict(self, feed):
        return self.sess.run(self.outputs, feed_dict=feed)
