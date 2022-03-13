from pydantic import BaseModel as BaseSchema


class PlayerBase(BaseSchema):
    board_id: int


class PlayerSearch(BaseSchema):
    id: int


class Player(PlayerBase, PlayerSearch):
    pass
