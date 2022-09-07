wget -c https://paddlespeech.bj.bcebos.com/PaddleAudio/zh.wav
{   printf '{"audio": "'
    base64 zh.wav
    printf '", "audio_format":"wav", "sample_rate": 16000, "lang": "zh_cn"}'
}|  curl -H "Content-Type: application/json" --data @- -X POST localhost:8080/paddlespeech/asr
