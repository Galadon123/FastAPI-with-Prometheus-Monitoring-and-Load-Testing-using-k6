import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter } from 'k6/metrics';

// Custom metrics
const postRequests = new Counter('post_requests');

export let options = {
  vus: 10, // 10 virtual users
  duration: '30s', // Test duration of 30 seconds
};

export default function () {
  // Make a POST request to the /submit endpoint
  let url = 'http://localhost:8000/submit';
  let payload = JSON.stringify({ name: 'John Doe', age: 30 });
  let params = { headers: { 'Content-Type': 'application/json' } };

  // Send the POST request
  let res = http.post(url, payload, params);

  // Track POST requests
  postRequests.add(1);

  // Check that the response status is 200
  check(res, { 'status is 200': (r) => r.status === 200 });

  // Pause for a moment between requests
  sleep(1);
}
