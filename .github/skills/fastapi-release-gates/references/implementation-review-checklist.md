# Implementation Review Checklist

Use this checklist before creating or approving a PR for FastAPI plus GenAI app changes.

## Security Wiring Review

- protected routes were tagged and dependency-wired from early scaffolding
- placeholder auth or rate-limit stubs are either hardened or explicitly tracked
- no production profile uses pass-through auth behavior

## Concurrency And Offloading Review

- CPU-heavy ML inference is offloaded to worker/process-pool path
- long-running endpoints use 202 plus task_id contract
- task status endpoint exists and uses stable response schema
- async routes avoid sync DB/HTTP calls

## Reliability Review

- outbound calls have timeout and typed failure mapping
- retries are bounded and only for transient cases
- fallback behavior is explicit and observable

## Performance And Stability Review

- payload limits enforced for high-risk routes
- connection pool limits and exhaustion behavior reviewed
- blocking hotspots identified and addressed

## Contract And Testing Review

- response and error contracts remain consistent
- critical path tests include failure and load-relevant paths
- lifecycle and cache resilience tests are present where applicable

## Decision

- approve
- approve with follow-up tasks
- request changes