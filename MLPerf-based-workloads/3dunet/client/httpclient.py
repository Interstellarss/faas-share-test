import http.client
import json
import argparse
import requests
class HTTPClient():

    def __init__(self, model_name="address", host="localhost", port=9000, timeout=10):
        self.model_name = model_name
        self.host = host
        self.port = port
        self.timeout = timeout
        self.endpoint = self.host + ":" + str(self.port)

    def request_many(self, input_seqs):
        futures = []
        for s in input_seqs:
            future = self._translate(s)
            futures.append(future)
        pairs = []
        for seq, future in zip(input_seqs, futures):
            result = self._parse_result(future)
            pairs.append((seq, result))
        return pairs

    def request(self):
        #headers = {'Content-type': 'application/json'}
        raw_data = open('sample.pkl', 'rb')
        response = requests.post("http://" + self.endpoint + "/predict", files = dict('payload'=raw_data) )
        #conn = http.client.HTTPConnection(self.endpoint)
        #conn.request('POST', '/v1/models/gnmt:predict', request, headers)
        #response = conn.getresponse()
        return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", required=True, help="model name")
    parser.add_argument("--host", default="localhost", help="model server host")
    parser.add_argument("--port", type=int, default=9000, help="model server port")
    parser.add_argument("--timeout", type=float, default=10.0, help="request timeout")
    args = parser.parse_args()

    client = HTTPClient(model_name=args.model_name, host=args.host, port=args.port, timeout=args.timeout)
    print("Request sending; Note that the processing time will be approximately 20s")
    output = client.request()
    print("Output: %s" % output.text)
