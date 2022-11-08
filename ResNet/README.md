# ResNet18-Flask
An example PyTorch implementation of a standard ResNet-18 network served with Flask, inspired from [this](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html) tutorial.

![image](https://github.com/irhumshafkat/generalRepo/blob/master/resources/carbonlong.png)

In order to use this:
1. Clone the repository
2. Run the `server.py` script to start the server. 
3. With the server activated, from a seperate terminal run the `request.py` script passing in the directory of the image to be classified using the `-i/--image` flag, (eg. `python3 request.py --image "cats.jpg"`)

You will need both PyTorch and Flask installed in the Python environment from which the scripts are run

# Build the image

1. Run the dataset downloader: `bash downloader.sh`
2. Build the docker image
