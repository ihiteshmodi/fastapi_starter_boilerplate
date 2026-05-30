from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI


analytics_app = FastAPI(title="analytics-subapp")
search_app = FastAPI(title="search-subapp")


@analytics_app.get("/health")
async def analytics_health():
    return {"service": "analytics", "ok": True}


@search_app.get("/health")
async def search_health():
    return {"service": "search", "ok": True}


@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    # Fan-in mounted sub-app lifespans into one parent lifecycle.
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(analytics_app.router.lifespan_context(analytics_app))
        await stack.enter_async_context(search_app.router.lifespan_context(search_app))
        yield


app = FastAPI(lifespan=combined_lifespan)
app.mount("/analytics", analytics_app)
app.mount("/search", search_app)


@app.get("/healthz")
async def root_health():
    return {"service": "gateway", "ok": True}
