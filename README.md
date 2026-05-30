# Starter Boilerplate

FastAPI boilerplate with production-first defaults:

- App factory + lifespan wiring
- Structured JSON logging with request IDs and redaction
- Global error handling contracts
- JWT login + protected routes
- Rate limiting and daily quota middleware
- Resilient outbound HTTP client (timeout + retry)
- Canonical GenAI-ready folder structure from skill guidance

## Quick Start

```bash
export SSL_CERT_FILE='/Users/hitesh.modi/Desktop/Kinda Personal/Backend Projects/caadmin.netskope.com.pem'
uv sync
uv run uvicorn app.main:app --reload
```

## Demo Credentials

- basic user: `basic_user` / `basic_password`
- premium user: `premium_user` / `premium_password`

## Endpoints

- `GET /health`
- `GET /ready`
- `POST /api/v1/auth/login`
- `GET /api/v1/hello` (protected)
- `GET /api/v1/me` (protected)

## Run Tests

```bash
export SSL_CERT_FILE='/Users/hitesh.modi/Desktop/Kinda Personal/Backend Projects/caadmin.netskope.com.pem'
uv run pytest -q
```

## Notes

- OpenTelemetry is feature-gated via environment config.
- Rate limiting is identity-aware:
	- user identity for valid bearer token requests
	- client IP fallback for unauthenticated requests
