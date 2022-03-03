from fastapi import FastAPI

from .core import logging


def create_app() -> FastAPI:
    app = FastAPI()
    return app
