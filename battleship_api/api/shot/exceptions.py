from fastapi import status

from . import schemas

from battleship_api.core.exceptions import BaseAPIException


class ShotCreationConflictException(BaseAPIException):
    """
    API exception raise when shot cannot be created, due to detected conflict.
    Conflict may occure in one of the following cases:
        - board state is not "in game"
        - player should wait until enemy player will create shot
        - player has already created shot at the same location

    `battleship_api.api.shot.schemas.ShotCreate` data must be provided,
    when initialized.
    """
    code = status.HTTP_409_CONFLICT
    message = (
        "Shot creation conflict. Player could already create shot at"
        " this location, should wait until enemy player will shot first or"
        " board status in not \"in game\".")
    schema = schemas.ShotCreate


class ShotNotFoundException(BaseAPIException):
    """
    API exception raise when shot cannot be found by given id.

    'battleship_api.api.shot.schemas.ShotSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_404_NOT_FOUND
    message = "Shot not found."
    schema = schemas.ShotSearch
