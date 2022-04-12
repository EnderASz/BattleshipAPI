from fastapi import APIRouter, Depends, Header, Response, status

from battleship_api.core.database import get_db_session
from battleship_api.core.exceptions import build_exceptions_dict

from . import crud, funcs, tags, schemas

from .exceptions import ShipCreationConflictException, ShipNotFoundException
from battleship_api.api.player.exceptions import (
    InvalidPlayerAccessTokenException,
    PlayerIsReadyException,
    PlayerNotFoundException)

from battleship_api.api.player import crud as player_crud
from battleship_api.api.player import schemas as player_schemas
from battleship_api.api.player.jwt import decode_player

from sqlalchemy.orm import Session


router = APIRouter(prefix='/ships')


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ShipPublic],
    response_model_exclude=schemas.ShipRestricted.schema().keys(),
    tags=[tags.ships_operation['name']])
async def get_ships(
    db: Session = Depends(get_db_session),
    limit: int = 100,
    offset: int = 0
):
    """
    Retrieves list of ships with length limited to `limit` query parameter
    value, starting at `offset` ship.
    \f
    Params:
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.
        - [Optional] limit: Maximum number of ships to retrieve.
            - Defaults to: 100.
        - [Optional] offset: Number of ships to skip before retrieve.
            - Defaults to: 0.

    Returns:
        Ship list of length limited to `limit` starting at `offset` ship.
    """
    return crud.get_ships(db, limit, offset)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Ship,
    responses=build_exceptions_dict(
        InvalidPlayerAccessTokenException,
        PlayerNotFoundException,
        ShipCreationConflictException),
    tags=[tags.ships_operation['name']])
async def create_ship(
    new_ship: schemas.ShipCreate,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Creates assigned to owner (player) ship instance and adds it to the
    database.
    \f
    Params:
        - ship_data: Ship creation data.
        - x_auth_token: Player validation token.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raise:
        - InvalidPlayerAccessTokenException: Given player authentication token
            is invalid.
        - PlayerNotFoundException: Player cannot cannot be found by given
            `owner_id`.
        - ShipCreationConflictException: Ship cannot be created due to conflict
            with another already existing ship.

    Returns:
        Database ship instance.
    """
    authed = decode_player(x_auth_token)
    if authed is None or authed.id != new_ship.owner_id:
        raise InvalidPlayerAccessTokenException({"x_auth_token": x_auth_token})

    if not (owner := player_crud.get_player(db, new_ship.owner_id)):
        raise PlayerNotFoundException({'id': new_ship.owner_id})

    for ship in owner.ships:
        if funcs.ships_conflicts(new_ship, ship):
            raise ShipCreationConflictException(new_ship)
    # Ship cannot conflict with any existing one when player is not ready, so
    # it's no needed to verify player's `ready` status.

    new_ship = crud.create_ship(db, new_ship)
    db.commit()
    db.refresh(new_ship)
    return new_ship


@router.get(
    '/{ship_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Ship,
    responses=build_exceptions_dict(
        InvalidPlayerAccessTokenException,
        ShipNotFoundException),
    tags=[tags.ships_operation['name']])
async def get_ship_all_data(
    ship_id: int,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Retrieves ship object from database and returns it all data if validated
    player is owner of this ship.
    \f
    Params:
        - ship_id: Ship id
        - x_auth_token: Player validation token.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - InvalidPlayerAccessTokenException: Given player authentication token
            is invalid for owner of given ship.
        - ShipNotFoundException: Ship not found by given id.

    Returns:
        Ship database object full representation
    """
    ship = crud.get_ship(db, ship_id)
    if ship is None:
        raise ShipNotFoundException(schemas.ShipSearch(id=ship_id))

    player = decode_player(x_auth_token)
    if player is None or player.id != ship.owner_id:
        raise InvalidPlayerAccessTokenException({"x_auth_token": x_auth_token})

    return ship


@router.delete(
    '/{ship_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=build_exceptions_dict(
        InvalidPlayerAccessTokenException,
        PlayerIsReadyException,
        ShipNotFoundException),
    tags=[tags.ships_operation['name']])
async def delete_ship(
    ship_id: int,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Deletes ship if given JWT access token (X-Auth-Token header value) is
    valid for owner of that ship, that owner have not "ready" status.
    \f
    Params:
        - ship_id: Ship id
        - x_auth_token: Ship owner JWT access token.
            - Provided by `X-Auth-Token` header.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raise:
        - ShipNotFoundException: Ship not found by given id.
        - InvalidPlayerAccessTokenException: Given player authentication token
            is invalid for owner of given ship.
        - PlayerIsReadyException: Player's ship collection cannot be modified,
            due to player's `ready` status is `True`.
    """
    ship = crud.get_ship(db, ship_id)
    if ship is None:
        raise ShipNotFoundException(schemas.ShipSearch(id=ship_id))

    authed = decode_player(x_auth_token)
    if authed is None or authed.id != ship.owner_id:
        raise InvalidPlayerAccessTokenException({"x_auth_token": x_auth_token})

    if ship.owner.ready:
        raise PlayerIsReadyException(
            player_schemas.PlayerSearch(id=ship.owner_id))

    db.delete(ship)
    db.commit()


@router.get(
    '/{ship_id}/public',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShipPublic,
    responses=build_exceptions_dict(ShipNotFoundException),
    tags=[tags.ships_operation['name']])
async def get_ship_public_data(
    ship_id: int,
    db: Session = Depends(get_db_session)
):
    ship = crud.get_ship(db, ship_id)
    if ship is None:
        raise ShipNotFoundException(schemas.ShipSearch(id=ship_id))
    return ship
