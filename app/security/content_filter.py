from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
import time

import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import Settings


@dataclass
class CounterWindow:
    window_start: float
    count: int


@dataclass
class DailyCounter:
    day: str
    count: int


class RateLimitQuotaMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, settings: Settings):
        super().__init__(app)
        self._settings = settings
        self._minute_counters: dict[str, CounterWindow] = {}
        self._daily_counters: dict[str, DailyCounter] = {}
        self._throttle_events: defaultdict[str, int] = defaultdict(int)

    def _identity_key(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            try:
                payload = jwt.decode(
                    token,
                    self._settings.jwt_secret_key,
                    algorithms=[self._settings.jwt_algorithm],
                    options={"verify_exp": False},
                )
                sub = payload.get("sub")
                if isinstance(sub, str) and sub:
                    return f"user:{sub}"
            except Exception:
                pass

        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    def _minute_limit_for_path(self, path: str) -> int:
        if path.startswith(f"{self._settings.api_prefix}/auth/login"):
            return max(1, self._settings.login_rate_limit_per_minute)
        return max(1, self._settings.rate_limit_per_minute)

    def _check_minute_limit(self, identity: str, path: str) -> tuple[bool, int, int, int]:
        now = time.time()
        window_key = f"{identity}:{path}"
        limit = self._minute_limit_for_path(path)
        record = self._minute_counters.get(window_key)

        if record is None or now - record.window_start >= 60:
            record = CounterWindow(window_start=now, count=0)

        record.count += 1
        self._minute_counters[window_key] = record

        remaining = max(0, limit - record.count)
        reset = int(max(0, 60 - (now - record.window_start)))
        allowed = record.count <= limit
        return allowed, limit, remaining, reset

    def _check_daily_quota(self, identity: str) -> tuple[bool, int, int]:
        today = datetime.now(UTC).date().isoformat()
        limit = max(1, self._settings.daily_quota_per_identity)
        current = self._daily_counters.get(identity)

        if current is None or current.day != today:
            current = DailyCounter(day=today, count=0)

        current.count += 1
        self._daily_counters[identity] = current

        remaining = max(0, limit - current.count)
        allowed = current.count <= limit
        return allowed, limit, remaining

    def _attach_headers(self, response: Response, *, limit: int, remaining: int, reset: int, quota_limit: int, quota_remaining: int) -> None:
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset)
        response.headers["X-Quota-Limit"] = str(quota_limit)
        response.headers["X-Quota-Remaining"] = str(quota_remaining)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/health", "/ready"}:
            return await call_next(request)

        identity = self._identity_key(request)
        minute_allowed, limit, remaining, reset = self._check_minute_limit(identity, request.url.path)
        quota_allowed, quota_limit, quota_remaining = self._check_daily_quota(identity)

        if not minute_allowed:
            self._throttle_events[identity] += 1
            response = JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
            self._attach_headers(
                response,
                limit=limit,
                remaining=remaining,
                reset=reset,
                quota_limit=quota_limit,
                quota_remaining=quota_remaining,
            )
            return response

        if not quota_allowed:
            self._throttle_events[identity] += 1
            response = JSONResponse(status_code=429, content={"detail": "Daily quota exceeded"})
            self._attach_headers(
                response,
                limit=limit,
                remaining=remaining,
                reset=reset,
                quota_limit=quota_limit,
                quota_remaining=quota_remaining,
            )
            return response

        response = await call_next(request)
        self._attach_headers(
            response,
            limit=limit,
            remaining=remaining,
            reset=reset,
            quota_limit=quota_limit,
            quota_remaining=quota_remaining,
        )
        return response
