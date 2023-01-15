import tensorflow as tf
import argparse
import os
from . import nmt
from . import train


def _update_flags(flags, test_name):
  """Update flags for basic training."""
  flags.num_train_steps = 100
  flags.steps_per_stats = 5
  flags.src = "en"
  flags.tgt = "de"
  flags.vocab_prefix = "nmt/data/vocab.bpe.32000"
  flags.infer_batch_size = 32
  flags.infer_file = "nmt/data/newstest2014.tok.bpe.32000.en"
  flags.hparams_path = "nmt/standard_hparams/wmt16_gnmt_4_layer.json"
  # Need train a model and save the model to `nmt/data/models`
  flags.out_dir = "nmt/data/models"
  flags.export_path = os.path.join("/models/gnmt/")
  flags.version_number = 1 
  flags.ckpt_path = None 


class TestExporter(tf.test.TestCase):

  def test_exporter(self):
    nmt_parser = argparse.ArgumentParser()
    nmt.add_arguments(nmt_parser)
    FLAGS, unparsed = nmt_parser.parse_known_args()

    _update_flags(FLAGS, "exporter_test")
    default_hparams = nmt.create_hparams(FLAGS)
    nmt.run_main(FLAGS, default_hparams, train.train, None)


if __name__ == "__main__":
  tf.test.main()
