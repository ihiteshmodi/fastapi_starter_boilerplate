---
name: fastapi-integration-reliability
description: Harden FastAPI external integrations with timeout, retry, HTTP error handling, and resource lifecycle safety. Use when users ask to call third-party APIs, add resilient clients, or prevent hanging requests.
argument-hint: [integration-goal] [dependencies]
---

# FastAPI Integration Reliability

## Scope

Covers canonical rules C15-C16 and resilient caching behavior.

Also covers async concurrency policy and long-task API design.

## Workflow

1. Define timeout defaults per integration type.
2. Enforce HTTP status handling and typed exception translation.
3. Add retry policy for transient errors only.
4. Use context-managed clients and resource cleanup.
5. Document fallback behavior when dependencies fail.
6. Offload CPU-heavy tasks to worker or process-pool execution.
7. Use 202 plus task_id contract for long-running APIs.

## Guardrails

1. Never call external APIs without timeout.
2. Avoid unbounded retries.
3. Do not leak upstream raw error payloads to clients.
4. Do not run CPU-heavy ML inference in async route handlers.

## Trigger Examples

Should trigger:

- "Add timeout, retry, and fallback rules for third-party API calls."
- "Design long-running inference endpoints with 202 plus task_id."

Paraphrased should trigger:

- "Prevent async blocking and offload heavy compute safely."

Should not trigger:

- "Implement JWT role hierarchy and login endpoints."
- "Write README badges and project intro text."

## Additional Resources

- API client policy: [references/api-client-policy.md](references/api-client-policy.md)
- Failure and retry policy: [references/retry-fallback-policy.md](references/retry-fallback-policy.md)
- Resilient caching patterns: [references/resilient-caching-patterns.md](references/resilient-caching-patterns.md)
- FastAPI concurrency and long-task thesis: [references/fastapi-concurrency-long-task-thesis.md](references/fastapi-concurrency-long-task-thesis.md)
- FastAPI official background task links: [references/fastapi-official-background-task-links.md](references/fastapi-official-background-task-links.md)
- Resilient background task manager pattern: [references/resilient-background-task-manager.md](references/resilient-background-task-manager.md)
- Example resilient call: [examples/resilient-http-call.py](examples/resilient-http-call.py)
- Example long task pattern: [examples/long-task-202-pattern.py](examples/long-task-202-pattern.py)
- Example background task dependency injection: [examples/background-tasks-dependency-injection.py](examples/background-tasks-dependency-injection.py)
- Example resilient background task manager: [examples/resilient-background-task-manager.py](examples/resilient-background-task-manager.py)
- Example payload guard middleware: [examples/payload-size-guard-middleware.py](examples/payload-size-guard-middleware.py)
- Example CPU offload: [examples/cpu-offload-process-pool.py](examples/cpu-offload-process-pool.py)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. External call policy enforces timeout defaults, bounded retries, and typed error translation.
2. Long-running APIs use 202 plus task_id with a status endpoint contract.
3. Output format must include failure-path behavior, fallback policy, and resource cleanup strategy.
4. Edge-case handling for pool exhaustion, retry exhaustion, and timeout saturation is documented.
5. Recovery guidance explains degradation mode and operator-visible remediation actions.