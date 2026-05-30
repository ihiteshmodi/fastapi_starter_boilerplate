---
name: fastapi-testing-quality
description: Define and implement FastAPI testing strategy with a practical test pyramid, edge-case coverage, and agent-friendly quality rules. Use when users ask for test plans, unit/integration structure, or quality gates.
argument-hint: [test-goal] [scope]
---

# FastAPI Testing Quality

## Scope

Covers canonical rules C24-C27.

## Workflow

1. Define test scope by pyramid layers.
2. Prioritize unit and integration tests for critical logic.
3. Add edge-case and security-path tests.
4. Apply meaningful coverage criteria rather than vanity targets.
5. Enforce policy: important logic must have tests.

## Guardrails

1. Do not rely only on E2E tests.
2. Do not optimize for coverage percentage alone.
3. Keep test fixtures deterministic.

## Trigger Examples

Should trigger:

- "Create a test plan for unit, integration, and failure-path coverage."
- "Add cache resilience and lifecycle teardown tests for this service."

Paraphrased should trigger:

- "What should we test first to catch production failures early?"

Should not trigger:

- "Set CORS allowlist and docs visibility rules."
- "Implement JWT endpoints and token validation logic."

## Additional Resources

- Test pyramid policy: [references/test-pyramid-policy.md](references/test-pyramid-policy.md)
- Edge-case matrix: [references/edge-case-matrix.md](references/edge-case-matrix.md)
- Cache and lifecycle tests: [references/cache-and-lifecycle-tests.md](references/cache-and-lifecycle-tests.md)
- Test stability for retries and telemetry: [references/test-stability-retries-telemetry.md](references/test-stability-retries-telemetry.md)
- FastAPI official testing links: [references/fastapi-official-testing-links.md](references/fastapi-official-testing-links.md)
- Example dependency override test: [examples/testclient-dependency-override.py](examples/testclient-dependency-override.py)
- Example lifespan and websocket tests: [examples/test-lifespan-and-websocket.py](examples/test-lifespan-and-websocket.py)
- Example test stability fixture pattern: [examples/test-stability-retry-and-telemetry.py](examples/test-stability-retry-and-telemetry.py)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. Test plan output maps critical behavior to unit, integration, and end-to-end coverage.
2. Reliability checks include deterministic fixtures and retry-wait neutralization where applicable.
3. Output format must include prioritized test list, risk rationale, and expected assertions.
4. Edge-case handling covers failure-paths, teardown safety, and flaky-test prevention.
5. Recovery guidance explains how to triage and stabilize failing test runs.