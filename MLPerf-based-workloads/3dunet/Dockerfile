FROM tensorflow/tensorflow:2.2.0-gpu 
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
 && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
RUN apt-get update && apt-get install -y git

## Prepare src code 
WORKDIR /workspace
COPY . .
RUN git clone --recursive https://github.com/mlcommons/inference \
    && cd inference/vision/medical_imaging/3d-unet-kits19 \
    && git checkout r2.1 \
    && cp /workspace/server/* ./
CMD ["/bin/bash"]
