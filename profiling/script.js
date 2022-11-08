import http from 'k6/http';
export let options = {
  ext: {
    loadimpact: {
      projectID: 3597080,
      // Test runs with the same name groups test runs together
      name: "YOUR TEST NAME"
    }
  }
}


export default function () {
    http.get('http://10.244.0.93:8080')
}
