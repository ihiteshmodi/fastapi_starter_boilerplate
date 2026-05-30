from typing import Any
import asyncio

import httpx
from fastapi import HTTPException, status

from app.config import Settings


class ResilientHttpClient:
    RETRIABLE_STATUS_CODES = {429, 500, 502, 503, 504}

    def __init__(self, *, client: httpx.AsyncClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def _sleep_before_retry(self, attempt: int) -> None:
        backoff = self._settings.http_retry_backoff_seconds * (2 ** (attempt - 1))
        await asyncio.sleep(backoff)

    async def get_json(self, url: str, *, params: dict[str, Any] | None = None) -> Any:
        attempts = max(1, self._settings.http_retry_attempts)

        for attempt in range(1, attempts + 1):
            try:
                response = await self._client.get(url, params=params, timeout=self._settings.http_timeout_seconds)
                response.raise_for_status()
                return response.json()
            except httpx.TimeoutException as exc:
                if attempt < attempts:
                    await self._sleep_before_retry(attempt)
                    continue
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="Upstream timeout",
                ) from exc
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in self.RETRIABLE_STATUS_CODES and attempt < attempts:
                    await self._sleep_before_retry(attempt)
                    continue
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Upstream returned an error",
                ) from exc
            except httpx.TransportError as exc:
                if attempt < attempts:
                    await self._sleep_before_retry(attempt)
                    continue
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed reaching upstream",
                ) from exc

        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Upstream failure")
