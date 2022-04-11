from sqlalchemy.orm import Session

from . import schemas

from .models import Board as BoardModel


def create_board(db: Session, board: schemas.BoardCreate) -> BoardModel:
    """
    Creates board instance and adds it to the database.

    Params:
        - db: Database session
        - board: Board data represented by
            `battleship_api.api.board.schemas.BoardCreate` schema

    Returns:
        New board database object instance.
    """
    new_board = BoardModel(**board.dict())
    db.add(new_board)
    return new_board


def get_board(db: Session, board_id: int) -> BoardModel | None:
    """
    Returns board object from database searched by board id.

    Params:
        - db: Database session
        - board_id: Board id

    Returns:
        Board database object instance.
    """
    return db.query(BoardModel).filter(BoardModel.id == board_id).first()


def get_boards(db: Session, limit: int, offset: int) -> list[BoardModel]:
    """
    Returns list of 'limit' boards in database starting from `offset` board.

    Params:
        db: Database session
        - limit: Number of boards to return
        - offset: Number of skipped boards

    Returns:
        Board list of 'limit' elements starting from 'offset' database.
    """
    return db.query(BoardModel).offset(offset).limit(limit).all()
