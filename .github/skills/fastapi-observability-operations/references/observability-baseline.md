# Observability Baseline

Logs:

- structured events with request_id, route, status, duration
- security and business events captured

Metrics:

- request rate, error rate, latency percentiles
- system resource and connection metrics

Traces:

- distributed request tracing for critical paths

Alerts:

Immediate:

- elevated error rate
- sustained high p99 latency
- failing health checks

Warning:

- resource pressure trends
- moderate error-rate drift

Use symptom-based alerting first, then investigate root causes.