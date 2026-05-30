# Resilient Background Task Manager Pattern

Use this when requests must return quickly while work continues in background workers.

## Why This Pattern

- avoids blocking request handlers
- keeps bounded queue pressure under control
- exposes operational status for health and debugging
- captures failures into machine-readable job state

## Core Design

1. Accept request and return 202 with job_id.
2. Enqueue work into a bounded queue.
3. Run worker loops started in app lifespan.
4. Track state transitions: queued -> running -> completed or failed.
5. Expose status endpoint for operators and clients.

## FastAPI Example

See: ../examples/resilient-background-task-manager.py

## Production Notes

- replace in-memory state with Redis or database
- add retention policy for completed jobs
- add idempotency key for duplicate submissions
- add per-tenant queue controls when multi-tenant
