FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime

USER root
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN apt-get update && \ 
    apt-get install -y wget curl -y

WORKDIR /home/app
COPY server .
RUN pip install -r requirements.txt

COPY checkpoints /root/.cache/torch/checkpoints

ENV fprocess="python index.py"
EXPOSE 8080

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]
#ENTRYPOINT [ "python3", "-u", "classifier.py" ]
