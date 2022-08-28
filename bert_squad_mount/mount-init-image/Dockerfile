FROM ubuntu:18.04

RUN apt-get update && apt-get install -y wget git python3 python3-pip
RUN pip3 install wget nltk

WORKDIR /workspace
ENV BERT_PREP_WORKING_DIR /root/bert/data
RUN git clone https://github.com/NVIDIA/DeepLearningExamples.git && \
    cd DeepLearningExamples && \
    git checkout 475cff63464736d836e1113a9839fc176bf67b38 && \
    cd .. && \
    mv DeepLearningExamples/PyTorch/LanguageModeling/BERT ./bert && \
    rm DeepLearningExamples -r 

COPY GooglePretrainedWeightDownloader.py /workspace/bert/data
COPY downloader.sh downloader.sh
CMD ["bash", "downloader.sh"]
