# Introduction
Here we use multi-stage build to build the target image, the library will first be compiled in the devel image and then be copied into the final image.

# Instruction:
- Build image: `docker build -t rnnt .`
- Download model at host: `wget https://zenodo.org/record/3662521/files/DistributedDataParallel_1576581068.9962234-epoch-100.pt?download=1 -O /models/rnnt/rnnt.pt`
- Start the server: `docker run --network host -v /models/rnnt:/models/rnnt --rm rnnt`
- Test by k6: 'cd client && k6 run k6-rnnt.js' 
