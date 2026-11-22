from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from src.common import configure_observability, settings

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[dict[str, Any]]:
    configure_observability()

    async with httpx.AsyncClient(timeout=30) as async_http_client:
        yield {"async_http_client": async_http_client}


app = FastAPI(
    title="Homelab Agent",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)


@app.get("/docs", include_in_schema=False)
async def show_scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title=app.title,
        hide_client_button=True,
        hide_download_button=True,
        hide_models=True,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.UVICORN_WORKERS,
    )
