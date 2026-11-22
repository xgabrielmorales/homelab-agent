from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.common import configure_observability, settings

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    configure_observability()
    yield


async def healthcheck(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


app = Starlette(
    routes=[Route("/healthcheck", healthcheck)],
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.UVICORN_WORKERS,
    )
