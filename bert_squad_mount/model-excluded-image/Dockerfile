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
ADD probe probe

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]
