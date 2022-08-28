FROM --platform=${TARGETPLATFORM:-linux/amd64} alpine:3.9

WORKDIR /tmp/squeezenet

COPY --from=squeezenet /tmp/squeezenet/squeezenet1_0-a815701f.pth .

COPY --from=squeezenet /tmp/squeezenet/squeezenet1_1-f364aa15.pth .

CMD ["cp", "/tmp/squeezenet/", "/model/squeezenet/"]