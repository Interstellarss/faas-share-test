import http from 'k6/http';
import encoding from 'k6/encoding';

import { check, sleep } from 'k6';

import { Trend } from 'k6/metrics';

export const options = {
  stages: [
     { duration: '2s', target: 10 },
  ],
};

let shufflenet_http_duration = new Trend('shufflenet_http_duration');
export default function () {
  let paddle = {
          method: 'GET',
          url: 'http://10.109.232.51:8080/function/shufflenet/',
  };

  let res = http.batch([paddle])
}
