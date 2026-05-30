# Request ID and Logging Correlation

Use one request ID for all logs and downstream calls across a request path.

## Goals

- correlate all log lines for a single request
- return the same ID to clients for support and debugging
- propagate ID to downstream services with outbound headers

## Minimum Pattern

1. Read incoming x-request-id if present, else generate one.
2. Store it in request context (for async-safe log correlation).
3. Add it to every log record.
4. Set the same x-request-id header on the response.
5. Forward it in outbound requests.

## Why Context Storage Matters

Thread-local storage can break in async execution. Use request-scoped async context (for example, Python contextvars) so concurrent requests do not leak correlation IDs into each other.

## FastAPI Example

See: ../examples/request-id-middleware.py

## Operational Rules

- Keep ID format stable across services.
- Never log secrets even when request IDs are present.
- Include request_id in error logs and timeout logs.
- Preserve incoming request IDs from trusted edge proxies.
- Generate server-side IDs when missing or malformed.
