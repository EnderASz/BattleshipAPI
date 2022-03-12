from fastapi import APIRouter

from .board.routes import router as board_router
from .player.routes import router as player_router


api_router = APIRouter(prefix='/api')

api_router.include_router(board_router)
api_router.include_router(player_router)
