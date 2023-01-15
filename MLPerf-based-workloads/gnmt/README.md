### Introduction
  Here, we make use of the program [mlperf/inference-v2.1](https://github.com/mlcommons/inference/tree/r2.1/translation/gnmt) to do the benchmark, which comes from the official repository [tensorflow/nmt](https://github.com/tensorflow/nmt). In order to only focus on the inference process and remove useless module like datasets loader, training graph, etc., the checkpoint model will be exported as a \.pb model to be served by tensorflow/serving.

Extract the model:

- Build the image: `docker build -t gnmt_model_exporter .` 
- Export the model: `docker run --rm --name gnmt-inst-exporter -v /models/gnmt:/models/gnmt gnmt_model_exporter`

Serving the model:

- Serving by docker: `docker run -t --rm --network host  -v "/models/gnmt:/models/gnmt"  --name tfx-inst   -e MODEL_NAME=gnmt   tensorflow/serving:1.14.0-gpu`
- Or, build and test with the FaaS image: `docker build -t gnmt . && docker run -t --rm --network host -v "/models/gnmt:/models/gnmt" --name tfx-inst -e MODEL_NAME=gnmt gnmt`
- Test by cURL: `curl -d '{"inputs": "I do not like it"}' -X POST http://localhost:8501/v1/models/gnmt:predict`
- Or, test by python client: `python3 httpclient.py --model_name gnmt --port 8501` 
