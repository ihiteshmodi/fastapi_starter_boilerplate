# FastAPI Starter Boilerplate For Secure APIs

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-tests%20passing-brightgreen)
![License](https://img.shields.io/badge/license-template-lightgrey)

> A production-first FastAPI starter with JWT auth, bcrypt password hashing, structured logging, Alembic migrations, and rate limit plus quota middleware.

## Quick Start

```bash
cd starter_boilerplate
export SSL_CERT_FILE='/Users/hitesh.modi/Desktop/Kinda Personal/Backend Projects/caadmin.netskope.com.pem'
uv sync && uv run python scripts/migrate.py && uv run python scripts/seed.py
uv run uvicorn app.main:app --reload
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok"}
```

## Usage Examples

### Login And Get JWT

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
	-H 'Content-Type: application/json' \
	-d '{"username":"basic_user","password":"basic_password"}'

# Expected response:
# {"access_token":"<jwt>","token_type":"bearer"}
```

### Access Protected Route

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
	-H 'Content-Type: application/json' \
	-d '{"username":"premium_user","password":"premium_password"}' | jq -r .access_token)

curl http://127.0.0.1:8000/api/v1/hello \
	-H "Authorization: Bearer ${TOKEN}"

# Expected response:
# {"message":"Hello from starter boilerplate","username":"premium_user","scope":"premium"}
```

### Python Client Example

```python
import httpx

base_url = "http://127.0.0.1:8000"

login = httpx.post(
		f"{base_url}/api/v1/auth/login",
		json={"username": "basic_user", "password": "basic_password"},
		timeout=10,
)
login.raise_for_status()
token = login.json()["access_token"]

profile = httpx.get(
		f"{base_url}/api/v1/me",
		headers={"Authorization": f"Bearer {token}"},
		timeout=10,
)
profile.raise_for_status()
print(profile.json())
# {"username": "basic_user", "scope": "basic"}
```

## Configuration

Create a `.env` file if you want to override defaults.

| Variable | Description | Default | Required |
|---|---|---|---|
| `APP_NAME` | Service name | `starter-boilerplate` | No |
| `APP_ENV` | Runtime environment (local/staging/prod) | `local` | No |
| `DEBUG` | Debug flag | `false` | No |
| `API_PREFIX` | API base prefix | `/api/v1` | No |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./starter.db` | No |
| `JWT_SECRET_KEY` | JWT signing key | `replace-in-production` | Yes (for real deployments) |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` | No |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry (minutes) | `60` | No |
| `AUTH_PASSWORD_SALT` | Salt used before bcrypt hashing | `starter-salt` | No |
| `BASIC_USERNAME` | Seeded basic username | `basic_user` | No |
| `BASIC_PASSWORD` | Seeded basic password | `basic_password` | No |
| `PREMIUM_USERNAME` | Seeded premium username | `premium_user` | No |
| `PREMIUM_PASSWORD` | Seeded premium password | `premium_password` | No |
| `LOG_LEVEL` | Logging verbosity | `INFO` | No |
| `LOG_JSON` | Enable JSON logs | `true` | No |
| `LOG_SERVICE_NAME` | Service label in logs | `starter-boilerplate` | No |
| `OPENTELEMETRY_TRACING_ENABLED` | Enable OpenTelemetry | `false` | No |
| `OPENTELEMETRY_SERVICE_NAME` | OTEL service name | `starter-boilerplate` | No |
| `OPENTELEMETRY_OTLP_ENDPOINT` | OTLP endpoint | `http://localhost:4317` | No |
| `OPENTELEMETRY_OTLP_INSECURE` | OTLP insecure transport | `true` | No |
| `HTTP_TIMEOUT_SECONDS` | External call timeout | `10.0` | No |
| `HTTP_RETRY_ATTEMPTS` | External call retries | `3` | No |
| `HTTP_RETRY_BACKOFF_SECONDS` | Retry backoff base seconds | `0.2` | No |
| `RATE_LIMIT_PER_MINUTE` | Global per-minute limit | `60` | No |
| `LOGIN_RATE_LIMIT_PER_MINUTE` | Login per-minute limit | `10` | No |
| `DAILY_QUOTA_PER_IDENTITY` | Daily request quota per identity | `1000` | No |

### Example .env

```bash
APP_ENV=local
DATABASE_URL=sqlite:///./starter.db
JWT_SECRET_KEY=replace-with-32-byte-or-longer-secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
RATE_LIMIT_PER_MINUTE=60
LOGIN_RATE_LIMIT_PER_MINUTE=10
```

## API Reference

### Health

#### GET /health

**Response (200):**

```json
{"status":"ok"}
```

### Authentication

#### POST /api/v1/auth/login

Authenticate username/password and return JWT.

**Request:**

```json
{
	"username": "basic_user",
	"password": "basic_password"
}
```

**Response (200):**

```json
{
	"access_token": "<jwt>",
	"token_type": "bearer"
}
```

**Errors:**

- `401`: Invalid credentials
- `429`: Rate limit exceeded
- `429`: Daily quota exceeded

### Protected APIs

#### GET /api/v1/hello

Returns greeting and current user context.

**Headers:**

- `Authorization: Bearer <token>`

**Response (200):**

```json
{
	"message": "Hello from starter boilerplate",
	"username": "basic_user",
	"scope": "basic"
}
```

**Errors:**

- `401`: Invalid or missing token
- `403`: Unauthorized scope

#### GET /api/v1/me

Returns current authenticated principal.

**Headers:**

- `Authorization: Bearer <token>`

**Response (200):**

```json
{
	"username": "basic_user",
	"scope": "basic"
}
```

**Errors:**

- `401`: Invalid or missing token
- `403`: Unauthorized scope

## Operations

### Run tests

```bash
export SSL_CERT_FILE='/Users/hitesh.modi/Desktop/Kinda Personal/Backend Projects/caadmin.netskope.com.pem'
uv run pytest -q
```

### Alembic

- Migration config: `alembic.ini`
- Migration environment: `alembic/env.py`
- Revision scripts: `alembic/versions/`
- App startup runs `upgrade head` before seeding users.

## Notes

- OpenTelemetry is feature-gated via environment config.
- Rate limiting is identity-aware:
	- user identity for valid bearer token requests
	- client IP fallback for unauthenticated requests
