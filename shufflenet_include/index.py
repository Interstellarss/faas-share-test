# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

#from flask import Flask, request
import flask
from flask import Flask, request
#from function import handler
#from waitress import serve
from celery import Celery
import os
import torch

from shufflenet import shufflenet_v2_x0_5


#app = Flask(__name__)
app = Celery(
    'index',
    broker='redis://10.100.81.107:6379',
    backend='redis://10.100.81.107:6379',
    #include=['app.index']
)


app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
    CELERY_TASK_PROTOCOL=1,
)

model, device = shufflenet_v2_x0_5(pretrained=True)
podname = os.getenv("POD_NAME")

# distutils.util.strtobool() can throw an exception
def is_true(val):
    return len(val) > 0 and val.lower() == "true" or val == "1"

#@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

#@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
#@app.route("/<path:path>", methods=["POST", "GET"])
@app.task
def shufflenet(path):
    #raw_body = os.getenv("RAW_BODY", "false")

    #as_text = True

    #if is_true(raw_body):
    #    as_text = False
    
    #model, device = shufflenet_v2_x0_5(pretrained=True)
    input_size=(1, 3, 224, 224)
    x = torch.randn(input_size, device=device)
    out = model(x)
    #response = flask.jsonify({"message": "success"})
    #response.status_code = 200
    #ret = handler.handle(request.get_data(as_text=as_text))
    #return str(out)
    tmp = str(out)
    return str(podname)

if __name__ == '__main__':
    #serve(app, host='0.0.0.0', port=5000, backlog=10)
    #app.run(host='0.0.0.0', port=5000)
    app.start()
    #app.app_context().push()

