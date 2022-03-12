from fastapi import FastAPI

from .core import database, exceptions, logging
from .core.settings import (
    get_app_settings,
    init as init_settings,
    init_from_object as init_settings_from_object)

from .core.settings import Settings


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
        init_settings()
    else:
        init_settings_from_object(settings)
    settings = get_app_settings()

    logging.init(
        logging.DEFAULT_LOGGER_NAME
        if settings.debug
        else logging.DEBUG_LOGGER_NAME)

    db_args = dict()
    if settings.db_check_same_thread is not None:
        db_args |= {'check_same_thread': settings.db_check_same_thread}
    database.init(settings.db_url, **db_args)

    app = FastAPI()
    app.add_exception_handler(exceptions.BaseAPIException, exceptions.api_exceptions_handler)
    return app
