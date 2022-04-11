from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column

from battleship_api.core.database import BaseModel
from battleship_api.core.types import BoardState


class Board(BaseModel):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=True)
    state = Column(Enum(BoardState), default=BoardState.preparing)

    players = relationship(
        'battleship_api.api.player.models.Player',
        back_populates='board')
