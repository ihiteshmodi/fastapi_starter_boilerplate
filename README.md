# Starter Boilerplate

FastAPI boilerplate with production-first defaults:

- App factory + lifespan wiring
- Structured JSON logging with request IDs and redaction
- Global error handling contracts
- JWT login + protected routes
- Rate limiting and daily quota middleware
- Resilient outbound HTTP client (timeout + retry)
- Alembic-managed database migrations
- Canonical GenAI-ready folder structure from skill guidance

## Step-by-Step Usage

### 1. Open project and install dependencies

```bash
export SSL_CERT_FILE='/Users/hitesh.modi/Desktop/Kinda Personal/Backend Projects/caadmin.netskope.com.pem'
uv sync
```

### 2. Apply database migrations (Alembic)

```bash
uv run python scripts/migrate.py
```

### 3. Seed demo users

```bash
uv run python scripts/seed.py
```

### 4. Start the API

```bash
uv run uvicorn app.main:app --reload
```

### 5. Validate health endpoints

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
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

## Auth Flow Example

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
	-H 'Content-Type: application/json' \
	-d '{"username":"basic_user","password":"basic_password"}' | jq -r .access_token)

curl http://127.0.0.1:8000/api/v1/hello -H "Authorization: Bearer ${TOKEN}"
```

## Run Tests

```bash
export SSL_CERT_FILE='/Users/hitesh.modi/Desktop/Kinda Personal/Backend Projects/caadmin.netskope.com.pem'
uv run pytest -q
```

## Alembic Notes

- Migration config: `alembic.ini`
- Migration environment: `alembic/env.py`
- Revision scripts: `alembic/versions/`
- App startup runs `upgrade head` before seeding users.

## Skill Alignment Checklist

### fastapi-foundation-contracts

- Environment-driven config and secret loading in `app/config.py`
- Lifespan app setup in `app/main.py`
- Consistent status and error handling via global exception handlers in `app/security/output_filter.py`

### structured-instructions: API and feature implementation

- Robust API fetching pattern with timeout, raise_for_status, retries in `app/services/http_client.py`
- Route protection and baseline endpoint contracts in `app/main.py` and `app/security/input_guard.py`

### structured-instructions: error handling, logging, observability

- Structured JSON logging + request IDs + redaction in `app/observability/feedback.py`
- OpenTelemetry feature gate in `app/observability/tracer.py`

### structured-instructions: authentication and security

- JWT login and protected routes in `app/main.py`
- Consistent invalid credential messaging in auth flow
- Scope-based route authorization in `app/security/input_guard.py`

### Additional requested baseline

- Rate limiting and daily quota middleware in `app/security/content_filter.py`

## Notes

- OpenTelemetry is feature-gated via environment config.
- Rate limiting is identity-aware:
	- user identity for valid bearer token requests
	- client IP fallback for unauthenticated requests
