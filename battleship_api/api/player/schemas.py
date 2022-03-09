from pydantic import BaseModel as BaseSchema, validator
from fastapi import HTTPException, status


class Player(BaseSchema):
    id: int
    board_id: int
