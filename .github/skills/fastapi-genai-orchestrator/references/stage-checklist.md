# Stage Checklist

1. Foundation complete:
- settings and env policy defined
- status and error contract defined

2. Security baseline complete:
- protected dependencies attached
- placeholder auth/rate-limit stubs attached where needed
- JWT and permission policy established

3. Data semantics complete:
- CRUD status contracts
- transactions and optimistic locking policy

4. Reliability complete:
- timeout/retry and resource lifecycle rules

5. Testing complete:
- unit and integration tests for important logic

6. Observability complete:
- request IDs, structured logs, metrics/traces, alerts

7. Release gate complete:
- pre-deploy and pre-flight checklists passed
- implementation review checklist passed (auth hardening, offloading, blocking checks)