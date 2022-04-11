from pydantic import BaseModel as BaseSchema

from enum import IntEnum


class Orientation(IntEnum):
    vertical = 0
    horizontal = 1


class Point(BaseSchema):
    x: int
    y: int
