FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime

USER root
#copy fwatchdog
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app
COPY index.py index.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#COPY squeezenet1_0-a815701f.pth squeezenet1_0-a815701f.pth
#COPY squeezenet1_1-f364aa15.pth squeezenet1_1-f364aa15.pth
COPY squeezenet.py squeezenet.py
#COPY classifier.py classifier.py

RUN mkdir -p function
RUN touch ./function/__init__.py
#USER root
WORKDIR /home/app/function
#COPY mobilenet_v2-b0353104.pth mobilenet_v2-b0353104.pth

#COPY function/handler.py   .

WORKDIR /home/app/

RUN apt-get update && \ 
    apt-get install -y wget curl -y

ADD porbe probe


ENV fprocess="python index.py"

EXPOSE 8080

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
# Set environment variables
#ENV OMP_NUM_THREADS=8

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]
#ENTRYPOINT [ "python3", "-u", "classifier.py" ]



