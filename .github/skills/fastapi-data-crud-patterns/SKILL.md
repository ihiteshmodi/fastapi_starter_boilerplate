---
name: fastapi-data-crud-patterns
description: Implement production-grade FastAPI CRUD semantics with transactions, soft delete, optimistic locking, and bulk operations. Use when users ask for create/update/delete patterns, data consistency rules, or repository and service boundaries.
argument-hint: [crud-goal] [domain]
---

# FastAPI Data CRUD Patterns

## Scope

Covers canonical rules C08-C14.

## Workflow

1. Define create contract (201 + created resource response).
2. Apply PUT vs PATCH semantics and partial update safety.
3. Apply delete contract (204 default, archive response only if contract requires).
4. Prefer soft delete with auditability.
5. Use transactions for related writes.
6. Add optimistic locking where concurrent updates are likely.
7. Support bulk operations with bounded batch policy.

## Guardrails

1. Keep transaction boundary in service/use-case layer.
2. Do not silently overwrite fields on PATCH.
3. Define explicit conflict behavior for stale writes.

## Trigger Examples

Should trigger:

- "Design PUT vs PATCH behavior for my FastAPI resource."
- "Add soft delete with audit fields and restore policy."

Paraphrased should trigger:

- "How should I handle update conflicts with optimistic locking?"

Should not trigger:

- "Configure OAuth login and token refresh."
- "Set up telemetry exporters and tracing dashboards."

## Additional Resources

- CRUD checklist: [references/crud-checklist.md](references/crud-checklist.md)
- Concurrency and bulk notes: [references/concurrency-bulk.md](references/concurrency-bulk.md)
- Soft delete and audit semantics: [references/soft-delete-audit-semantics.md](references/soft-delete-audit-semantics.md)
- Example PATCH with version check: [examples/patch-with-optimistic-lock.py](examples/patch-with-optimistic-lock.py)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. Create, update, delete semantics are explicit, including 201/204 policy and PATCH safety.
2. Transaction boundaries are defined in service or use-case layers for related writes.
3. Output format must include conflict behavior, versioning strategy, and bulk limits.
4. Edge-case behavior for stale version writes and partial payload conflicts is documented.
5. Recovery guidance explains conflict resolution and safe retry expectations.