---
name: fastapi-genai-orchestrator
description: Route broad FastAPI and GenAI backend requests into the correct implementation skill and stage. Use when users ask to build a complete FastAPI app, scaffold architecture, or plan end-to-end backend delivery.
argument-hint: [goal] [domain] [constraints]
---

# FastAPI GenAI Orchestrator

Use this as the main entry skill for broad requests.

## Workflow

1. Classifies request scope by stage and domain.
2. Routes work to one or more side skills.
3. Enforces implementation order and quality checks.

## Stage Router

1. Foundation and contracts -> fastapi-foundation-contracts
2. Auth and route security -> fastapi-auth-security
3. Data and CRUD semantics -> fastapi-data-crud-patterns
4. External integration reliability -> fastapi-integration-reliability
5. GenAI architecture and safety -> fastapi-genai-application-patterns
6. Testing and quality -> fastapi-testing-quality
7. Observability and runtime ops -> fastapi-observability-operations
8. Release checks and docs -> fastapi-release-gates

## Routing Rules

- If user asks "build full app" -> run stages 1 to 8 in order.
- If user asks "scaffold first and harden auth later" -> run stage 1 with auth placeholder mode, continue stages 2 to 7, then hardening pass in stage 8 review.
- If user asks only "auth/JWT/protected routes" -> run auth skill only.
- If user asks only "CRUD/update/delete semantics" -> run data skill only.
- If user asks only "timeouts/retries/external API" -> run integration skill only.
- If user asks "LLM app/agentic workflow/RAG/tool-calling" -> run GenAI skill, then testing and observability as needed.
- If user asks "production readiness" -> run observability + release skills.

## Guardrails

1. Keep business logic out of route handlers.
2. Keep all response/error contracts consistent.
3. Keep secrets and tokens out of logs and responses.
4. Do not skip tests for important logic.

## Trigger Examples

Should trigger:

- "Build a complete FastAPI plus GenAI backend from scaffold to release readiness."
- "Scaffold first, then harden auth and production checks later."

Paraphrased should trigger:

- "Plan and route the full implementation stages for this backend project."

Should not trigger:

- "Only fix this one PATCH endpoint conflict behavior."
- "Create a marketing landing page."

## Additional Resources

- Routing matrix: [references/routing-matrix.md](references/routing-matrix.md)
- Stage checklist: [references/stage-checklist.md](references/stage-checklist.md)
- GenAI routing addendum: [references/genai-routing-addendum.md](references/genai-routing-addendum.md)
- Skillset coverage: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. Broad build requests route to stages 1 through 8 in order unless the user explicitly asks to skip stages.
2. Narrow requests route to only the targeted skill and do not trigger unrelated stages.
3. Output format must include selected stage(s), rationale for routing, and any deferred hardening steps.
4. Edge-case requests that mix app scope and single-endpoint fixes must prioritize minimal routing with explicit scope confirmation.
5. Recovery guidance must state what to do when requirements are conflicting or underspecified.