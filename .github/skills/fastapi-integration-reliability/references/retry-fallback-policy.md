# Retry and Fallback Policy

Retry only on transient failures:

- network timeout
- temporary upstream unavailability
- retry-safe 5xx conditions

Do not retry on:

- invalid requests
- auth failures
- deterministic validation errors

Fallback guidance:

- return safe degraded responses when allowed by product policy
- surface machine-readable error codes when fallback is not possible
- emit metrics and logs for retry and fallback behavior