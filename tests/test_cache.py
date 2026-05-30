import httpx
import pytest

from app.config import Settings
from app.services.http_client import ResilientHttpClient


@pytest.mark.asyncio
async def test_resilient_http_client_retries_and_succeeds() -> None:
    attempts = {"count": 0}

    def handler(_: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] < 3:
            return httpx.Response(status_code=503, json={"error": "transient"})
        return httpx.Response(status_code=200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as async_client:
        settings = Settings(http_retry_attempts=3, http_retry_backoff_seconds=0.0)
        client = ResilientHttpClient(client=async_client, settings=settings)
        payload = await client.get_json("https://example.com/resource")

    assert payload == {"ok": True}
    assert attempts["count"] == 3
