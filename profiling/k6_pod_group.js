import http from 'k6/http';
  
import { check, sleep } from 'k6';

import { Trend } from 'k6/metrics';
import { group } from 'k6'


//let shufflenet_http_duration = new Trend('shufflenet_http_duration');
//let shufflenet_req_count = new 
//let squeezenet_http_duration = new Trend('squeezenet_http_duration');
//let bert-squad_http_duration = new Trend('bert-squad_http_duration')
//let paddlespeach_http_duration = new Trend('paddlespeach_http_duration')

export default function () {
  let shufflenet = {
          method: 'GET',
          url: 'http://10.244.1.66:8080',
  };

  let squeezenet = {
          method: 'GET',
          url: 'http://10.244.1.66:8080',
  };
  let bertsquad  = {
          method: 'GET',
          url: 'http://10.244.0.78:8080/?question=What%20food%20does%20Harry%20like?&&context=My%20name%20is%20Harry%20and%20I%20grew%20up%20in%20Canada.%20I%20love%20bananas.',
  };

  let paddle = {
          method: 'GET',
          url: 'http://10.244.0.77:8080',
  };
  group('test', function(){
      group('test1', function(){
          http.get(shufflenet.url)
      });
      group('test2', function(){
          http.get(squeezenet.url)
      });
      group('test3', function(){
          http.get(squeezenet.url)
      });
  });
}

