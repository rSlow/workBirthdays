from fastapi import FastAPI, APIRouter

from . import birthdays


def setup(app: FastAPI):
    root_router = APIRouter()

    root_router.include_router(birthdays.setup())

    app.include_router(root_router)
