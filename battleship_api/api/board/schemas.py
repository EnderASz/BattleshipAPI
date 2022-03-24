from pydantic import BaseModel as BaseSchema, validator
import bcrypt

from .utils import BoardState


class BoardBase(BaseSchema):
    password: str | bytes | None


class BoardCreate(BoardBase):
    @validator('password')
    def password_validator(cls, password):
        if not password:
            return None
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')


class BoardSearch(BaseSchema):
    id: int


class Board(BoardBase, BoardSearch):
    state: BoardState

    class Config:
        orm_mode = True


class BoardOut(BoardSearch):
    class Config:
        orm_mode = True
