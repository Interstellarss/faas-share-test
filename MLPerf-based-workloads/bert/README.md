# Introduction
The unecessary features like dataset donwloaders are removed.

- Build the image: `docker build -t bert .`
- Downlaod the model: `wget 'https://api.ngc.nvidia.com/v2/models/nvidia/bert_pyt_ckpt_large_qa_squad11_amp/versions/19.09.0/files/bert_large_qa.pt' -O /models/bert/bert_large_qa.pt`
- Run the image: `docker run --network host --rm --name bert-inst -v /models/bert:/models/bert bert`
- Run the cURL commands to generate a request: `curl "localhost:5000/?question=What%20food%20does%20Harry%20like?&&context=My%20name%20is%20Harry%20and%20I%20grew%20up%20in%20Canada.%20I%20love%20bananas."`
