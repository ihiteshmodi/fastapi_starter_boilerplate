from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

app = FastAPI()
MAX_BODY_BYTES = 1_000_000  # 1 MB


@app.middleware("http")
async def body_size_guard(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_BODY_BYTES:
        return JSONResponse(
            status_code=413,
            content={"error": "Payload too large"},
        )
    return await call_next(request)
