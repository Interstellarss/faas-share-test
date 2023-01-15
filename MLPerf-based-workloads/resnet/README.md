# Introduction
Run one of the following command to download the models and build the docker image:
""" 
1.1 make download_tensorflow_model 
1.2 make download_pytorch_model 
1.3 make download_onnx_model 
2.1 make build_docker_pytoch 
2.2 make build_docker_tensorflow 
2.3 make build_docker_onnxruntime 
"""
- Run the image: `docker run --network host --rm -v /models/resnet:/models/resnet resnet:[tensorflow/pytorch/onnxruntime]`
- Run the perf script in the client folder: `k6 run k6.js`.

  Note: the inference result generated from the pretrained model tensorflow/onnxruntime provided by NVIDIA might be wrong, but it does not impact the performance test which we focus on
