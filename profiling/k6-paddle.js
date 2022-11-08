import http from 'k6/http';
import encoding from 'k6/encoding';
import { group } from 'k6'

import { check, sleep } from 'k6';

import { Trend } from 'k6/metrics';

export const options = {
   scenarios: {
    contacts: {
      executor: 'constant-vus',
      vus: 2,
      duration: '120s', 
    },
  },
  ext: {
    loadimpact: {
      projectID: 3599369,
      // Test runs with the same name groups test runs together
      name: "Batch test"
    }
  }
};

//let shufflenet_http_duration = new Trend('shufflenet_http_duration');

//let shufflenet_req_count = new 

//let squeezenet_http_duration = new Trend('squeezenet_http_duration');

//let bert-squad_http_duration = new Trend('bert-squad_http_duration')

//let paddlespeach_http_duration = new Trend('paddlespeach_http_duration')
const binFile = open('zh.wav', 'b');
const paddledata = {
  audio: encoding.b64encode(binFile), 
  audio_format: "wav",
  sample_rate: 16000,
  lang: "zh_cn",
}
let shufflenet = {
        method: 'GET',
        url: 'http://10.106.46.112:8080/function/shufflenet/',
};

let squeezenet = {
        method: 'GET',
        url: 'http://10.106.46.112:8080/function/squeezenet',
};
let bertsquad  = {
        method: 'GET',
        url: 'http://10.106.46.112:8080/function/bert-squad/?question=What%20food%20does%20Harry%20like?&&context=My%20name%20is%20Harry%20and%20I%20grew%20up%20in%20Canada.%20I%20love%20bananas.',
};

let bertsquad_mount  = {
        method: 'GET',
        url: 'http://10.106.46.112:8080/function/bert-squad-mounted/?question=What%20food%20does%20Harry%20like?&&context=My%20name%20is%20Harry%20and%20I%20grew%20up%20in%20Canada.%20I%20love%20bananas.',
};

let paddle = {
        method: 'POST',
        url: 'http://10.106.46.112:8080/function/paddlespeech/paddlespeech/asr',
        body: JSON.stringify(paddledata), 
        params: {
            headers: { 'Content-Type': 'application/json'},
        },
};

let mobilenet = {
        method: 'GET',
        url: 'http://10.106.46.112:8080/function/mobilenet',
};


export default function () {
    //let res = http.batch([shufflenet, squeezenet, bertsquad, paddle, mobilenet])
  //let res = http.batch([shufflenet, squeezenet, bertsquad, mobilenet])
  // group usage
  //group('shufflenet', function(){
  //    http.get(shufflenet.url)
  //});
  //group('squeezenet', function(){
  //    http.get(squeezenet.url)
  //});
  //group('bertsquad', function(){
  //    http.get(bertsquad.url)
  //});
  //group('bertsquad_mount', function(){
  //    http.get(bertsquad_mount.url)
  //});
  //group('mobilenet', function(){
  //    http.get(mobilenet.url)
  //});
  group('paddle', function(){
      http.post(paddle.url, paddle.body, paddle.params)
  });
}
