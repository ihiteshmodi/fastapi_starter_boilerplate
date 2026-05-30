import logging

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.observability.feedback import JsonLogFormatter


def test_request_id_header_present(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_rate_limit_enforced(tmp_path) -> None:
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'limit.db'}",
        jwt_secret_key="test-secret-key-with-minimum-thirty-two-bytes",
        auth_password_salt="test-salt",
        rate_limit_per_minute=2,
        login_rate_limit_per_minute=10,
        daily_quota_per_identity=100,
    )

    app = create_app(custom_settings=settings)
    with TestClient(app) as local_client:
        first = local_client.get("/ready")
        second = local_client.get("/api/v1/me")
        third = local_client.get("/api/v1/me")
        fourth = local_client.get("/api/v1/me")

    assert first.status_code == 200
    assert second.status_code in {401, 403}
    assert third.status_code in {401, 403}
    assert fourth.status_code == 429
    assert fourth.json()["detail"] in {"Rate limit exceeded", "Daily quota exceeded"}


def test_daily_quota_enforced(tmp_path) -> None:
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'quota.db'}",
        jwt_secret_key="test-secret-key-with-minimum-thirty-two-bytes",
        auth_password_salt="test-salt",
        rate_limit_per_minute=100,
        login_rate_limit_per_minute=100,
        daily_quota_per_identity=2,
    )

    app = create_app(custom_settings=settings)
    with TestClient(app) as local_client:
        first = local_client.post("/api/v1/auth/login", json={"username": "basic_user", "password": "basic_password"})
        second = local_client.post("/api/v1/auth/login", json={"username": "basic_user", "password": "basic_password"})
        third = local_client.post("/api/v1/auth/login", json={"username": "basic_user", "password": "basic_password"})

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 429
    assert third.json()["detail"] == "Daily quota exceeded"


def test_json_formatter_redacts_sensitive_fields() -> None:
    formatter = JsonLogFormatter(service_name="test", environment="test")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="event",
        args=(),
        exc_info=None,
    )
    record.api_key = "secret-key"
    record.payload = {"password": "abc123", "safe": "ok"}

    rendered = formatter.format(record)
    assert "secret-key" not in rendered
    assert "abc123" not in rendered
    assert "[REDACTED]" in rendered
