import http from 'k6/http';
import encoding from 'k6/encoding';
import { group } from 'k6'
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

export const options = {
   scenarios: {
    contacts: {
      executor: 'constant-vus',
      startTime: '0s',
      vus: 1,
      iterations: 1,
      //duration: '2m',
   },
  },
};
//Task specific
const sample = open('sample.pkl', 'br');
const fd = new FormData();
fd.append('data', http.file(sample, 'sample.pkl'));
let unet = {
        method: 'POST',
	url: 'http://localhost:5000/predict',
        body: fd.body(), 
        params: {
            headers: {
	      'Content-Type': 'multipart/form-data; boundary=' + fd.boundary 
	    },
        },
};
export default function () {
  const res = http.post(unet.url, unet.body, unet.params)
  check(res, {
    'is status 200': (r) => r.status === 200,
    //'check body': (r) => r.body.includes('knock'),
  });
}
