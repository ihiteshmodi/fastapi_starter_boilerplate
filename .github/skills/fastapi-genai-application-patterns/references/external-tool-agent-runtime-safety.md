# External Tool And Agent Runtime Safety

Use this policy when agents or orchestration layers call external tools.

## Runtime Safety Rules

1. Every tool call has a timeout envelope.
2. Every background task has done-callback error capture.
3. Every tool execution path uses explicit allowlists.
4. Every failure path has graceful degradation policy.

## Background Task Discipline

- fire-and-forget tasks must consume result in done callback
- log task exception with task identity
- avoid silent background failures

## Health Update Tasks

- report tool or server health status asynchronously
- include status, reason, timestamp, and hostname
- never block request path on health update write

## Graceful Degradation

When external tool fails:

- attempt bounded fallback route if configured
- return stable machine-readable error contract
- emit observability events for tool failure and fallback

## Anti-Patterns

- unbounded tool retries
- executing untrusted tool arguments without validation
- background tasks without exception consumption