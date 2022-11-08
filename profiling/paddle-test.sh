#wget -c https://paddlespeech.bj.bcebos.com/PaddleAudio/zh.wav
for i in {1..10}; do
    {   printf '{"audio": "'
        base64 zh.wav
        printf '", "audio_format":"wav", "sample_rate": 16000, "lang": "zh_cn"}'
    }|  curl -H "Content-Type: application/json" --data @- -X POST http://10.109.232.51:8080/function/paddlespeech//paddlespeech/asr
done
