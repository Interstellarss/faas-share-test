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

    def request(self, input_seq):
        future = self._translate(input_seq)
        result = self._parse_result(future)
        return (input_seq, result)

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

    def _parse_result(self, future):
        result = future.json()
        result = result["outputs"]
        words = ""
        for w in list(result):
            words += w[0][0] + " "
        return words

    def _translate(self, seq):
        headers = {'Content-type': 'application/json'}
        request = json.dumps({'inputs': seq})
        response = requests.post("http://" + self.endpoint + "/v1/models/gnmt:predict", data = request, timeout=2.50)
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

    test_seqs = [
        "I love it.",
        "Madam President, I should like to draw your attention to a case in which this Parliament has consistently shown an interest. It is the case of Alexander Nikitin.",
        "If you hear a lot about tiger attacks, there must be a lot of tigers around.",
        "He has a doctorate in technical sciences.",
    ]
    client = HTTPClient(model_name=args.model_name, host=args.host, port=args.port, timeout=args.timeout)

    #input_seq, output_seq = client.request(test_seqs[0])
    #print("Input : %s" % input_seq)
    #print("Output: %s" % output_seq)
   
    results = client.request_many(test_seqs)
    for r in results:
        print("Input : %s" % r[0])
        print("Output: %s" % r[1])
