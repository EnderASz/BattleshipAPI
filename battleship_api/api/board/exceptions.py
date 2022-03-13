from fastapi import status

from . import schemas
from battleship_api.core.exceptions import BaseAPIException


class BoardNotFoundException(BaseAPIException):
    """
    API exception raise when board object can not be found.

    `battleship_api.api.board.schemas.BoardSearch` data must be provided, when
    initialized.
    """
    code = status.HTTP_404_NOT_FOUND
    message = "Board not found"
    schema = schemas.BoardSearch
