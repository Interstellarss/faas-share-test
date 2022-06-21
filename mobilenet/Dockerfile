FROM cheproximity/mobilenet-ssd:latest
ADD file:592c2540de1c707636622213ee30ff5b6f8be0a48bb25c97edc7204ea4df1a81 in /
RUN /bin/sh -c set -xe 		\
    && echo '#!/bin/sh' > /usr/sbin/policy-rc.d 	\
    && echo 'exit 101' >> /usr/sbin/policy-rc.d 	\
    && chmod +x /usr/sbin/policy-rc.d 		\
    && dpkg-divert --local --rename --add /sbin/initctl 	\
    && cp -a /usr/sbin/policy-rc.d /sbin/initctl 	\
    && sed -i 's/^exit.*/exit 0/' /sbin/initctl 		\
    && echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup 		\
    && echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean 	\
    && echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean 	\
    && echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean 		\
    && echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages 		\
    && echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes 		\
    && echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests
RUN /bin/sh -c rm -rf /var/lib/apt/lists/*
RUN /bin/sh -c sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list
RUN /bin/sh -c mkdir -p /run/systemd \
    && echo 'docker' > /run/systemd/container
CMD ["/bin/bash"]


RUN /bin/sh -c apt-get update \
    && apt-get install -y --no-install-recommends         build-essential         curl         libfreetype6-dev         libpng12-dev         libzmq3-dev         pkg-config         python3         python3-dev         rsync         software-properties-common         unzip         \
    &&     apt-get clean \
    &&     rm -rf /var/lib/apt/lists/*
RUN /bin/sh -c curl -O https://bootstrap.pypa.io/get-pip.py \
    &&     python3 get-pip.py \
    &&     rm get-pip.py
RUN /bin/sh -c pip3 --no-cache-dir install         Pillow         h5py         ipykernel         jupyter         matplotlib         numpy         pandas         scipy         sklearn         \
    &&     python3 -m ipykernel.kernelspec
COPY file:c3139c07e03f4de071d6e7a04dd2cde795d1e617b712b2b1419eda23938851af in /
RUN /bin/sh -c pip3 --no-cache-dir install /tensorflow-1.8.0-cp35-cp35m-manylinux1_x86_64.whl
RUN /bin/sh -c ln -s -f /usr/bin/python3 /usr/bin/python
COPY file:50103defeea39e9f41799396ee1b8d9504c4372025d4b363c72945c356cdb36b in /root/.jupyter/
COPY dir:4679761a8b21dd5190b632d03ed07a3d0e677cdf8263e6fd696df0dc5192c9db in notebooks/
COPY file:523b42812b104f4125ce45b39e5f2ac799d152e0e2273679f6ad1f33f1034a9a in /
EXPOSE 6006
EXPOSE 8888
WORKDIR /notebooks
CMD ["/run_jupyter.sh" "--allow-root"]
WORKDIR /ml
COPY dir:ffd0974126e9a6c7943871ed478336f6d16797e89aff146c85b945be5579e709 in ml/
RUN /bin/sh -c pip install -r requirements.txt
RUN /bin/sh -c rm /*.whl;     rm -rf /notebooks/*;
ENV PATH=/ml:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CMD ["train.sh"]