from fastapi import status

from . import schemas
from battleship_api.core.exceptions import BaseAPIException


class ShipCreationConflictException(BaseAPIException):
    """
    API exception raise when ship cannot be created, due to detected conflict.
    Conflict may occure when player tries to create a new ship that collides
    with any existing or is the same length.

    `battleship_api.api.ship.schemas.ShipCreate` data must be provided,
    when initialized.
    """
    code = status.HTTP_409_CONFLICT
    message = ("Ship creation conflict detected. Ship may have same length or"
               " it's position collides with one of already existing"
               " ships.")
    schema = schemas.ShipCreate


class ShipNotFoundException(BaseAPIException):
    """
    API exception raise when ship cannot be found by given id.

    'battleship_api.api.shot.schemas.ShipSearch` data must be provided,
    when initialized.
    """
    code = status.HTTP_404_NOT_FOUND
    message = "Ship not found."
    schema = schemas.ShipSearch
