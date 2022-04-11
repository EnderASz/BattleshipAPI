from fastapi import APIRouter, Depends, Response, status

from . import crud, schemas, tags
from .exceptions import BoardInUseException, BoardNotFoundException

from battleship_api.core.database import get_db_session
from battleship_api.core.exceptions import build_exceptions_dict
from battleship_api.core.types import BoardState

from sqlalchemy.orm import Session


router = APIRouter(prefix='/boards')


@router.post(
    '/',
    response_model=schemas.BoardOut,
    status_code=status.HTTP_201_CREATED,
    tags=[tags.boards_operation['name']])
async def create_board(
    board: schemas.BoardCreate,
    db: Session = Depends(get_db_session)
):
    """
    Creates board with given password and add it to the database.
    \f
    Params:
        - board: Board object that will be added to the database.
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Returns:
        Created board object.
    """
    new_board = crud.create_board(db, board)
    db.commit()
    db.refresh(new_board)
    return new_board


@router.get(
    '/',
    response_model=list[schemas.BoardOut],
    status_code=status.HTTP_200_OK,
    tags=[tags.boards_operation['name']])
async def get_boards(
    db: Session = Depends(get_db_session),
    limit: int = 100,
    offset: int = 0
):
    """
    Retrieves list of boards with lenght limited to `limit` query parameter
    value, starting from `offset` player.
    \f
    Params:
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.
        - [Optional] limit: Number of boards to retrieve.
            - Defaults to: 100.
        - [Optional] offset: Number of boards to skip before retrieve.
            - Defaults to: 0.

    Returns:
        Boards list of `limit` players from `offset` player.
    """
    return crud.get_boards(db, limit, offset)


@router.get(
    '/{board_id}',
    response_model=schemas.BoardOut,
    status_code=status.HTTP_200_OK,
    tags=[tags.boards_operation['name']],
    responses=build_exceptions_dict(BoardNotFoundException))
async def get_board(board_id: int, db: Session = Depends(get_db_session)):
    """
    Retrieves board with given id equal to given `board_id` path parameter.
    \f
    Params:
        - board_id: Retrieving board id
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Returns:
        Board with given id.
    """
    board = crud.get_board(db, board_id)
    if board is None:
        raise BoardNotFoundException(schemas.BoardSearch(id=board_id))
    return board


@router.delete(
    '/{board_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=build_exceptions_dict(
        BoardInUseException,
        BoardNotFoundException),
    tags=[tags.boards_operation['name']])
async def delete_board(board_id: int, db: Session = Depends(get_db_session)):
    """
    Removes board with given id after verifying that it is not in use by any
    player.
    \f
    Params:
        - board_id: Deleting board id
        - db: Database session.
            - Provided automatically by
                `battleship_api.core.database.get_db_session` dependency
                during request.

    Raises:
        - BoardNotFoundException: Board not found by given id.
        - BoardInUseException: Board cannot be removed because any player is
            assigned to it.
    """
    board = crud.get_board(db, board_id)
    if board is None:
        raise BoardNotFoundException(schemas.BoardSearch(id=board_id))
    if len(board.players):
        raise BoardInUseException(schemas.BoardSearch(id=board_id))
    db.delete(board)
    db.commit()
