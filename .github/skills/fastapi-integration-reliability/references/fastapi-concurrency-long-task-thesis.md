# FastAPI Concurrency And Long-Task Thesis

## Core Mental Model

FastAPI is a traffic controller:

1. Accept request.
2. Validate input.
3. Route to execution path.

FastAPI is not the place to do heavy compute directly in request handlers.

## Async Policy

- async is non-blocking I/O, not automatically faster Python
- use async def for I/O-bound work
- do not run CPU-heavy inference directly inside async route handlers

One blocking call in an async request path can reduce concurrency for everyone.

## CPU-Heavy Work Policy

For expensive ML inference:

- offload to worker systems or process pools
- keep request thread/event-loop path short
- prefer task orchestration patterns over long synchronous waits

## Long Task API Contract

If processing is long-running:

- return 202 Accepted quickly
- return a task_id
- expose status endpoint for polling
- keep task execution in background workers or managed background job system

## Validation Policy

Validation is a guardrail, not optional styling:

- reject malformed payloads early
- enforce payload bounds in schema and middleware
- fail fast before expensive work starts

## Load-Failure First Questions

Design for failure under load from day one:

- what blocks the event loop first?
- when do DB/HTTP pools saturate?
- what is the timeout path for dependencies?
- what fallback exists when worker queue lags?

## Database/Client Compatibility

Use async-compatible clients for async route paths.

Examples:

- async DB drivers
- async HTTP clients

Avoid mixing sync clients inside async request flows.

## Response Design Rule

If latency cannot meet interactive SLA:

- switch to async job contract (202 + task_id)
- do not fake real-time by holding client connections open unnecessarily