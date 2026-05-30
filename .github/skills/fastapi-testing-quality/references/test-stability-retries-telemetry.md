# Test Stability: Neutralize Retries and Clean Telemetry

Use this for production-grade test suites where retries and tracing are enabled in app runtime.

## Problem

- Retry decorators add real sleep delays in failing-path tests.
- Telemetry exporters may keep background workers alive during test teardown.
- Combined, these make CI slow and flaky.

## Pattern

1. In tests, patch retry wait strategy to no-wait.
2. Initialize a test tracer provider once per session.
3. Shut down tracer provider cleanly at session end.

## Benefits

- faster test runtime
- fewer teardown warnings
- deterministic failure-path assertions

## Example

See: ../examples/test-stability-retry-and-telemetry.py

## Notes

- Keep this behavior in tests only.
- Do not change production retry/backoff policy for test speed.
