##############################################################################
# Bert Setup
FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime
RUN apt-get update && apt-get install -y pbzip2 pv bzip2 cabextract git
ENV BERT_PREP_WORKING_DIR /workspace/bert/data

WORKDIR /workspace
RUN git clone https://github.com/NVIDIA/DeepLearningExamples.git && \
    cd DeepLearningExamples && \ 
    git checkout 475cff63464736d836e1113a9839fc176bf67b38 && \
    cd .. && \
    mv DeepLearningExamples/PyTorch/LanguageModeling/BERT ./bert && \
    rm DeepLearningExamples -r 

RUN pip install --no-cache-dir \
 tqdm boto3 requests six ipdb h5py nltk progressbar onnxruntime tokenizers>=0.7\
 git+https://github.com/NVIDIA/dllogger wget

RUN apt-get install -y iputils-ping wget

WORKDIR /workspace/bert
## Install lddl served as multi-node training workloader, no need 
# RUN conda install -y jemalloc
# RUN apt-get install -y libopenmpi-dev gcc g++ 
# RUN pip install git+https://github.com/NVIDIA/lddl.git
# RUN python -m nltk.downloader punkt
# RUN pip install lamb_amp_opt/

## nvidia apex torch training extension: no need
# RUN git clone https://github.com/NVIDIA/apex && \
#     cd apex && \
#     pip install -v --disable-pip-version-check --no-cache-dir \
#   --global-option="--cpp_ext" --global-option="--cuda_ext" ./
 
# prepare dataset  
COPY inference_patch/GooglePretrainedWeightDownloader.py ./data 
RUN python3 data/bertPrep.py --action download --dataset google_pretrained_weights 
RUN wget 'https://api.ngc.nvidia.com/v2/models/nvidia/bert_pyt_ckpt_large_qa_squad11_amp/versions/19.09.0/files/bert_large_qa.pt' --directory-prefix=/workspace/bert/checkpoints

##############################################################################
# Of-watchdog Setup
USER root
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /workspace
COPY index.py index.py
COPY config.py config.py
COPY inference_patch/modeling.py bert/modeling.py
COPY inference_patch/run_squad.py bert/run_squad.py
COPY requirements.txt requirements.txt 

# Function Installation
RUN pip install -r requirements.txt

# Env Setup
EXPOSE 8080

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV fprocess="python index.py"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]
