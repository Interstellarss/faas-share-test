import http from 'k6/http';

import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m30s', target: 10 },
    { duration: '20s', target: 0 },
  ],
};


export default function () {

  http.get('http://localhost:9999')
  sleep(1);

}
