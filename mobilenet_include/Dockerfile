FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
#need to modify to nvidia pytorch
#FROM nvcr.io/nvidia/pytorch:22.04-py3
#FROM bitnami/pytorch:1.5.1
FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime


RUN apt-get update && \ 
    apt-get install -y wget curl -y



USER root
#copy fwatchdog
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

#RUN addgroup -S app && adduser app -S -G app
#RUN chown app /home/app

#USER app



ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app

COPY index.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY mobilenet_v2-b0353104.pth mobilenet_v2-b0353104.pth
COPY mobilenet.py mobilenet.py
COPY index.py index.py



#USER app

RUN mkdir -p function
RUN touch ./function/__init__.py
#USER root
WORKDIR /home/app/function
#COPY mobilenet_v2-b0353104.pth mobilenet_v2-b0353104.pth

COPY function/handler.py   .
#COPY function/mobilenet.py .
#COPY function/mobilenet_v2-b0353104.pth .
#RUN chown -R app:app ../

#ARG TEST_COMMAND=tox
#ARG TEST_ENABLED=true
#RUN [ "$TEST_ENABLED" = "false" ] && echo "skipping tests" || eval "$TEST_COMMAND"



WORKDIR /home/app/
#ENTRYPOINT [ "python3", "-u", "classifier.py" ]
#USER app

RUN apt-get update && \ 
    apt-get install -y wget curl -y

ADD probe probe

ENV fprocess="python index.py"

EXPOSE 8080

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
# Set environment variables
#ENV OMP_NUM_THREADS=8

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]