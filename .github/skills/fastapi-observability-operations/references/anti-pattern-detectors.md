# Operations Anti-Pattern Detectors

Use this checklist during reviews and incident prevention.

## Async Blocking Detectors

- async route calling sync DB/HTTP client
- long CPU work inside async route handler
- missing timeout on outbound network calls
- long-running endpoint holding connection open instead of 202 plus task_id contract
- missing task-status endpoint for accepted background operations

## Error Contract Detectors

- broad except Exception without typed mapping
- stack traces or internal exceptions leaked to API responses
- mixed error payload formats across related endpoints

## Runtime Stability Detectors

- no request ID propagation
- no rate limits on sensitive routes
- no readiness checks for critical dependencies

## Action Rule

For every detector hit:

1. classify severity
2. add remediation task
3. add regression test or lint check where possible