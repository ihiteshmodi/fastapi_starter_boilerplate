from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"params": commons}


async def override_common_parameters(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}


def test_dependency_override():
    app.dependency_overrides[common_parameters] = override_common_parameters
    try:
        with TestClient(app) as client:
            response = client.get("/items/?q=foo&skip=100")
            assert response.status_code == 200
            assert response.json() == {
                "params": {"q": "foo", "skip": 5, "limit": 10},
            }
    finally:
        app.dependency_overrides = {}
