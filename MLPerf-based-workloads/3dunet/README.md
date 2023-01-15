# Introduction

- Build the image: `docker build -t 3dunet .`
- Run the image: `docker run --network host -v /models/3dunet:/models/3dunet 3dunet`
- Note: if there's no pretrained model on the host, run `make download_tensorflow_model` in advance in the directory server
- Run the client (approx. 20s): `python3 httpclient.py --port 5000 --model_name 3dunet`
  and you will get the response like: `Output: {"output":[1,1,192,384,384],"success":true}`
