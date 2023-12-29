from Player import Player
from Type import Type
from Alliance import Alliance

class ComputerPlayer(Player):
    def __init__(self, pieces, alliance, status, king, hasEnPassawnablePiece=False,type=Type.COMPUTER):
        super().__init__(pieces, type, alliance, status, king, hasEnPassawnablePiece)