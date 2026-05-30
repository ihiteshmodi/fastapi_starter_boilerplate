# Multi-App Composition And Mounted Sub-Apps

Use this pattern when a single host FastAPI service composes multiple sub-apps (FastAPI or MCP-compatible).

## Why Use It

- isolate domain-specific serving interfaces
- scale and deploy sub-capabilities independently when needed
- keep host app thin and orchestration-focused

## Composition Rules

1. Define one host app as the mount root.
2. Mount sub-apps under versioned path prefixes.
3. Keep mount names stable and descriptive.
4. Use one shared lifecycle orchestrator for startup and teardown.

## Mount Path Convention

Recommended:

- /api/v1/<domain>/
- /mcp/v1/<capability>/
- /sub-agent/v1/<capability>/

Versioning rule:

- version in path, not only in docs
- breaking changes require new path version

## Shared Lifespan Orchestration

- use one combined lifespan with AsyncExitStack
- enter each sub-app lifespan in a deterministic order
- close in reverse order automatically
- fail host startup if critical sub-app init fails

## Operational Checks

- each sub-app exposes health or readiness signal
- host app readiness reflects critical sub-app readiness
- route-level auth and rate limits remain explicit per mounted surface