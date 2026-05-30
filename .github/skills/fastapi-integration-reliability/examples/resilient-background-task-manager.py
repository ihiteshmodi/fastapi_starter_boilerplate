import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


@dataclass
class Job:
    job_id: str
    payload: str


class BackgroundJobManager:
    def __init__(self, worker_count: int = 2, max_queue_size: int = 100) -> None:
        self._queue: asyncio.Queue[Job] = asyncio.Queue(maxsize=max_queue_size)
        self._workers: list[asyncio.Task] = []
        self._worker_count = worker_count
        self._shutdown = asyncio.Event()
        self.state: dict[str, dict[str, Any]] = {}

    async def start(self) -> None:
        for idx in range(self._worker_count):
            self._workers.append(asyncio.create_task(self._worker_loop(idx)))

    async def stop(self) -> None:
        self._shutdown.set()
        for _ in self._workers:
            await self._queue.put(Job(job_id="__shutdown__", payload=""))
        await asyncio.gather(*self._workers, return_exceptions=True)

    async def submit(self, payload: str) -> str:
        if self._queue.full():
            raise RuntimeError("Queue is full")

        job_id = str(uuid4())
        self.state[job_id] = {
            "status": "queued",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await self._queue.put(Job(job_id=job_id, payload=payload))
        return job_id

    async def _worker_loop(self, worker_id: int) -> None:
        while not self._shutdown.is_set():
            job = await self._queue.get()
            try:
                if job.job_id == "__shutdown__":
                    return

                self.state[job.job_id]["status"] = "running"
                self.state[job.job_id]["worker_id"] = worker_id

                # Replace with CPU/process pool or external queue worker in production.
                await asyncio.sleep(0.2)
                result = job.payload.upper()

                self.state[job.job_id].update(
                    {
                        "status": "completed",
                        "result": result,
                        "finished_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except Exception as exc:
                self.state[job.job_id].update(
                    {
                        "status": "failed",
                        "error": str(exc),
                        "finished_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
            finally:
                self._queue.task_done()


class JobRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


manager = BackgroundJobManager(worker_count=2, max_queue_size=100)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.start()
    yield
    await manager.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/jobs", status_code=202)
async def create_job(payload: JobRequest):
    try:
        job_id = await manager.submit(payload.text)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = manager.state.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, **job}


@app.get("/ops/background-jobs")
async def get_background_status():
    queued_count = sum(1 for j in manager.state.values() if j["status"] == "queued")
    running_count = sum(1 for j in manager.state.values() if j["status"] == "running")
    failed_count = sum(1 for j in manager.state.values() if j["status"] == "failed")
    return {
        "queue_depth": manager._queue.qsize(),
        "jobs_total": len(manager.state),
        "jobs_queued": queued_count,
        "jobs_running": running_count,
        "jobs_failed": failed_count,
    }
