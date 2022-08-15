FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:latest

WORKDIR /tmp/mobilenet

COPY ./mobilenet_v2-b0353104.pth .

CMD ["cp", "/mobilenet_v2-b0353104.pth", "/model/mobilenet/mobilenet_v2-b0353104.pth"]