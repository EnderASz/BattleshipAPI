from fastapi import APIRouter, Depends, Header, status

from . import crud
from . import schemas
from . import tags
from .exceptions import ShotCreationConflictException, ShotNotFoundException
from .models import Shot as ShotModel

from battleship_api.core.types import BoardState
from battleship_api.api.board import crud as board_crud

from battleship_api.api.player.exceptions import (
    InvalidPlayerAccessTokenException)
from battleship_api.api.player.jwt import decode_player
from battleship_api.api.player.models import Player as PlayerModel
from battleship_api.api.player import crud as player_crud
from battleship_api.api.player import schemas as player_schemas

from battleship_api.api.ship.models import Ship as ShipModel
from battleship_api.api.ship.funcs import is_ship

from battleship_api.core.database import get_db_session
from battleship_api.core.exceptions import build_exceptions_dict

from sqlalchemy.orm import Session

router = APIRouter(prefix='/shots')


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Shot],
    tags=[tags.shots_operation['name']])
async def get_shots(
    db: Session = Depends(get_db_session),
    limit: int = 100,
    offset: int = 0
):
    """
    Retrieves list of shots with length limited to `limit` query parameter
    value, starting at `offset` shot.
    \f
    Params:
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.
        - [Optional] limit: Maximum number of shots to retrieve.
            - Defaults to: 100.
        - [Optional] offset: Number of shots to skip before retrieve.
            - Defaults to: 0.

    Returns:
        Shot list of length limited to `limit` starting at `offset` shot.
    """
    return crud.get_shots(db, limit, offset)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Shot,
    responses=build_exceptions_dict(
        InvalidPlayerAccessTokenException,
        ShotCreationConflictException),
    tags=[tags.shots_operation['name']])
async def create_shot(
    new_shot: schemas.ShotCreate,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Creates shot instance and adds it to the database if player validated
    successfully and no shot creation conflicts detected.
    \f
    Args:
        - new_shot: Shot creation data.
        - x_auth_token: Player validation token.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - InvalidPlayerAccessTokenException: Given player authentication token
            is invalid.
        - ShotCreationConflictException: Shot cannot be created, due to
            detected conflict.

    Returns:
        Created shot database instance.
    """
    authed = decode_player(x_auth_token)
    if authed is None or new_shot.player_id != authed.id:
        raise InvalidPlayerAccessTokenException({"x_auth_token": x_auth_token})

    authed = player_crud.get_player(db, authed.id)

    enemy_player_id = db.query(PlayerModel.id).filter(
        PlayerModel.id != authed.id,
        PlayerModel.board_id == authed.board_id).scalar()

    enemy_shots_num = db.query(ShotModel).filter(
        ShotModel.player_id == enemy_player_id).count()
    player_shots_num = db.query(ShotModel).filter(
        ShotModel.player_id == authed.id).count()
    if (
        authed.board.state is not BoardState.in_game
        or (
            authed.id < enemy_player_id
            and player_shots_num > enemy_shots_num)
        or (
            authed.id > enemy_player_id
            and player_shots_num == enemy_shots_num)
        or db.query(
            db.query(ShotModel).filter(
                ShotModel.player_id == new_shot.player_id,
                ShotModel.row == new_shot.row,
                ShotModel.column == new_shot.column).exists()
        ).scalar()
    ):
        raise ShotCreationConflictException(new_shot)

    new_shot = crud.create_shot(db, new_shot)
    db.commit()
    db.refresh(new_shot)

    enemy_ships = db.query(ShipModel).filter(
        ShipModel.owner_id == enemy_player_id
    ).all()
    success_shots = [
        shot
        for shot
        in db.query(ShotModel).filter(ShotModel.player_id == authed.id)
        if is_ship(shot.column, shot.row, enemy_ships)]
    if (sum([ship.length for ship in enemy_ships]) == len(success_shots)):
        board = board_crud.get_board(db, authed.board_id)
        board.state = BoardState.game_finished
        db.commit()

    return new_shot


@router.get(
    '/{shot_id}',
    response_model=schemas.Shot,
    status_code=status.HTTP_200_OK,
    responses=build_exceptions_dict(ShotNotFoundException),
    tags=[tags.shots_operation['name']])
async def get_shot(shot_id: int, db: Session = Depends(get_db_session)):
    """
    Retrieves shot with given id and returns it.
    \t
    Args:
        - shot_id: Shot id
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - ShotNotFoundException: Shot not found by given id.

    Returns:
        Shot database object
    """
    shot = crud.get_shot(db, shot_id)
    if shot is None:
        raise ShotNotFoundException(schemas.ShotSearch(id=shot_id))
    return shot


@router.get(
    '/{shot_id}/hit',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Hit,
    responses=build_exceptions_dict(ShotNotFoundException),
    tags=[tags.shots_operation['name']])
async def get_shot_success(
    shot_id: int,
    db: Session = Depends(get_db_session)
):
    """
    Retrieves information about shot success and returns it.
    \t
    Args:
        - shot_id: Shot id
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - ShotNotFoundException: Shot not found by given id.

    Returns:
        Shot success info
    """
    shot = crud.get_shot(db, shot_id)
    if shot is None:
        raise ShotNotFoundException(schemas.ShotSearch(id=shot_id))

    board_id = db.query(PlayerModel.board_id).filter(
        PlayerModel.id == shot.player_id
    ).scalar()

    enemy_player_id = db.query(PlayerModel.id).filter(
        PlayerModel.id != shot.player_id,
        PlayerModel.board_id == board_id
    ).scalar()

    return schemas.Hit(
        hit=is_ship(
            shot.column,
            shot.row,
            db.query(ShipModel).filter(ShipModel.owner_id == enemy_player_id)))
