---
name: fastapi-foundation-contracts
description: Define FastAPI project foundations including settings, API contract shape, status code policy, and baseline code standards. Use when users ask for project setup, configuration, response contracts, or architecture scaffolding.
argument-hint: [goal] [constraints]
---

# FastAPI Foundation Contracts

## Scope

Covers canonical rules C01-C04.

## Workflow

1. Define persistence model boundaries before implementing routes.
2. Set naming, typing, and docstring conventions.
3. Configure environment-driven settings and secret loading.
4. Choose one response and error envelope style.
5. Establish status-code mapping policy for all operations.

## Guardrails

1. Do not hardcode secrets.
2. Do not mix response styles in the same API surface.
3. Keep imports consistent with project package layout.

## Trigger Examples

Should trigger:

- "Scaffold a FastAPI backend with proper settings and status contracts."
- "Set up environment-driven configuration and base response format."

Paraphrased should trigger:

- "Help me create the initial app skeleton and API contract rules."

Should not trigger:

- "Build an LLM evaluation pipeline."
- "Implement JWT login and refresh tokens."

## Additional Resources

- Foundation checklist: [references/foundation-checklist.md](references/foundation-checklist.md)
- Status code contract: [references/status-contract.md](references/status-contract.md)
- FastAPI official lifespan and dependency links: [references/fastapi-official-lifespan-dependencies-links.md](references/fastapi-official-lifespan-dependencies-links.md)
- Lifespan fan-in for mounted sub-apps: [references/lifespan-fan-in-mounted-subapps.md](references/lifespan-fan-in-mounted-subapps.md)
- Example lifespan and dependency yield: [examples/lifespan-and-dependency-yield.py](examples/lifespan-and-dependency-yield.py)
- Example lifespan fan-in mounted sub-apps: [examples/lifespan-fan-in-mounted-subapps.py](examples/lifespan-fan-in-mounted-subapps.py)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. Foundation output defines model boundaries, config policy, and one consistent response envelope.
2. Status-code policy is complete for create, read, update, delete, and validation failures.
3. Output format must include project conventions for naming, typing, and import discipline.
4. Edge-case handling for missing environment values and startup initialization failures is documented.
5. Recovery guidance explains safe defaults and how to fail fast on contract violations.