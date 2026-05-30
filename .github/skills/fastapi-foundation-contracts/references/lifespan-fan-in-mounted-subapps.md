# Lifespan Fan-in for Mounted Sub-apps

Use this when one gateway app mounts many FastAPI sub-apps and each sub-app has its own startup and shutdown resources.

## Why This Pattern

- centralizes startup and shutdown sequencing
- avoids missing sub-app initialization in multi-worker deployments
- makes mounted app lifecycle behavior explicit and testable

## Core Design

1. Create sub-apps normally.
2. In parent app lifespan, open an AsyncExitStack.
3. Enter each sub-app lifespan context through the stack.
4. Yield once all sub-app resources are ready.
5. Let AsyncExitStack tear down all sub-apps cleanly on shutdown.

## FastAPI Example

See: ../examples/lifespan-fan-in-mounted-subapps.py

## Production Notes

- keep mount list and lifespan entries in sync
- log startup and shutdown boundaries per sub-app
- fail fast on critical sub-app startup errors
