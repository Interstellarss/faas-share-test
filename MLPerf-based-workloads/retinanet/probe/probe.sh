if test -f "/healthz"; then
   exit 0
fi

function probing
{
chmod +x /workspace/probe/curl
/workspace/probe/curl -i -X POST -H "Content-Type: multipart/form-data" -F "payload=@/workspace/probe/car.jpg" http://localhost:5000 
}

RESULT=$(probing)
if [[ $RESULT =~ .*\"success\":true.* ]]; then
  touch /healthz
  exit 0
else
  exit 1
fi

