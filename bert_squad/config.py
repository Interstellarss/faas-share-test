"""Flask configuration."""

INIT_CHECKPOINT = '/workspace/bert/checkpoints/bert_large_qa.pt'
BERT_MODEL = 'bert-large-uncased'
VOCAB_FILE = '/workspace/bert/data/download/google_pretrained_weights/uncased_L-24_H-1024_A-16/vocab.txt'
CONFIG_FILE = '/workspace/bert/bert_configs/large.json'
QUESTION = "What food does Harry like?"
CONTEXT = "My name is Harry and I grew up in Canada. I love bananas."
FP16 = True
NO_CUDA = False
DO_LOWER_CASE = True
MAX_SEQ_LENGTH = 384
MAX_QUERY_LENGTH = 64
VERSION_2_WITH_NEGATIVE = False
N_BEST_SIZE = 1
NULL_SCORE_DIFF_THRESHOLD = -11.0
SEED = 1
VERBOSE_LOGGING = False
verbose_logging=False
MAX_ANSWER_LENGTH=30
LOCAL_RANK = -1
