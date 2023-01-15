# FaaS watchdog image
FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
# Compiler image
FROM --platform=${TARGETPLATFORM:-linux/amd64} pytorch/pytorch:1.5.1-cuda10.1-cudnn7-devel as compiler
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
 && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
RUN apt-get update && apt-get install -y libsndfile1 git sox cmake build-essential && rm -rf /var/lib/apt/lists/*
COPY patch/setup.py /setup.py
RUN COMMIT_SHA=c6d12f9e1562833c2b4e7ad84cb22aa4ba31d18c && \
    git clone https://github.com/HawkAaron/warp-transducer deps/warp-transducer && \
    cd deps/warp-transducer && \
    git checkout $COMMIT_SHA && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make VERBOSE=1 && \
       export CUDA_HOME="/usr/local/cuda" && \
    export WARP_RNNT_PATH=`pwd` && \
    export CUDA_TOOLKIT_ROOT_DIR=$CUDA_HOME && \
    export LD_LIBRARY_PATH="$CUDA_HOME/extras/CUPTI/lib64:$LD_LIBRARY_PATH" && \
    export LIBRARY_PATH=$CUDA_HOME/lib64:$LIBRARY_PATH && \
    export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH && \
    export CFLAGS="-std=c++14 -I$CUDA_HOME/include $CFLAGS" && \
    export CXXFLAGS="-std=c++14 -I$CUDA_HOME/include $CXXFLAGS" && \
    cd ../pytorch_binding && \
    cp /setup.py ./setup.py && \
    python3 setup.py install --user 

# Base Image
FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime
RUN apt-get update && apt-get install -y libsndfile1 git sox && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY --from=compiler /root/.local /root/.local 
COPY requirements.txt .
RUN pip install --disable-pip-version-check -U -r requirements.txt

## Prepare src code 
COPY . .
RUN git clone --recursive https://github.com/mlcommons/inference \
    && cd inference/speech_recognition/rnnt/pytorch \
    && git checkout r2.1 \
    && git apply /workspace/patch/*.patch \ 
    && cp /workspace/server/* ./

## Setup FaaS components
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV fprocess="python /workspace/inference/speech_recognition/rnnt/pytorch/index.py"
CMD ["fwatchdog"]
