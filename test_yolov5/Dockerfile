# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
# Builds ultralytics/yolov5:latest image on DockerHub https://hub.docker.com/r/ultralytics/yolov5
# Image is CUDA-optimized for YOLOv5 single/multi-GPU training and inference

# Start FROM NVIDIA PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/classic-watchdog:0.2.1 as watchdog
FROM nvcr.io/nvidia/pytorch:22.05-py3
RUN rm -rf /opt/pytorch  # remove 1.2GB dir

# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf https://ultralytics.com/assets/Arial.Unicode.ttf /root/.config/Ultralytics/

#copy fwatchdog
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Install linux packages
RUN apt update && apt install --no-install-recommends -y zip htop screen libgl1-mesa-glx

# Install pip packages
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip uninstall -y torch torchvision torchtext Pillow
#RUN pip install --no-cache -r requirements.txt albumentations wandb gsutil notebook Pillow>=9.1.0 \
#    'opencv-python<4.6.0.66' \
#    --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install  -r requirements.txt

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app
RUN git clone https://github.com/ultralytics/yolov5 /usr/src/yolov5

#COPY 

#ENV fprocess="python /usr/src/yolov5/detect.py --weights yolov5s.pt --source /usr/src/yolov5/data/images/bus.jpg"
ENV fprocess="python inference.py"


EXPOSE 8080

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
# Set environment variables
ENV OMP_NUM_THREADS=8

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]