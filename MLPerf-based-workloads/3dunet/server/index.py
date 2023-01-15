import flask
from waitress import serve
import json
import io
import time
from tensorflow_SimplifiedSUT import _3DUNET_TensorFlow_SimplifedSUT as backend
import pickle

app = flask.Flask(__name__)
model = None
log_enabled = True

def initialize():
    global model
    model_path = "/models/3dunet/3dunet_kits19_128x128x128.tf"
    model = backend(model_path)
    
@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("data"):
            raw_data = flask.request.files["data"].read()
            input_data = pickle.loads(raw_data)
            output = model.predict(input_data)
            data["success"] = True
            data["output"] = output 
    if log_enabled:
        print("output:", output)
        print("elapsed: ", time.time() - start, " with success ", data["success"] )

    return flask.jsonify(data)      

if __name__ == "__main__":
    print("Loading PyTorch model, and starting Flask server")       
    initialize()
    serve(app, host="0.0.0.0", port=5000)
