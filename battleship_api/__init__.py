from fastapi import FastAPI

from .core import logging
from .core.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()
    if settings.debug:
        logging.init(logging.DEBUG_LOGGER_NAME)
    app = FastAPI()
    return app
