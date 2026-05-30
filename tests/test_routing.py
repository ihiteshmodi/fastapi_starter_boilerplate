from fastapi.testclient import TestClient


def _login(client: TestClient, username: str = "basic_user", password: str = "basic_password") -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    return body["access_token"]


def test_health_and_ready_endpoints(client: TestClient) -> None:
    health = client.get("/health")
    ready = client.get("/ready")

    assert health.status_code == 200
    assert ready.status_code == 200
    assert health.json() == {"status": "ok"}
    assert ready.json() == {"status": "ready"}


def test_login_and_protected_hello(client: TestClient) -> None:
    token = _login(client)
    response = client.get(
        "/api/v1/hello",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "basic_user"
    assert body["scope"] == "basic"


def test_protected_route_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/hello")
    assert response.status_code == 401


def test_invalid_credentials_return_consistent_message(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "basic_user", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
