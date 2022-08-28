FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:3.9

WORKDIR /tmp/mobilenet

COPY --from=mobilenet /tmp/mobilenet/mobilenet_v2-b0353104.pth .

CMD ["cp", "'mobilenet_v2-b0353104.pth'", "/model/mobilenet/"]