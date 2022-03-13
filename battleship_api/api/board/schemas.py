from pydantic import BaseModel as BaseSchema, validator
import bcrypt


class BoardBase(BaseSchema):
    password: str | bytes | None


class BoardCreate(BoardBase):
    @validator('password')
    def password_validator(cls, password):
        if not password:
            return None
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class BoardSearch(BaseSchema):
    id: int


class Board(BoardBase, BoardSearch):
    class Config:
        orm_mode = True


class BoardOut(BoardSearch):
    pass
