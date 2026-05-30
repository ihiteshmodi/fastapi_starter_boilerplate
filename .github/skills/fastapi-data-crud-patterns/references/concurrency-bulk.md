# Concurrency and Bulk

Concurrency policy:

- Use optimistic version field checks for contested updates.
- Return 409 conflict on stale update attempts.

Bulk policy:

- Define max batch size.
- Run bulk write flows in transaction chunks.
- Define all-or-nothing vs partial-failure behavior explicitly.
- Report per-item failures if partial success is allowed.