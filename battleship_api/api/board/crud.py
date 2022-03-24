from sqlalchemy.orm import Session

from . import schemas
from . import models
from .exceptions import BoardInUseException, BoardNotFoundException

def create_board(db: Session, board: schemas.BoardCreate):
    """Creates board instance and adds it to the database.

    Params:
        - db: Database session
        - board: Board data represented by
            `battleship_api.api.board.schemas.BoardCreate` schema

    Returns:
        New board database object instance.
    """
    new_board = models.Board(**board.dict())
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


def get_board(db: Session, board_id: int):
    """
    Returns board object from database searched by board id.

    Params:
        - db: Database session
        - board_id: Board id

    Returns:
        Board database object instance.
    """
    return db.query(models.Board).filter(models.Board.id == board_id).first()


def get_boards(db: Session, limit: int, offset: int):
    """
    Returns list of 'limit' boards in database starting from `offset` board.

    Params:
        db: Database session
        - limit: Number of boards to return
        - offset: Number of skipped boards

    Returns:
        Board list of 'limit' elements starting from 'offset' database.
    """
    return db.query(models.Board).offset(offset).limit(limit).all()


def delete_board(db: Session, board_id: int):
    """
    Removes board with given id from the database, if there is no players
    assigned to it.
    In this case it always be 0 (if player remove was not successful)
    or 1 (if player remove was successful).

    Params:
        - db: Database session
        - player_id: Player id

    Raises:
        - BoardNotFoundException: Board not found by given id.
        - BoardInUseException: Board cannot be removed because any player is
            assigned to it.
    """
    board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if board is None:
        raise BoardNotFoundException(schemas.BoardSearch(id=board_id))
    if board.players.count():
        raise BoardInUseException(schemas.BoardSearch(id=board_id))
    board.delete()
    db.commit()
