from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, UniqueConstraint
from sqlalchemy import ForeignKey, Integer

from battleship_api.core.database import BaseModel
from battleship_api.api.player.models import Player


class Shot(BaseModel):
    __tablename__ = 'shots'
    __tableargs__ = (UniqueConstraint(
        'row',
        'column',
        name='_location_unique_constraint'),)

    id = Column(Integer, primary_key=True)
    player_id = Column(
        Integer,
        ForeignKey(f'{Player.__tablename__}.id')
    )
    row = Column(Integer)
    column = Column(Integer)

    player = relationship(
        'battleship_api.api.player.models.Player',
        back_populates='shots')
