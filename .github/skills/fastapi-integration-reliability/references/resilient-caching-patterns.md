# Resilient Caching Patterns

Use this guide for cache correctness under load and partial upstream failure.

## Core Patterns

1. Lock-protected refresh:
- allow one refresher for an expired key
- serve cached value to concurrent callers when safe

2. Stale-on-failure fallback:
- if refresh fails and stale value exists, serve stale with observability marker
- fail only when no acceptable cached value exists

3. Invalidation cascade:
- invalidate dependent caches when source registry/config changes
- document dependency graph for cache entries

4. Versioned key naming:
- use namespaced keys like service:v2:resource:{id}

## Timeout And TTL Policy

- short TTL for volatile data
- longer TTL for expensive but stable data
- enforce refresh timeout to avoid request hanging

## Observability For Cache

Track:

- hit ratio
- miss ratio
- refresh success/failure
- stale served count
- refresh latency

## Safety Rules

- never treat stale data as fresh silently
- include fallback reason in logs/metrics
- avoid wildcard invalidation in hot paths