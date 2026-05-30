from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TaskPatch(BaseModel):
    title: str | None = None
    version: int


@app.patch("/tasks/{task_id}")
async def patch_task(task_id: int, updates: TaskPatch):
    changes = updates.model_dump(exclude_unset=True)
    expected_version = changes.pop("version")

    # Replace this block with real database update:
    db_updated = False  # False means version mismatch in this sample.

    if not db_updated:
        raise HTTPException(status_code=409, detail="Conflict: resource was modified")

    return {"task_id": task_id, "updated": changes}
