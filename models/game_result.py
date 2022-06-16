from enum import Enum


class GameResult(str, Enum):
    WIN = "WIN"
    LOSE = "LOSE"
    NOT_DECIDED = "NOT_DECIDED"
