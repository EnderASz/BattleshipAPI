from fastapi import status
from pydantic import BaseModel as BaseSchema

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

    Dictionary with `x_auth_token` value must be provided,
    when initialized.

    Example:
    ```python
    raise InvalidPlayerAccessTokenException({'x_auth_token': "invalid token"})
    ```
    """
    code = status.HTTP_403_FORBIDDEN
    message = "Invalid X-Auth-Token header value"

    class schema(BaseSchema):
        x_auth_token: str


class PlayerIsReadyException(BaseAPIException):
    """
    API exception raise when cannot do an operation that needs player not to be
    ready.

    `battleship_api.api.player.schemas.PlayerSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_409_CONFLICT
    message = ("Operation cannot be performed, because player have ready"
               " status.")
    schema = schemas.PlayerSearch


class PlayerStatusChangeConflictException(BaseAPIException):
    """
    API exception raise when occurrs conflict on change of player's status.
    Conflict may occure in one of the following cases:
        - board state is not "preparing"
        - player have to few ships assigned (created)

    `battleship_api.api.player.schemas.PlayerSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_409_CONFLICT
    message = ("Player's status change conflict occured, probably due to"
               " assigned board's status is \"in game\" or player have to few"
               " ships created.")
    schema = schemas.PlayerSearch
