from sqlalchemy import Boolean, Column, ForeignKey, Integer
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
    ready = Column(Boolean, default=False)

    board = relationship(
        'battleship_api.api.board.models.Board',
        back_populates='players')
    ships = relationship(
        'battleship_api.api.ship.models.Ship',
        cascade="all, delete",
        back_populates='owner')
    shots = relationship(
        'battleship_api.api.shot.models.Shot',
        cascade="all, delete",
        back_populates='player')
