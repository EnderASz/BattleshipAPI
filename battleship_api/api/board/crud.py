from sqlalchemy.orm import Session

from . import schemas
from . import models


def create_board(db: Session, board: schemas.BoardCreate):
    new_board = models.Board(**board.dict())
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


def get_board(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()


def get_boards(db: Session, limit: int, offset: int):
    return db.query(models.Board).offset(offset).limit(limit).all()
