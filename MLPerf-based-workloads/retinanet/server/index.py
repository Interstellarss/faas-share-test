import flask
from waitress import serve
import json
import io
import time
from backend_onnxruntime import BackendOnnxruntime
from PIL import Image
import numpy as np

app = flask.Flask(__name__)
model = None
labels = None
log_enabled = True
base_dir = "/workspace/inference/vision/classification_and_detection/python"

def initialize():
    global model, labels
    backend = BackendOnnxruntime()
    model_path = "/models/retinanet/resnext50_32x4d_fpn.onnx"
    model = backend.load(model_path)
    with open(base_dir + '/retinanet_class_index.json') as json_file:
        labels = json.loads(json_file.read())

def transform_image(image):
    image = Image.open(io.BytesIO(image))
    image = image.resize((800, 800))
    image = np.array(image).astype(np.float32)
    image = image/255.
    image = np.moveaxis(image, -1, 0)
    image = image[np.newaxis, :]

    return image

def post_process(result):
    bboxes_ = result[0] 
    scores_ = result[1] 
    labels_ = result[2]
    topk = min(5, len(bboxes_))
    labels_ = [labels[str(idx)] for idx in labels_[:topk]]
    result = [bboxes_[:topk].tolist(), labels_, scores_[:topk].tolist()]
    return result

@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"].read()
            image = transform_image(image)
            output = model.predict({"images":image})
            output = post_process(output)
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
