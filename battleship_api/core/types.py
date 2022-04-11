from pydantic import BaseModel as BaseSchema

from enum import IntEnum


class BoardState(IntEnum):
    preparing = 0
    in_game = 1
    game_finished = 2


class Hit(BaseSchema):
    hit: bool


class Orientation(IntEnum):
    vertical = 0
    horizontal = 1


class Point(BaseSchema):
    x: int
    y: int
