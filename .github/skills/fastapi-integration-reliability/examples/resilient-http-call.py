import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/external/profile")
async def get_external_profile():
    timeout = httpx.Timeout(10.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get("https://example.com/api/profile")
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Upstream timeout") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail="Upstream returned error") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="Upstream unavailable") from exc
