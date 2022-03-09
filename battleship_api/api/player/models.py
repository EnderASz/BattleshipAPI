from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from battleship_api.core.database import BaseModel
from battleship_api.api.board.models import Board


class Player(BaseModel):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(
        Integer,
        ForeignKey(f'{Board.__tablename__}.id'),
        index=True)

    board = relationship(
        'battleship_api.api.board.models.Board',
        back_populates='players')
