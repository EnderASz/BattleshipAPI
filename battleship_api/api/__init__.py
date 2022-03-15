from fastapi import APIRouter

from .board.routes import router as board_router
from .player.routes import router as player_router
from .ship.routes import router as ship_router

from .board.tags import all_tags as board_tags
from .player.tags import all_tags as player_tags
from .ship.tags import all_tags as ship_tags


api_tags = (
    board_tags
    + player_tags
    + ship_tags)


api_router = APIRouter(prefix='/api')

api_router.include_router(board_router)
api_router.include_router(player_router)
api_router.include_router(ship_router)
