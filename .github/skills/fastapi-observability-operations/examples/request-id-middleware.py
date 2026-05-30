import contextvars
import logging
import time
import uuid

from fastapi import FastAPI, Request

app = FastAPI()
REQUEST_ID_HEADER = "x-request-id"
request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.addFilter(RequestIdFilter())
handler.setFormatter(
    logging.Formatter("%(asctime)s level=%(levelname)s request_id=%(request_id)s %(message)s")
)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def build_outbound_headers(existing: dict[str, str] | None = None) -> dict[str, str]:
    headers = dict(existing or {})
    headers[REQUEST_ID_HEADER] = request_id_ctx.get()
    return headers


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get(REQUEST_ID_HEADER, uuid.uuid4().hex[:8])
    token = request_id_ctx.set(request_id)
    start = time.perf_counter()
    try:
        logger.info("request received method=%s path=%s", request.method, request.url.path)
        response = await call_next(request)
        duration_ms = int((time.perf_counter() - start) * 1000)
        response.headers[REQUEST_ID_HEADER] = request_id
        logger.info(
            "request complete status_code=%s duration_ms=%s",
            response.status_code,
            duration_ms,
        )
        return response
    finally:
        request_id_ctx.reset(token)


@app.get("/example-downstream-call")
async def example_downstream_call() -> dict:
    outbound_headers = build_outbound_headers({"x-service": "api-gateway"})
    logger.info("calling downstream with propagated request id")
    return {"outbound_headers": outbound_headers}
