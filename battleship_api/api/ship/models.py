from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, ForeignKey, Integer

from battleship_api.core.database import BaseModel
from battleship_api.core.types import Orientation
from battleship_api.api.player.models import Player


class Ship(BaseModel):
    __tablename__ = 'ships'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(
        Integer,
        ForeignKey(f'{Player.__tablename__}.id'),
        index=True)
    length = Column(Integer)
    column = Column(Integer, index=True)
    row = Column(Integer, index=True)
    orientation = Column(Enum(Orientation))

    owner = relationship(
        'battleship_api.api.player.models.Player',
        back_populates='ships')
