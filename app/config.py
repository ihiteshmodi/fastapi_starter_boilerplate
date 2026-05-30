from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "starter-boilerplate"
    app_env: str = "local"
    debug: bool = False

    api_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./starter.db"

    jwt_secret_key: str = Field(default="replace-in-production")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    auth_password_salt: str = "starter-salt"

    basic_username: str = "basic_user"
    basic_password: str = "basic_password"
    premium_username: str = "premium_user"
    premium_password: str = "premium_password"

    log_level: str = "INFO"
    log_json: bool = True
    log_service_name: str = "starter-boilerplate"

    opentelemetry_tracing_enabled: bool = False
    opentelemetry_service_name: str = "starter-boilerplate"
    opentelemetry_otlp_endpoint: str = "http://localhost:4317"
    opentelemetry_otlp_insecure: bool = True

    http_timeout_seconds: float = 10.0
    http_retry_attempts: int = 3
    http_retry_backoff_seconds: float = 0.2

    rate_limit_per_minute: int = 60
    login_rate_limit_per_minute: int = 10
    daily_quota_per_identity: int = 1000


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
