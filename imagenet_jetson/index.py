
#from flask import Flask, request
import flask
from flask import Flask, request

from waitress import serve
import os
import torch

import jetson.inference
import jetson.utils

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
    raw_body = os.getenv("RAW_BODY", "true")

    as_text = True

    if is_true(raw_body):
        as_text = False

    # load an image (into shared CPU/GPU memory)
img = jetson.utils.loadImage(args.filename)

# load the recognition network
net = jetson.inference.imageNet(args.network)

# classify the image
class_idx, confidence = net.Classify(img)

# find the object description
class_desc = net.GetClassDesc(class_idx)

# print out the result
print("image is recognized as '{:s}' (class #{:d}) with {:f}% confidence".format(class_desc, class_idx, confidence * 100))
response = flask.jsonify({"message": "success"})
 response.status_code = 200

    #ret = handler.handle(request.get_data(as_text=as_text))
return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)