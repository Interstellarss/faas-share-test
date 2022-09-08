FROM alpine:latest

RUN apk add --no-cache wget 

WORKDIR /workspace

# Prepare for Dataset (for more details: paddlespeech/resource/pretrained_models.py)
COPY downloader.sh downloader.sh
CMD ["sh", "downloader.sh"]
