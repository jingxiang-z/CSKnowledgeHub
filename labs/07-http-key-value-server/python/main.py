import logging
import re
from threading import Lock
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class PutRequest(BaseModel):
    value: Any = Field(...)


app = FastAPI()
store = {}
lock = Lock()
logger = logging.getLogger("key_value_server")


@app.middleware("http")
async def log_request(request: Request, call_next):
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        logger.info("%s %s %s", request.method, request.url.path, status_code)


@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception):
    logger.error(
        "Unhandled error during %s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def check_key(key: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", key):
        raise HTTPException(status_code=400, detail="Invalid key")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/keys/{key}")
def get_key_value(key: str):
    check_key(key)
    with lock:
        if key not in store:
            raise HTTPException(status_code=404, detail="Key not found")
        value = store[key]
    return {"key": key, "value": value}


@app.put("/keys/{key}")
def put_key_value(key: str, request: PutRequest):
    check_key(key)
    with lock:
        store[key] = request.value
    return {"key": key, "value": request.value}


@app.delete("/keys/{key}")
def delete_key_value(key: str):
    check_key(key)
    with lock:
        if key not in store:
            raise HTTPException(status_code=404, detail="Key not found")
        del store[key]
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="127.0.0.1", port=8000,
                timeout_graceful_shutdown=5, access_log=False)
