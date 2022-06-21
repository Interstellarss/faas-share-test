
FROM --platform=${TARGETPLATFORM:-linux/amd64}  ghcr.io/openfaas/of-watchdog:0.9.6 as watchdog
#need to modify to nvidia pytorch
FROM nvcr.io/nvidia/pytorch:22.04-py3

#copy fwatchdog
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY mobilenet_v2-b0353104.pth mobilenet_v2-b0353104.pth
COPY mobilenet.py mobilenet.py
COPY classifier.py classifier.py

#ENTRYPOINT [ "python3", "-u", "classifier.py" ]

ENV fprocess="python3 classifier.py"

EXPOSE 8080

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
# Set environment variables
ENV OMP_NUM_THREADS=8

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]

#ENTRYPOINT [ "python3", "-u", "classifier.py" ]