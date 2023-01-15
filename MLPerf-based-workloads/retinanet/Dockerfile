# FaaS watchdog image
FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
# Base Image
FROM nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04
RUN apt-get update && apt-get install -y python3 python3-pip git && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt .
RUN pip3 install --disable-pip-version-check -U -r requirements.txt

## Prepare src code 
COPY . .
RUN git clone --recursive https://github.com/mlcommons/inference \
    && cd inference/vision/classification_and_detection/python \
    && git checkout r2.1 \
    && cp /workspace/server/* ./

## Setup FaaS components
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV fprocess="python3 /workspace/inference/vision/classification_and_detection/python/index.py"
CMD ["fwatchdog"]
