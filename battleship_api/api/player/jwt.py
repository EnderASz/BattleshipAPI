from jose import jwt

from . import schemas
from battleship_api.core.settings import get_app_settings


ENCODE_ALGORITHM = jwt.ALGORITHMS.HS256
DECODE_ALGORITHMS = [jwt.ALGORITHMS.HS256]


def encode_player(player: schemas.PlayerToken) -> str:
    """
    Encodes a player into JWT (JSON Web Token)

    Params:
        player: Player object

    Returns:
        JWT token string encoded from player's id and assigned board id
    """
    return jwt.encode(
        player.dict(),
        get_app_settings().secret_key,
        ENCODE_ALGORITHM)


def decode_player(token: str) -> schemas.Player:
    """
    Decode a player's JWT (JSON Web Token) and returns a player object or None
    if it's invalid.

    Params:
        token: Player's JWT token string

    Returns:
        Player object or None if given token is invalid
    """
    try:
        return schemas.Player(
            **jwt.decode(
                token,
                get_app_settings().secret_key,
                DECODE_ALGORITHMS))
    except jwt.JWTError:
        return None
