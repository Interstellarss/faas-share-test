#import flask
from flask import Flask, request
from mobilenet import mobilenet_v2
import torch
from waitress import serve
import os

app = Flask(__name__)
app.debug = False
model = None

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

'''
@app.route("/init", methods=["POST"])
def init():
    global model
    model = mobilenet_v2(pretrained=True)
    return ('OK', 200)
'''

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def run():
    model = mobilenet_v2(pretrained=True)
    input_size=(1, 3, 224, 224)
    x = torch.randn(input_size)
    out = model(x)
    response = flask.jsonify({"message": "success"})
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
