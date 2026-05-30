# FastAPI GenAI Skillset

Modular skill pack for building production-ready FastAPI apps and GenAI services.

## Included Skills

- fastapi-genai-orchestrator
- fastapi-foundation-contracts
- fastapi-auth-security
- fastapi-data-crud-patterns
- fastapi-integration-reliability
- fastapi-genai-application-patterns
- fastapi-testing-quality
- fastapi-observability-operations
- fastapi-release-gates

## Design Goals

1. Keep each skill focused so trigger accuracy stays high.
2. Keep SKILL.md short and move depth into references.
3. Preserve normalized instruction coverage from instructions.json.
4. Support both strong and small models with deterministic playbooks.

## GenAI Structure Model

This pack uses a hybrid structure for AI apps:

1. Virtual layers for decoupling: domain, application, infrastructure, interfaces.
2. Production slices for reliability: services, prompts, agents, security, evaluation, observability.

This combination captures both architectural clarity and production completeness.

## Stage Order

1. Foundation and contracts
2. API skeleton and security baseline
3. Data and CRUD semantics
4. Integration resilience
5. GenAI architecture and safety patterns
6. Testing and quality
7. Observability and operations
8. Release and post-deploy gates

## Routing

Use `fastapi-genai-orchestrator` first for broad requests like "build my FastAPI app".
Use side skills directly for narrow requests like "set JWT auth" or "define CRUD update semantics".

## Coverage Map

See [normalized-instruction-matrix.md](normalized-instruction-matrix.md).

## Single Structure Reference

For one canonical FastAPI plus GenAI architecture and folder blueprint, use:

- [fastapi-genai-application-patterns/references/architecture-and-domain-genai.md](fastapi-genai-application-patterns/references/architecture-and-domain-genai.md)