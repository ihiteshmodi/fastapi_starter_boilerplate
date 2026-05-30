# Normalized Instruction Matrix

This matrix preserves all important instruction intent from instructions.json while deduplicating overlapping guidance.

## Canonical Rules

- C01: Persistence-first domain modeling.
- C02: Naming, type hints, docstrings, import discipline.
- C03: Env-driven configuration and secret handling.
- C04: Unified response and status-code contract.
- C05: Protected-route dependencies wired from day zero.
- C06: Early health endpoint.
- C07: Specific exception handling and safe error mapping.
- C08: Create semantics (201, schema validation, resource return, idempotency check).
- C09: PUT vs PATCH semantics and partial-update safety.
- C10: Delete semantics (204 default policy).
- C11: Soft delete baseline with audit/recovery intent.
- C12: Transaction boundaries for related writes.
- C13: Optimistic locking for concurrent updates.
- C14: Bulk operations with limits and consistency.
- C15: External API reliability (timeout, raise_for_status, retries, typed errors).
- C16: Context-managed resource lifecycle.
- C17: Environment-specific runtime profile policy.
- C18: Structured logging with severity and request correlation.
- C19: Log redaction and sensitive-data policy.
- C20: Logs, metrics, traces baseline.
- C21: Symptom-first alerting policy.
- C22: JWT auth flow baseline (register/login/protected route).
- C23: JWT security hardening (exp, strong secret, anti-enumeration errors).
- C24: Test pyramid policy.
- C25: TDD-preferred, tests mandatory for important logic.
- C26: Edge-case and risk-based test prioritization.
- C27: Meaningful coverage over vanity metrics.
- C28: Pre-deploy audit gate.
- C29: Pre-flight go-live gate.
- C30: README quality contract.

## GenAI Extension Rules

- C31: Use hybrid AI architecture: four virtual layers plus production AI slices.
- C32: Keep domain and application logic decoupled from serving interfaces and provider adapters.
- C33: Define service slice explicitly: rag pipeline, semantic cache, memory, query rewrite, and routing.
- C34: Prompt assets must be versioned, typed, and registry-managed.
- C35: Security uses three guard layers: input, content, output.
- C36: Evaluation stack includes golden dataset, offline eval, and online monitoring.
- C37: Observability tracks per-stage traces, feedback linkage, and cost per query.
- C38: Treat layer boundaries as pragmatic guidance; allow selective simplification while preserving evolvability.

## FastAPI Concurrency Extension Rules

- C39: Async is for I/O concurrency, not CPU acceleration; avoid blocking calls in async routes.
- C40: CPU-heavy inference must be offloaded to worker systems or process pools.
- C41: Long-running operations should return 202 Accepted with task_id and status endpoint.
- C42: Validation must fail fast with bounded payload policies before expensive execution starts.
- C43: Use async-compatible clients and drivers in async request paths.
- C44: Design for load failure first: check pool exhaustion, blocking hotspots, timeout paths, and degradation behavior.

## Stage Mapping

1. Stage 0: C01-C04
2. Stage 1: C05-C07, C22-C23
3. Stage 2: C08-C14
4. Stage 3: C15-C16
5. Stage 4: C24-C27
6. Stage 5: C17-C21
7. Stage 6: C28-C30

GenAI extension stage mapping:

1. Stage 5A: C31-C38

FastAPI concurrency extension stage mapping:

1. Stage 3A: C39-C44