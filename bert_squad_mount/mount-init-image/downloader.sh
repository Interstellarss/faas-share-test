python3 /root/bert/data/bertPrep.py --action download --dataset google_pretrained_weights
wget 'https://api.ngc.nvidia.com/v2/models/nvidia/bert_pyt_ckpt_large_qa_squad11_amp/versions/19.09.0/files/bert_large_qa.pt' --directory-prefix=/workspace/bert/chekpoints
