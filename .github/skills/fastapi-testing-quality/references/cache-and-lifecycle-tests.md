# Cache And Lifecycle Test Patterns

Add these tests for production reliability.

## Cache Tests

- stale fallback when refresh fails
- lock-protected single refresh behavior under concurrency
- invalidation cascade after source changes
- cache key versioning compatibility

## Lifecycle Tests

- app startup initializes required clients and pools
- app teardown disposes clients and pools cleanly
- mounted sub-app lifespan startup and teardown ordering

## Integration Test Focus

- mount-level route availability
- readiness behavior when one critical sub-app fails to initialize
- timeout and retry behavior for external dependencies

## CI Rule

At least one cache resilience test and one lifecycle teardown test must run in CI for GenAI services.