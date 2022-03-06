from fastapi import FastAPI

from .core import logging
from .core.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Function initializing application instance with given settings.
    If settings not provided, function takes care of creating them,
    from default ones, environment variables and if is it possible config file.

    Params:
        - [Optional] settings - Settings object instance.
            - If not provided, default settings are used and overwrited by
              environment variables and configuration file settings if
              available.

    Returns:
        FastAPI: BattleshipAPI app instance
    """
    if settings is None:
        settings = get_settings()
        
    logging.init(
        logging.DEFAULT_LOGGER_NAME
        if settings.debug
        else logging.DEBUG_LOGGER_NAME)
    app = FastAPI()
    return app
