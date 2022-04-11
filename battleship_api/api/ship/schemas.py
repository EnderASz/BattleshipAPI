from pydantic import BaseModel as BaseSchema, Field

from enum import Enum

from battleship_api.core.types import Orientation


class ShipSearch(BaseSchema):
    id: int


class ShipOwner(BaseSchema):
    owner_id: int


class ShipLocation(BaseSchema):
    length: int = Field(..., ge=1, le=4)
    column: int = Field(..., ge=1, le=10)
    row: int = Field(..., ge=1, le=10)
    orientation: Orientation


class ShipCreate(ShipLocation, ShipOwner):
    pass


class ShipPublic(ShipSearch, ShipOwner):
    class Config:
        orm_mode = True


class ShipRestricted(ShipLocation):
    class Config:
        orm_mode = True


class Ship(ShipPublic, ShipRestricted):
    pass
