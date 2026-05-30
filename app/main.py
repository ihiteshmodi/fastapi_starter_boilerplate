from contextlib import asynccontextmanager
from typing import Annotated
import logging
import time
import uuid

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.observability.feedback import clear_request_id, configure_logging, set_request_id
from app.observability.tracer import configure_telemetry
from app.schemas import HelloResponse, LoginRequest, Principal, TokenResponse
from app.security.content_filter import RateLimitQuotaMiddleware
from app.security.input_guard import require_basic_or_premium
from app.security.output_filter import install_error_handlers
from app.services.auth_service import AuthenticationError, authenticate
from app.services.migrations import run_migrations
from app.services.memory_service import create_session_factory, seed_demo_users

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings

    run_migrations(settings.database_url)
    app.state.db_session_factory = create_session_factory(settings.database_url)
    seed_demo_users(
        app.state.db_session_factory,
        basic_username=settings.basic_username,
        basic_password=settings.basic_password,
        premium_username=settings.premium_username,
        premium_password=settings.premium_password,
        salt=settings.auth_password_salt,
    )

    async with httpx.AsyncClient() as http_client:
        app.state.http_client = http_client
        yield


def create_app(custom_settings: Settings | None = None) -> FastAPI:
    settings = custom_settings or get_settings()
    configure_logging(settings)

    app = FastAPI(title="Starter Boilerplate API", version="0.1.0", lifespan=lifespan)
    app.state.settings = settings

    app.add_middleware(RateLimitQuotaMiddleware, settings=settings)
    configure_telemetry(app, settings)
    install_error_handlers(app)

    @app.middleware("http")
    async def request_logging(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        set_request_id(request_id)
        started = time.perf_counter()

        logger.info(
            "request_start",
            extra={"request_id": request_id, "method": request.method, "path": request.url.path},
        )

        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            logger.exception(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": elapsed_ms,
                },
            )
            clear_request_id()
            raise

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request_complete",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": elapsed_ms,
            },
        )
        clear_request_id()
        return response

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", tags=["health"])
    def ready() -> dict[str, str]:
        return {"status": "ready"}

    @app.post(f"{settings.api_prefix}/auth/login", response_model=TokenResponse)
    def login(payload: LoginRequest, request: Request) -> TokenResponse:
        session_factory = request.app.state.db_session_factory
        session: Session = session_factory()
        try:
            token = authenticate(
                username=payload.username,
                password=payload.password,
                session=session,
                settings=request.app.state.settings,
            )
            logger.info("auth_success", extra={"username": payload.username})
            return TokenResponse(access_token=token)
        except AuthenticationError as exc:
            logger.info("auth_failed", extra={"username": payload.username})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        finally:
            session.close()

    @app.get(f"{settings.api_prefix}/hello", response_model=HelloResponse)
    def hello(current_user: Annotated[Principal, Depends(require_basic_or_premium)]) -> HelloResponse:
        return HelloResponse(
            message="Hello from starter boilerplate",
            username=current_user.username,
            scope=current_user.scope,
        )

    @app.get(f"{settings.api_prefix}/me", response_model=Principal)
    def me(current_user: Annotated[Principal, Depends(require_basic_or_premium)]) -> Principal:
        return current_user

    return app


app = create_app()
