from kafka import KafkaConsumer
import os
import torch

from squeezenet import squeezenet1_1
model, device = squeezenet1_1(pretrained=True)

def handel():
    input_size=(1, 3, 224, 224)
    x = torch.randn(input_size, device=device)
    out = model(x)
    
    response = jsonify({"message": "success", "status":200})
    return response

consumer = KafkaConsumer(
    'bertsquad',
     bootstrap_servers=['kafka.default.svc.cluster.local:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     )
for message in consumer:
    message = message.value
    print('{} received!'.format(message))
    handel()
