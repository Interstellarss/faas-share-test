FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:3.9

WORKDIR /tmp/shufflenet

COPY shufflenetv2_x0.5-f707e7126e.pth .

COPY shufflenetv2_x1-5666bf0f80.pth .

CMD ["cp", "-r", "/tmp/shufflenet/", "/model/shufflenet/"]