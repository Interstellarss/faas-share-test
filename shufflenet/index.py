# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

#from flask import Flask, request
import flask
from flask import Flask, request
#from function import handler
from waitress import serve
import os
import torch

from shufflenet import shufflenet_v2_x0_5

app = Flask(__name__)

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
    
    model = shufflenet_v2_x0_5(pretrained=True)
    input_size=(1, 3, 224, 224)
    x = torch.randn(input_size)
    out = model(x)

    #ret = handler.handle(request.get_data(as_text=as_text))
    return str(out)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)