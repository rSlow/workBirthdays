from contextlib import asynccontextmanager
from typing import Any

from aiogram import Dispatcher
from dishka import AsyncContainer
from fastapi import FastAPI, APIRouter


def setup_lifespan(app: FastAPI, dishka: AsyncContainer, /, **kwargs: Any):
    workflow_data = {
        "app": app,
        "dishka": dishka,
        **kwargs,
    }

    @asynccontextmanager
    async def lifespan(*_: Any, **__: Any):
        dispatcher = await dishka.get(Dispatcher)
        await dispatcher.emit_startup(**workflow_data, **dispatcher.workflow_data)
        yield
        await dispatcher.emit_shutdown(**workflow_data, **dispatcher.workflow_data)

    app.include_router(APIRouter(lifespan=lifespan))
    # lifespan replace events ahahahah fastapi nice work
