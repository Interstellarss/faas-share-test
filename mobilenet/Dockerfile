
ADD file ... in /

/bin/sh -c set -xe &&


/bin/sh -c rm -rf /var/lib/apt/lists/*

/bin/sh -c sed -i 's/^#\s*\(deb.*universe\)$/\1/g'


/bin/sh -c mkdir -p /run/systemd

CMD ["/bin/bash"]


LABEL maintainer=Craig Citro <craigcitro@google.com>


/bin/sh -c apt-get update &&


/bin/sh -c curl -O https://bootstrap.pypa.io/get-pip.py


/bin/sh -c pip3 --no-cache-dir install


COPY file:c3139c07e03f4de071d6e7a04dd2cde795d1e617b712b2b1419eda23938851af in /

/bin/sh -c pip3 --no-cache-dir install


/bin/sh -c ln -s -f


COPY file:50103defeea39e9f41799396ee1b8d9504c4372025d4b363c72945c356cdb36b in /root/.jupyter/

COPY dir:4679761a8b21dd5190b632d03ed07a3d0e677cdf8263e6fd696df0dc5192c9db in /notebooks

COPY file:523b42812b104f4125ce45b39e5f2ac799d152e0e2273679f6ad1f33f1034a9a in /

EXPOSE 6006

EXPOSE 8888

WORKDIR /notebooks

CMD ["/run_jupyter.sh" "--allow-root"]

WORKDIR /ml

COPY dir:ffd0974126e9a6c7943871ed478336f6d16797e89aff146c85b945be5579e709 in /ml

/bin/sh -c pip install -r

/bin/sh -c rm /*.whl;

ENV PATH=/ml:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

CMD ["train.sh"]