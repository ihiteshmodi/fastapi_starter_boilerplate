---
name: fastapi-release-gates
description: Apply final pre-deploy and go-live checks for FastAPI services, including security, database, health, and documentation readiness. Use when users ask for deployment readiness, launch checklist, or production gates.
argument-hint: [release-goal] [environment]
---

# FastAPI Release Gates

## Scope

Covers canonical rules C28-C30.

## Workflow

1. Run pre-deploy audit checks.
2. Run pre-flight go-live checks.
3. Validate health endpoint and migration status.
4. Confirm secret handling and HTTPS policy.
5. Validate README quality contract.

## Guardrails

1. Do not ship with debug prints or hardcoded secrets.
2. Do not ship without migration and rollback plan clarity.
3. Do not treat README as optional for generated projects.

## Trigger Examples

Should trigger:

- "Run final pre-deploy and pre-flight checks for this FastAPI service."
- "Review PR readiness for auth hardening, offloading, and reliability."

Paraphrased should trigger:

- "Is this backend ready to go live in production?"

Should not trigger:

- "Design a prompt registry and LLM tool planner."
- "Implement retry middleware for outbound HTTP clients."

## Additional Resources

- Pre-deploy audit checklist: [references/pre-deploy-audit.md](references/pre-deploy-audit.md)
- Pre-flight checklist: [references/pre-flight-checklist.md](references/pre-flight-checklist.md)
- Implementation review checklist: [references/implementation-review-checklist.md](references/implementation-review-checklist.md)
- README contract: [references/readme-contract.md](references/readme-contract.md)
- Matrix mapping: [../normalized-instruction-matrix.md](../normalized-instruction-matrix.md)

## Validation Expectations

1. Release output includes pre-deploy, pre-flight, and migration readiness checks.
2. Security and transport checks explicitly cover secret handling and HTTPS policy.
3. Output format must include pass/fail status per gate with blocking issues called out.
4. Edge-case handling for rollback readiness and partial gate failures is documented.
5. Recovery guidance explains remediation order before re-running go-live checks.