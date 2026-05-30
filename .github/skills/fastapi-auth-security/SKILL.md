---
name: fastapi-auth-security
description: Implement FastAPI authentication, authorization, protected dependency chains, and security-safe error handling. Use when users ask for JWT login/register flows, protected routes, role checks, or auth hardening.
argument-hint: [auth-goal] [constraints]
---

# FastAPI Auth Security

## Scope

Covers canonical rules C05, C07, C22, C23 and security portions of C19.

## Workflow

1. Add auth dependency placeholders to protected route signatures from day zero.
2. Add placeholder rate-limit dependencies for sensitive routes from day zero.
3. Build app features while keeping placeholder dependencies attached.
4. Implement JWT register/login/protected-user flow.
5. Enforce role checks using dependency factories.
6. Set token expiry and strong secret policy.
7. Return generic auth failure messages to prevent enumeration.

## Guardrails

1. Never log raw tokens, credentials, or secret keys.
2. Keep auth failures user-safe and non-revealing.
3. Keep permission logic explicit at route boundary or dependency layer.
4. Do not ship production environments with pass-through auth stubs.

## Trigger Examples

Should trigger:

- "Add JWT auth and protect profile routes."
- "Wire auth and rate-limit placeholders first, then harden later."

Paraphrased should trigger:

- "Set up login, token validation, and role checks in FastAPI."

Should not trigger:

- "Tune PostgreSQL indexing strategy."
- "Build a React navigation bar."

## Additional Resources

- JWT baseline flow: [references/jwt-baseline.md](references/jwt-baseline.md)
- Bootstrap auth and rate-limit stubs: [references/bootstrap-auth-stubs.md](references/bootstrap-auth-stubs.md)
- Security checklist: [references/security-checklist.md](references/security-checklist.md)
- FastAPI official security and JWT links: [references/fastapi-official-security-jwt-links.md](references/fastapi-official-security-jwt-links.md)
- Example protected route: [examples/jwt-protected-route.py](examples/jwt-protected-route.py)
- Example OAuth2 JWT flow: [examples/oauth2-jwt-password-flow.py](examples/oauth2-jwt-password-flow.py)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. JWT register/login/protected-route flow is explicitly defined with token expiry and secret policy.
2. Protected routes enforce auth dependency and role-check boundaries instead of inline route logic.
3. Output format must include auth contract summary, failure response policy, and hardening checklist.
4. Edge-case behavior for invalid, expired, and malformed tokens is documented with non-enumerating errors.
5. Recovery guidance states how to move from placeholder mode to hardened production auth.