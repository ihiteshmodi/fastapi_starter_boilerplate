from uuid import uuid4

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

TASK_STATE: dict[str, dict] = {}


class InferenceRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


def run_inference_task(task_id: str, text: str) -> None:
    try:
        # Replace with queue worker or process-pool execution in production.
        result = text.upper()
        TASK_STATE[task_id] = {"status": "completed", "result": result}
    except Exception as exc:
        TASK_STATE[task_id] = {"status": "failed", "error": str(exc)}


@app.post("/inference", status_code=202)
async def start_inference(payload: InferenceRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    TASK_STATE[task_id] = {"status": "queued"}
    background_tasks.add_task(run_inference_task, task_id, payload.text)
    return {"task_id": task_id, "status": "queued"}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in TASK_STATE:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, **TASK_STATE[task_id]}
