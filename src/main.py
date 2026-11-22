from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import httpx
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from src.agents import homelab_agent
from src.common import configure_observability, settings
from src.tools import Deps

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

async_http_client = httpx.AsyncClient(timeout=30)


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    configure_observability()

    async with async_http_client:
        yield


async def healthcheck(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


app = Starlette(
    routes=[
        Route("/healthcheck", healthcheck),
        Mount(
            "/",
            homelab_agent.to_web(
                deps=Deps(async_http_client=async_http_client),
                html_source=settings.CHAT_UI_HTML,
                allowed_hosts=settings.ALLOWED_HOSTS,
            ),
        ),
    ],
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.UVICORN_WORKERS,
    )
