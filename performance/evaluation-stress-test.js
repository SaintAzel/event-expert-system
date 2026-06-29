import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 50 },
    { duration: "30s", target: 100 },
    { duration: "30s", target: 150 },
    { duration: "30s", target: 200 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<2000"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";

const payloads = [
  { facts: [] },
  {
    facts: [
      "F001", "F002", "F005",
      "F006", "F007", "F010",
      "F016", "F017", "F020",
      "F021", "F022", "F025",
    ],
  },
  {
    facts: [
      "F001", "F002", "F005",
      "F006", "F007", "F010",
      "F011", "F012", "F015",
      "F016", "F017", "F020",
      "F021", "F022", "F025",
      "F026", "F027", "F030",
      "F031", "F032", "F035",
      "F036", "F037", "F040",
    ],
  },
];

const params = {
  headers: {
    "Content-Type": "application/json",
  },
};

export default function () {
  const payload = JSON.stringify(payloads[__ITER % payloads.length]);
  const response = http.post(`${BASE_URL}/evaluation`, payload, params);

  check(response, {
    "status is 200": (r) => r.status === 200,
    "has evaluation data": (r) => Boolean(r.json("data.evaluation")),
  });

  sleep(1);
}
