from torchvision import models, transforms
from PIL import Image
import flask
import torch
import torch.nn.functional as F
from waitress import serve
import json
import io
import time

app = flask.Flask(__name__)
model = None

def initalize():
    # loading pretrained ResNet18
    global model

    print("load to cpu, ", time.time())
    model = models.resnet152(pretrained=True)
    model.eval()
    print("load to gpu, ", time.time())
    model = model.cuda()
    print("load to gpu done, ", time.time())

    # preparing the required ResNet transofrms
    global resnet_transform
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )

    resnet_transform = transforms.Compose([transforms.Resize(224),
                                           transforms.CenterCrop(224),
                                           transforms.ToTensor(), 
                                           normalize])     

    global labels
    json_file = open('imagenet_class_index.json')
    json_str = json_file.read()
    labels = json.loads(json_str)       

def transform_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")

    return resnet_transform(image)

      
@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read into PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = transform_image(image)
            image = image.view(-1, 3, 224, 224)
            image = image.cuda()
            result = model(image)[0] 
            prediction = F.softmax(result, dim=0)
            
            topk_vals, topk_idxs = torch.topk(prediction, 3)
            
            data["predictions"] = []

            for i in range(len(topk_idxs)):
                r = {"label": labels[str(topk_idxs[i].item())][1], 
                     "probability": topk_vals[i].item()}
                data["predictions"].append(r)    

            data["success"] = True
    print("elapsed: ", time.time() - start, " with success ", data["success"] )

    return flask.jsonify(data)      

if __name__ == "__main__":
    print("Loading PyTorch model, and starting Flask server")       
    initalize()
    serve(app, host="0.0.0.0", port=5000)

            
