from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

items: dict[str, dict[str, str]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    yield
    items.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return items[item_id]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


def test_lifespan_runs_in_testclient_context():
    assert items == {}

    with TestClient(app) as client:
        assert items == {
            "foo": {"name": "Fighters"},
            "bar": {"name": "Tenders"},
        }

        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}

    assert items == {}


def test_websocket():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            data = websocket.receive_json()
            assert data == {"msg": "Hello WebSocket"}
