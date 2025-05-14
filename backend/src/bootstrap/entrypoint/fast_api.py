import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.src.bootstrap.di.container import get_container
from backend.src.presentation.endpoints import router

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def run_api() -> None:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        title="Gatchi energy",
        description="API gatchi energy",
    )
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = get_container()

    setup_dishka(container=container, app=app)

    logging.info("FastAPI app created.")

    # добавить роутеры тут
    app.include_router(router)

    uvicorn.run(
        app,
        port=8000,
        host="localhost",
        log_config=log_config,
    )


if __name__ == "__main__":
    run_api()
