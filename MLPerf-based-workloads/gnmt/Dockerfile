# FaaS watchdog image
FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
# Base image
FROM tensorflow/serving:1.14.0-gpu
## Note: The model needs to be mounted into dir: $MODEL_BASE_PATH:$MODEL_NAME
ENV MODEL_BASE_PATH /models
ENV MODEL_NAME gnmt

## Setup FaaS components
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog
ENV mode="http"
ENV upstream_url="http://127.0.0.1:8051"
ENV fprocess="/usr/bin/tf_serving_entrypoint.sh"
ENTRYPOINT ["fwatchdog"]
