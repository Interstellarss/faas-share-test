if test -f "/healthz"; then
   exit 0
fi

function probing
{
chmod +x /workspace/probe/curl
/workspace/probe/curl "localhost:5000/?question=What%20food%20does%20Harry%20like?&&context=My%20name%20is%20Harry%20and%20I%20grew%20up%20in%20Canada.%20I%20love%20bananas."
}

RESULT=$(probing)
if [[ $RESULT =~ .*\"message\":\"success\".* ]]; then
  touch /healthz
  exit 0
else
  exit 1
fi

