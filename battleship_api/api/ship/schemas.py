from pydantic import BaseModel as BaseSchema, Field, validator

from .utils import Rotation


class ShipCreate(BaseSchema):
    owner_id: int
    length: int
    column: int = Field(..., ge=1, le=10)
    row: int = Field(..., ge=1, le=10)
    rotation: Rotation


class Ship(ShipCreate):
    id: int

    class Config:
        orm_mode = True
