from email.mime import message
from fastapi import status

from . import schemas
from battleship_api.api.board import schemas as board_schemas
from battleship_api.core.exceptions import BaseAPIException


class PlayerNotFoundException(BaseAPIException):
    """
    API exception raise when board object can not be found.

    `battleship_api.api.player.schemas.PlayerSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_404_NOT_FOUND
    message = "Player not found"
    schema = schemas.PlayerSearch


class MaximumPlayersNumberException(BaseAPIException):
    """
    API exception raise when player tries to join to board with maximum number
    of players.

    `battleship_api.api.board.schemas.BoardSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_409_CONFLICT
    message = "There are maximum number of players assigned to this board"
    schema = board_schemas.BoardSearch


class InvalidPlayerAccessTokenException(BaseAPIException):
    """
    API exception raise when received player access token is invalid.

    `battleship_api.api.player.schemas.PlayerSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_403_FORBIDDEN
    message = "Invalid X-Auth-Token header value"
    schema = schemas.PlayerSearch
