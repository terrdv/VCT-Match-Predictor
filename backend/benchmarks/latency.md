## Performance

January 19th:

Latency was measured locally using repeated HTTP requests. 

| Endpoint | Avg | p95 | p 99 |
|--------|-----|-----|
| GET /api/info/<team> | 22 ms | 42 ms | 79 ms|
| GET /api/matchup_data | 23 ms | 23 ms | 26 ms |
| GET /api/predict | 44 ms | 52 ms | 71 ms |

Measurements taken over 50 requests on localhost.
