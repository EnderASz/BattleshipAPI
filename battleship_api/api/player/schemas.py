from pydantic import BaseModel as BaseSchema


class PlayerBase(BaseSchema):
    board_id: int


class PlayerStatus(BaseSchema):
    ready: bool = False


class PlayerSearch(BaseSchema):
    id: int

    class Config:
        orm_mode = True


class PlayerToken(PlayerBase, PlayerSearch):
    pass


class Player(PlayerBase, PlayerSearch, PlayerStatus):
    class Config:
        orm_mode = True
