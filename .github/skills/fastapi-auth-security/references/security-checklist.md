# Security Checklist

- Secrets loaded from environment only.
- CORS policy differs by environment profile.
- Debug mode disabled in production.
- Sensitive fields excluded from response models.
- Token lifetimes and refresh policy documented.
- Auth and refresh routes have stricter rate limits.
- Exception payloads do not leak internal traces in production.