import logging
import logging.config
from pydantic import BaseModel

from logging import Logger
from typing import Callable


DEFAULT_LOGGER_NAME = 'battleship_api'
DEBUG_LOGGER_NAME = f'{DEFAULT_LOGGER_NAME}.debug'


logger_queue = list()
logger_initialized = False


class LogConfig(BaseModel):
    """
    Logger configuration used in application (for debug and release modes).
    """
    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s'
        }
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr'
        }
    }
    loggers = {
        DEFAULT_LOGGER_NAME: {
            'handlers': ['default'],
            'level': logging.INFO
        },
        DEBUG_LOGGER_NAME: {
            'level': logging.DEBUG
        }
    }


def append_logger_queue(task: Callable[[Logger], None]):
    global logger_queue
    global logger_initialized
    if logger_initialized:
        global logger
        task(logger)
        return
    logger_queue.append(task)


def init(name: str | None = None):
    """
    Initialize new logger and replace previous one with it.

    Use `battleship_api.core.logging.DEBUG_LOGGER_NAME` as `name` parameter
    value only in debug mode.

    Params:
        - [Optional] `name` - Logger name string defining new logger.
            - Default: `battleship_api.core.logging.DEFAULT_LOGGER_NAME`
    """
    global logger
    global logger_queue
    global logger_initialized
    logging.config.dictConfig(LogConfig().dict())
    logger = logging.getLogger(name or DEFAULT_LOGGER_NAME)
    logger_initialized = True
    for task in logger_queue:
        task(logger)


def get_app_logger():
    """
    Returns application logger instance.
    """
    global logger
    return logger
