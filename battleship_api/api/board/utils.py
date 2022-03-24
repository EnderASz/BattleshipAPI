from enum import Enum


class BoardState(Enum):
    preparing = 0
    in_game = 1
    game_finished = 2
