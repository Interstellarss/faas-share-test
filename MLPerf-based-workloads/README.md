The building and testing instructions are described in each workload.

The prebuilt images are:

- `resnet`(vision/classification\_and\_detection): `yukiozhu/mlperf-faas-resnet:[pytorch/tensorflow/onnx]`
- `3dunet`(vision/medical\_imaging/3d-unet-kits19): `yukiozhu/mlperf-faas-3dunet`
- `retinanet`(vision/classification\_and\_detection): `yukiozhu/mlperf-faas-retinanet`
- `bert`(language/bert): `yukiozhu/mlperf-faas-bert` 
- `gnmt`(translation/gnmt): `yukiozhu/mlperf-faas-gnmt`
- `rnnt`(speech\_recognition/rnnt): `yukiozhu/mlperf-faas-rnnt` 

Note: the models should be already existed on the host, e.g. /models/3dunet/3dunet\_kits19\_128x128x128.tf. Please refer to the README instructions of each workload to download the models.

Running examples:

``` 
docker run --network host -v /models/3dunet:/models/3dunet yukiozhu/mlperf-faas-3dunet
cd faas-share-test/MLPerf-based-workloads/3dunet/client
python3 httpclient.py --port 5000 --model_name 3dunet
```
