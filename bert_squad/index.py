# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

#from flask import Flask, request
import flask
from flask import Flask, request
#from function import handler
from waitress import serve
import os
import sys
import logging
import json
import torch

import numpy as np
import argparse
import collections
from types import SimpleNamespace

from bert.modeling import BertForQuestionAnswering, BertConfig, WEIGHTS_NAME, CONFIG_NAME
from bert.tokenization import (BasicTokenizer, BertTokenizer, whitespace_tokenize)
from bert.inference import preprocess_tokenized_text, get_answer
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# python   inference.py --init_checkpoint=/workspace/bert/checkpoints/bert_large_qa.pt --bert_model=bert-large-uncased  --vocab_file=/workspace/bert/data/download/google_pretrained_weights/uncased_L-24_H-1024_A-16/vocab.txt  --config_file=/workspace/bert/bert_configs/large.json  --question="What food does Harry like?" --context="My name is Harry and I grew up in Canada. I love bananas." --fp16
def initargs():
    args = argparse.ArgumentParser().parse_args()
    args.init_checkpoint = app.config["INIT_CHECKPOINT"]
    args.bert_model = app.config["BERT_MODEL"]
    args.vocab_file = app.config["VOCAB_FILE"]
    args.config_file = app.config["CONFIG_FILE"]
    args.question = app.config["QUESTION"]
    args.context = app.config["CONTEXT"]
    args.fp16 = app.config["FP16"]
    args.no_cuda = app.config["NO_CUDA"]
    args.do_lower_case = app.config["DO_LOWER_CASE"]
    args.max_seq_length = app.config["MAX_SEQ_LENGTH"]
    args.max_query_length = app.config["MAX_QUERY_LENGTH"]
    args.version_2_with_negative = app.config["VERSION_2_WITH_NEGATIVE"]
    args.n_best_size = app.config["N_BEST_SIZE"]
    args.null_score_diff_threshold = app.config["NULL_SCORE_DIFF_THRESHOLD"]
    args.max_answer_length = app.config["MAX_ANSWER_LENGTH"]
    args.local_rank = app.config["LOCAL_RANK"]
    args.verbose_logging = app.config["VERBOSE_LOGGING"]
    args.seed = app.config["SEED"]
    #print(args)
    return args

app = Flask(__name__)
app.config.from_pyfile("config.py")
args = initargs()
device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
#device = torch.device("cpu")
tokenizer = BertTokenizer(args.vocab_file, do_lower_case=args.do_lower_case, max_len=512) # for bert large

# Prepare model
config = BertConfig.from_json_file(args.config_file)

# Padding for divisibility by 8
if config.vocab_size % 8 != 0:
    config.vocab_size += 8 - (config.vocab_size % 8)
    # initialize model
model = BertForQuestionAnswering(config)
model.load_state_dict(torch.load(args.init_checkpoint, map_location='cuda:0')["model"])
model.to(device)
if args.fp16:
    model.half()
model.eval()
#print("model loaded!", flush=True)

# distutils.util.strtobool() can throw an exception
def is_true(val):
    return len(val) > 0 and val.lower() == "true" or val == "1"

@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def main_route(path):
    raw_body = os.getenv("RAW_BODY", "false")

    as_text = True

    if is_true(raw_body):
        as_text = False
    
    args.question = request.args.get('question')
    args.context = request.args.get('context')
    #print("question: ", args.question)
    #print("context: ", args.context)
    if args.question == None or args.context == None:
        response = flask.jsonify({"message": "invalid request"})
        response.status_code = 400
        return response

    # preprocessing
    doc_tokens = args.context.split()
    query_tokens = tokenizer.tokenize(args.question)
    feature = preprocess_tokenized_text(doc_tokens,
                                        query_tokens,
                                        tokenizer,
                                        max_seq_length=args.max_seq_length,
                                        max_query_length=args.max_query_length)

    tensors_for_inference, tokens_for_postprocessing = feature

    input_ids = torch.tensor(tensors_for_inference.input_ids, dtype=torch.long).unsqueeze(0)
    segment_ids = torch.tensor(tensors_for_inference.segment_ids, dtype=torch.long).unsqueeze(0)
    input_mask = torch.tensor(tensors_for_inference.input_mask, dtype=torch.long).unsqueeze(0)

    # load tensors to device
    input_ids = input_ids.to(device)
    input_mask = input_mask.to(device)
    segment_ids = segment_ids.to(device)

    # run prediction
    with torch.no_grad():
        start_logits, end_logits = model(input_ids, segment_ids, input_mask)
    #print("inference completed!", flush=True)

    # post-processing
    start_logits = start_logits[0].detach().cpu().tolist()
    end_logits = end_logits[0].detach().cpu().tolist()
    answer, answers = get_answer(doc_tokens, tokens_for_postprocessing,
                                 start_logits, end_logits, args)

    #print result
    #print(answer)
    #print(json.dumps(answers, indent=4))

    response = flask.jsonify({"message": "success"})
    response.status_code = 200
    #ret = handler.handle(request.get_data(as_text=as_text))
    #return str(out)
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, backlog=10, connection_limit=10)

