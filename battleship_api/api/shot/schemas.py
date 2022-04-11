from pydantic import BaseModel as BaseSchema, Field

from battleship_api.core.types import Hit


class ShotLocation(BaseSchema):
    column: int = Field(..., ge=1, le=10)
    row: int = Field(..., ge=1, le=10)


class ShotCreate(ShotLocation):
    player_id: int


class ShotSearch(BaseSchema):
    id: int


class Shot(ShotCreate, ShotSearch):
    class Config:
        orm_mode = True
