FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:3.9

WORKDIR /tmp/squeezenet

COPY squeezenet1_0-a815701f.pth .

COPY squeezenet1_1-f364aa15.pth .

CMD ["cp", "-r", "/tmp/squeezenet/", "/model/squeezenet/"]