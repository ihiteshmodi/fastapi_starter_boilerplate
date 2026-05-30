---
name: fastapi-observability-operations
description: Add production-safe observability and runtime operations to FastAPI services, including logging, metrics, tracing, environment profiles, and alerting. Use when users ask for health monitoring, telemetry, or production hardening.
argument-hint: [ops-goal] [environment]
---

# FastAPI Observability Operations

## Scope

Covers canonical rules C17-C21 and lifecycle orchestration patterns.

## Workflow

1. Define environment profiles (local/dev/stage/prod).
2. Enforce structured logs and request correlation IDs.
3. Define redaction policy for sensitive fields.
4. Add metrics and trace baselines.
5. Add symptom-first alerting thresholds.
6. Apply lifespan-based startup/shutdown and mounted-subapp lifecycle policy where needed.

## Guardrails

1. Do not expose stack traces to clients in production.
2. Do not log secrets, tokens, or protected financial/health data.
3. Keep OpenTelemetry defaults environment-aware.

## Trigger Examples

Should trigger:

- "Add structured logs, request IDs, metrics, traces, and alerts."
- "Define mounted sub-app lifecycle policy and runtime health checks."

Paraphrased should trigger:

- "Harden runtime observability with environment-specific telemetry rules."

Should not trigger:

- "Create user and todo CRUD endpoints."
- "Implement query rewriting for retrieval prompts."

## Additional Resources

- Environment profiles: [references/environment-profiles.md](references/environment-profiles.md)
- Observability baseline: [references/observability-baseline.md](references/observability-baseline.md)
- Multi-app composition and mounted sub-apps: [references/multi-app-composition-mounted-subapps.md](references/multi-app-composition-mounted-subapps.md)
- Operations anti-pattern detectors: [references/anti-pattern-detectors.md](references/anti-pattern-detectors.md)
- FastAPI official middleware and error links: [references/fastapi-official-middleware-error-links.md](references/fastapi-official-middleware-error-links.md)
- Request ID and logging correlation guide: [references/request-id-logging-correlation.md](references/request-id-logging-correlation.md)
- Credential refresh lifecycle (advanced operations): [references/credential-refresh-lifecycle.md](references/credential-refresh-lifecycle.md)
- Example request-id middleware: [examples/request-id-middleware.py](examples/request-id-middleware.py)
- Example process-time middleware: [examples/process-time-middleware.py](examples/process-time-middleware.py)
- Example HTTP and validation error handlers: [examples/http-exception-and-validation-handler.py](examples/http-exception-and-validation-handler.py)
- Example credential refresh lifecycle: [examples/credential-refresh-lifecycle.py](examples/credential-refresh-lifecycle.py)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. Observability output includes structured logs, request correlation, and telemetry baseline by environment.
2. Sensitive-field redaction policy is explicit and applied to logs and error payloads.
3. Output format must include alerting signals, health checks, and runtime lifecycle expectations.
4. Edge-case handling for telemetry exporter failure and degraded tracing is documented.
5. Recovery guidance explains safe telemetry teardown and restart sequencing.