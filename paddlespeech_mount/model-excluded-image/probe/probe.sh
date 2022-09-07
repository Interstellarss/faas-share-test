if test -f "/healthz"; then
   exit 0
fi

function probing
{
chmod +x /home/app/probe/curl
{   printf '{"audio": "'
    base64 /home/app/probe/zh.wav
    printf '", "audio_format":"wav", "sample_rate": 16000, "lang": "zh_cn"}'
}|  /home/app/probe/curl -H "Content-Type: application/json" --data @- -X POST localhost:8080/paddlespeech/asr
}

RESULT=$(probing)
if [[ $RESULT =~ .*\"success\":true.* ]]; then
  touch /healthz
  exit 0
else
  exit 1
fi

