FROM tensorflow/tensorflow:1.14.0-gpu-py3
RUN apt-key del 7fa2af80 && apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends wget \
    unzip \
    git


# clone and patch
WORKDIR /workspace 
COPY . .
RUN git clone --recursive https://github.com/mlcommons/inference \
    && cd inference/translation/gnmt/tensorflow/ \
    && git checkout r2.1 \
    && cp /workspace/patch/* ./nmt \
    && chmod +x ./download_dataset.sh ./verify_dataset.sh  ./download_trained_model.sh \
    && ./download_dataset.sh && ./verify_dataset.sh && ./download_trained_model.sh \
    && mv nmt/checkpoint ende_gnmt_model_4_layer/checkpoint \ 
    && mv ende_gnmt_model_4_layer nmt/data/models

# The .pb model will be exported to /models/gnmt
# So, we can run the docker with -v /models/gnmt:/models/gnmt
CMD cd inference/translation/gnmt/tensorflow/ \
    && python -m nmt.exporter_test 

