from fastapi import (
    APIRouter,
    Body,
    Depends,
    Header,
    Response,
    status)
import bcrypt

from . import crud, jwt, schemas, tags
from .exceptions import (
    InvalidPlayerAccessTokenException,
    MaximumPlayersNumberException,
    PlayerNotFoundException,
    PlayerStatusChangeConflictException)
from .models import Player as PlayerModel

from battleship_api.api.board import crud as board_crud
from battleship_api.api.board import schemas as board_schemas
from battleship_api.api.board.exceptions import (
    BoardNotFoundException,
    GameFinishedException,
    InvalidBoardPasswordException,
    MissingBoardPasswordException)

from battleship_api.core.database import get_db_session
from battleship_api.core.exceptions import build_exceptions_dict
from battleship_api.core.types import BoardState

from sqlalchemy.orm import Session


router = APIRouter(prefix='/players')


@router.get(
    '/',
    response_model=list[schemas.Player],
    status_code=status.HTTP_200_OK,
    tags=[tags.players_operation['name']])
async def get_players(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db_session)
):
    """
    Retrieves list of players with lenght limited to `limit` query parameter
    value, starting from `offset` player.
    \f
    Params:
        - [Optional] limit: Maximum number of players to retrieve.
            - Defaults to: 100.
        - [Optional] offset: Number of players to skip before retrieve.
            - Defaults to: 0.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Returns:
        Players list of length limited to `limit` starting at `offset` player.
    """
    return crud.get_players(db, limit, offset)


@router.post(
    '/',
    response_model=schemas.Player,
    status_code=status.HTTP_201_CREATED,
    tags=[tags.players_operation['name']],
    responses=build_exceptions_dict(
        BoardNotFoundException,
        InvalidBoardPasswordException,
        MaximumPlayersNumberException,
        MissingBoardPasswordException))
async def create_player(
    response: Response,
    board_id: int = Body(...),
    password: str | None = Body(None),
    db: Session = Depends(get_db_session)
):
    """
    Creates assigned to board by `board_id` player instance and adds it to the
    database.

    If password is required for the access to board, you should pass
    `password` value in request body.
    \f
    Params:
        - response: Response object that will be modified during request
        processing.
            - It is provided via FastAPI framework by default.
        - board_id: Board id to which player will be assigned.
            - It is provided via request body.
        - [Optional] password: Board access password.
            - Provided via request body.
            - Required if board access requires password.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Returns:
        Created player instance data (without password) and player access
        token via `X-Auth-Token` header.
    """
    board = board_crud.get_board(db, board_id)
    if board is None:
        raise BoardNotFoundException({'id': board_id})

    if board.password is not None:
        if password is None:
            raise MissingBoardPasswordException()
        if not bcrypt.checkpw(
            password.encode('utf-8'),
            board.password.encode('utf-8')
        ):
            raise InvalidBoardPasswordException()
    if not len(board.players) < 2:
        raise MaximumPlayersNumberException({'id': board.id})

    player = crud.create_player(db, board)
    db.commit()
    db.refresh(player)

    token = jwt.encode_player(schemas.Player.from_orm(player))
    response.headers['X-Auth-Token'] = token
    return player


@router.get(
    '/{player_id}',
    response_model=schemas.Player,
    status_code=status.HTTP_200_OK,
    tags=[tags.players_operation['name']],
    responses=build_exceptions_dict(PlayerNotFoundException))
async def get_player(player_id: int, db: Session = Depends(get_db_session)):
    """
    Retrieves player with given id equal to given `player_id` path parameter.
    \f
    Params:
        - player_id: Retrieving player id
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Returns:
        Player with given id.
    """
    player = crud.get_player(db, player_id)
    if player is None:
        raise PlayerNotFoundException(schemas.PlayerSearch(id=player_id))
    return player


@router.delete(
    '/{player_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=build_exceptions_dict(
        GameFinishedException,
        InvalidPlayerAccessTokenException,
        PlayerNotFoundException),
    tags=[tags.players_operation['name']])
async def delete_player(
    player_id: int,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Deletes player if given JWT access token (X-Auth-Token header value) is
    valid.

    If player was in game, it's status will change to "preparing".
    \f
    Params:
        - player_id: Player id
        - x_auth_token: Player JWT access token.
            - Provided by header.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - GameFinishedException: Board status is "finished" and player cannot
            be deleted.
        - InvalidPlayerAccessTokenException: Given player authentication token
            is invalid.
        - PlayerNotFoundException: Player not found by given id.

    """
    player = crud.get_player(db, player_id)
    authed = jwt.decode_player(x_auth_token)
    if player is None:
        raise PlayerNotFoundException(schemas.PlayerSearch(id=player_id))
    if authed is None or authed.id != player.id:
        raise InvalidPlayerAccessTokenException({"x_auth_token": x_auth_token})
    if player.board.status == BoardState.game_finished:
        raise GameFinishedException(
            board_schemas.BoardSearch.from_orm(player.board))
    player.board.state = BoardState.preparing

    db.delete(player)
    db.commit()


@router.put(
    '/{player_id}/ready',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Player,
    responses=build_exceptions_dict(
        InvalidPlayerAccessTokenException,
        PlayerNotFoundException,
        PlayerStatusChangeConflictException),
    tags=[tags.players_operation['name']])
async def update_player_status(
    player_id: int,
    body: schemas.PlayerStatus,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Updates player's `ready` status.

    If new status is True, checks if another
    player assigned to that same board as this player is ready and updates the
    board status to "in game".

    Cannot update player status if board status is not "preparing" or player
    has not assigned 4 ships.
    \f
    Params:
        - player_id: Player id
        - x_auth_token: Player JWT access token.
            - Provided by `X-Auth-Token` header.
        - body: Request body containing new player's `ready` status data.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - InvalidPlayerAccessTokenException: Given player authentication token
            is invalid.
        - PlayerNotFoundException: Player not found by given id.
        - PlayerStatusChangeConflictException: Player status cannot be updated
            because board status is not "preparing" or player has not 4 ships
            assigned.

    Returns:
        Updated player database object.
    """
    player = crud.get_player(db, player_id)
    if player is None:
        raise PlayerNotFoundException(schemas.PlayerSearch(id=player_id))
    authed = jwt.decode_player(x_auth_token)
    if authed is None or authed.id != player.id:
        raise InvalidPlayerAccessTokenException({"x_auth_token": x_auth_token})

    new_status = body.ready

    if (
        player.board.state != BoardState.preparing
        or (new_status and len(player.ships) != 4)
    ):
        raise PlayerStatusChangeConflictException(
            schemas.PlayerSearch.from_orm(player))

    player.ready = new_status

    if (
        player.ready
        and db.query(PlayerModel.ready).filter(
            PlayerModel.board_id == player.board_id,
            PlayerModel.id != player.id
        ).scalar()
    ):
        player.board.state = BoardState.in_game

    db.commit()
    return player
