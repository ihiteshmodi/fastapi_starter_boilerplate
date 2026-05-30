import asyncio
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI

app = FastAPI()
process_pool = ProcessPoolExecutor(max_workers=2)


def heavy_cpu_inference(x: int) -> int:
    total = 0
    for i in range(20_000_000):
        total += (i % 7) * x
    return total


@app.get("/compute/{x}")
async def compute(x: int):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(process_pool, heavy_cpu_inference, x)
    return {"result": result}
