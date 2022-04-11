from pydantic import BaseModel as BaseSchema, validator
import bcrypt

from battleship_api.core.types import BoardState


class BoardSecure(BaseSchema):
    password: str | bytes | None


class BoardCreate(BoardSecure):
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

    class Config:
        orm_mode = True


class BoardState(BaseSchema):
    state: BoardState


class BoardOut(BoardSearch, BoardState):
    class Config:
        orm_mode = True


class BoardDB(BoardOut, BoardSecure):
    class Config:
        orm_mode = True
