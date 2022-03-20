from pydantic import BaseModel as BaseSchema, Field

from .utils import Orientation


class ShipLocation(BaseSchema):
    length: int = Field(..., ge=1, le=4)
    column: int = Field(..., ge=1, le=10)
    row: int = Field(..., ge=1, le=10)
    orientation: Orientation


class ShipRestricted(ShipLocation):
    pass


class ShipCreate(ShipRestricted):
    owner_id: int


class Ship(ShipCreate):
    id: int

    class Config:
        orm_mode = True
