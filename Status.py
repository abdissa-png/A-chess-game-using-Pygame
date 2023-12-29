from enum import Enum

class Status(Enum):
    CHECK=0
    CHECKMATE=1
    ILLEGAL_MOVE=2
    GAME=3