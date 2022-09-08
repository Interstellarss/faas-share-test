if test -f "/healthz"; then
   exit 0
fi

function probing
{
#chmod +x /home/app/probe/curl
 #/home/app/probe/curl -H "Content-Type: application/json" --data @- -X POST localhost:8080/paddlespeech/asr
 curl localhost:8080
}

RESULT=$(probing)
if [[ $RESULT =~ .*\"success\":true.* ]]; then
  touch /healthz
  exit 0
else
  exit 1
fi

