from pydantic import BaseModel as BaseSchema


class PlayerBase(BaseSchema):
    board_id: int


class Player(PlayerBase):
    id: int
