FROM --platform=${TARGETPLATFORM:-linux/amd64} alphine:latest

WORKDIR /tmp/mobilene

COPY  mobilenet_v2-b0353104.pth mobilenet_v2-b0353104.pth

CMD ["cp", "/mobilenet_v2-b0353104.pth", "/mobdel/mobilenet/mobilenet_v2-b0353104.pth"]