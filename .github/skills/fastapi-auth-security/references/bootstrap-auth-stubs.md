# Bootstrap Auth And Rate-Limit Stubs

Use this mode at project start when authentication and rate limiting must be wired early but hardening will happen later.

## Phase 1: Wiring First

- add auth dependency placeholders to all protected routes
- add rate-limit dependency placeholders to sensitive endpoints
- keep signatures stable so future hardening does not require route reshaping

Placeholder behavior policy:

- auth stub can temporarily allow pass-through in local/dev bootstrapping
- rate-limit stub can be no-op in early phase
- placeholder mode must be explicitly marked and tracked as debt

## Phase 2: Progressive Hardening

- replace auth pass-through with JWT validation and role checks
- replace no-op rate-limit dependency with real limiter policy
- enforce stricter dependencies on write and privileged routes first

## Phase 3: Validation

- verify protected routes are not accidentally left in pass-through mode
- verify auth and rate-limit dependencies are active in staging/production profiles
- verify unauthorized and throttled responses use consistent error contracts

## Guardrails

- do not leave placeholder auth enabled in production
- do not remove dependency wiring once introduced
- keep transition plan documented per endpoint group