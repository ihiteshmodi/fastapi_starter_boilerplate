# Trigger Test Set

## Should Trigger

1. Build a production FastAPI backend for orders with auth, CRUD, tests, and deployment checks.
2. Add JWT login/register and protect all user profile routes.
3. Refactor my update endpoints to proper PATCH semantics with optimistic locking.
4. Add retries, timeouts, and safe error translation for external payment API calls.
5. Add structured logging, request IDs, and health/metrics for production readiness.
6. Create release checklists before we deploy this FastAPI service.
7. Build a FastAPI-based LLM API with safe tool-calling and fallback strategy.

## Paraphrased Should Trigger

1. Help me scaffold a clean FastAPI service that is secure and ops-ready.
2. I need robust outbound API clients so calls do not hang or fail silently.
3. I want an agentic FastAPI app with model routing and evaluation baselines.

## Should Not Trigger

1. Build a React landing page with animations.
2. Explain Java thread scheduling internals.
3. Write a bash script for local file backup only.

## End-to-End Scenario

Prompt:

1. Build and harden a FastAPI plus GenAI backend from scaffold through release gates.

Expected routing outcome:

1. Orchestrator routes to stages 1 through 8 in order.
2. Output includes stage-by-stage plan, validations, and release readiness summary.

## Failure and Recovery Scenario

Prompt:

1. Add resilient payment API integration where retries are exhausted, then provide recovery behavior and operator actions.

Expected routing outcome:

1. Routes to integration reliability skill primarily, with testing quality and observability support as needed.
2. Output includes timeout and retry policy, failure translation, degraded mode, and remediation checklist.

## Edge-Case Scenario

Prompt:

1. I need only one PATCH conflict fix, but also want production hardening guidance without changing the whole architecture.

Expected routing outcome:

1. Orchestrator prioritizes narrow routing to data CRUD patterns first.
2. Output explicitly marks optional hardening follow-up stages instead of forcing full stage 1 through 8 routing.