from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

app_state: dict[str, object] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_state["cache"] = {}
    yield
    app_state.clear()


app = FastAPI(lifespan=lifespan)


def get_db_session():
    db = {"connected": True}
    try:
        yield db
    finally:
        db["connected"] = False


def get_username():
    try:
        yield "service-user"
    finally:
        # With scope="function", this cleanup runs before response is sent.
        print("cleanup before response")


@app.get("/healthz")
async def healthcheck(db: Annotated[dict, Depends(get_db_session)]):
    return {
        "status": "ok",
        "cache_ready": "cache" in app_state,
        "db_connected": db["connected"],
    }


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_username, scope="function")]):
    return {"username": username}
