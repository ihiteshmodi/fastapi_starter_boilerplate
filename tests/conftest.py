import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import Settings
from app.main import create_app


@pytest.fixture
def test_settings(tmp_path) -> Settings:
    return Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        jwt_secret_key="test-secret-key-with-minimum-thirty-two-bytes",
        auth_password_salt="test-salt",
        basic_username="basic_user",
        basic_password="basic_password",
        premium_username="premium_user",
        premium_password="premium_password",
        rate_limit_per_minute=50,
        login_rate_limit_per_minute=50,
        daily_quota_per_identity=500,
        opentelemetry_tracing_enabled=False,
        log_json=True,
    )


@pytest.fixture
def client(test_settings: Settings):
    app = create_app(custom_settings=test_settings)
    with TestClient(app) as test_client:
        yield test_client
