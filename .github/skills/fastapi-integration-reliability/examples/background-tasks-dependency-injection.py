from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, status

app = FastAPI()
audit_log: list[str] = []


def write_log(message: str) -> None:
    audit_log.append(message)


def add_query_audit(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"query={q}")
    return q


@app.post("/process/{item_id}", status_code=status.HTTP_202_ACCEPTED)
async def process_item(
    item_id: str,
    background_tasks: BackgroundTasks,
    q: Annotated[str | None, Depends(add_query_audit)],
):
    background_tasks.add_task(write_log, f"process item={item_id}")
    return {"item_id": item_id, "status": "accepted", "query": q}
