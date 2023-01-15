import flask
from waitress import serve
import json
import io
import time
from backend_pytorch import BackendPytorchNative
from scipy.io import wavfile

app = flask.Flask(__name__)
model = None
log_enabled = True
gpu_enabled = True

def initialize():
    global model
    model = BackendPytorchNative(use_gpu=gpu_enabled)
    model.load(config_path = "/workspace/inference/speech_recognition/rnnt/pytorch/configs/rnnt.toml", model_path = "/models/rnnt/rnnt.pt")
    
@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("data"):
            # read into PIL format
            raw_data = flask.request.files["data"].read()
            rate, raw_data = wavfile.read(io.BytesIO(raw_data))
            output = model.predict(raw_data)
            output = ''.join(output)  #char list to string
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
