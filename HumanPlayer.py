from Pieces.King import King
from Player import Player
from Type import Type
from Alliance import Alliance

class HumanPlayer(Player):
    def __init__(self,pieces, alliance:Alliance, status, king:King, hasEnPassawnablePiece=False,type=Type.HUMAN):
        super().__init__(pieces, type, alliance, status, king, hasEnPassawnablePiece)

