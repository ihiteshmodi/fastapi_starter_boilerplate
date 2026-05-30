import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI


class CredentialRefresher:
    def __init__(self, refresh_interval_seconds: int = 300) -> None:
        self._interval = refresh_interval_seconds
        self._task: asyncio.Task | None = None
        self.last_refresh_at: str | None = None

    async def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._task = asyncio.create_task(self._refresh_loop())

    async def stop(self) -> None:
        if not self._task:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass

    async def _refresh_loop(self) -> None:
        while True:
            await self._refresh_once()
            await asyncio.sleep(self._interval)

    async def _refresh_once(self) -> None:
        # Replace with your secret manager call and client rebind logic.
        self.last_refresh_at = datetime.now(timezone.utc).isoformat()


refresher = CredentialRefresher(refresh_interval_seconds=120)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await refresher.start()
    yield
    await refresher.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/ops/credentials")
async def credential_status():
    return {
        "refresh_task_running": bool(refresher._task and not refresher._task.done()),
        "last_refresh_at": refresher.last_refresh_at,
    }
