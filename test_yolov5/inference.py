import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_test.pt')  # or yolov5n - yolov5x6, custom

# Images
img = '/usr/src/data/images/bus.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print() 