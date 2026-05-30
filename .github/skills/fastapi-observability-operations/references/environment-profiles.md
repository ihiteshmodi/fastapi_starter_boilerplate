# Environment Profiles

Local:

- OpenTelemetry off by default.
- Enable deeper logs only when debugging.
- permissive CORS allowed only for local development.
- docs exposure can be enabled.
- auth strictness can be relaxed only for explicit local testing setups.

Development:

- debug-level logs allowed.
- test credentials and sinks only.
- docs and schema endpoints typically enabled.
- moderate error detail allowed for debugging.

Staging:

- info-level logs.
- production-like telemetry and redaction.
- CORS should mirror production policy as closely as possible.
- auth strictness should match production for validation confidence.

Production:

- warning/info depending on policy.
- strict redaction and minimal error detail in responses.
- full tracing, metrics, and alerts enabled.
- strict CORS allowlist only.
- docs exposure disabled or access-controlled by policy.
- strongest auth and authorization enforcement required.