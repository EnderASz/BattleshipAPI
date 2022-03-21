from fastapi import (
    APIRouter,
    Body,
    Depends,
    Header,
    Response,
    status)
import bcrypt

from . import schemas
from . import crud
from . import jwt
from . import tags
from battleship_api.api.board import crud as board_crud
from battleship_api.core.database import get_db_session
from battleship_api.core.exceptions import build_exceptions_dict

from .exceptions import (
    InvalidPlayerAccessTokenException,
    MaximumPlayersNumberException,
    PlayerNotFoundException)
from battleship_api.api.board.exceptions import (
    BoardNotFoundException,
    MissingBoardPasswordException,
    InvalidBoardPasswordException)

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
        raise PlayerNotFoundException({'id': player_id})
    return player


@router.delete(
    '/{player_id}',
    status_code=status.HTTP_200_OK,
    tags=[tags.players_operation['name']],
    responses=build_exceptions_dict(
        InvalidPlayerAccessTokenException,
        PlayerNotFoundException))
async def delete_player(
    player_id: int,
    x_auth_token: str = Header(...),
    db: Session = Depends(get_db_session)
):
    """
    Deletes player if given JWT access token (X-Auth-Token header value) is
    valid.
    \f
    Params:
        - player_id: Player id
        - x_auth_token: Player JWT access token.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.
    """
    player = crud.get_player(db, player_id)
    auth_player = jwt.decode_player(x_auth_token)
    if player is None:
        raise PlayerNotFoundException({'player_id': player_id})
    if [auth_player.id, auth_player.board_id] != [player.id, player.board_id]:
        raise InvalidPlayerAccessTokenException({'player_id': player.id})
    player.delete()
