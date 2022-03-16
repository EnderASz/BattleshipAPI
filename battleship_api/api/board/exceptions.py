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


class MissingBoardPasswordException(BaseAPIException):
    """
    API exception raise when missing board access password.
    """
    code = status.HTTP_401_UNAUTHORIZED
    message = "Board access requires password"


class InvalidBoardPasswordException(BaseAPIException):
    """
    API exception raise when invalid board access password is provided.
    """
    code = status.HTTP_403_FORBIDDEN
    message = "Board access password is incorrect"