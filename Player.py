from typing import List
from Alliance import Alliance
from Pieces.Piece import Piece
from Pieces.King import King
from Status import Status
from Type import Type


class Player:
    def __init__(self,pieces:List[Piece],type:Type,alliance:Alliance,status:Status,king:King,hasEnPassawnablePiece=False):
        self.type=type
        self.alliance=alliance
        self.pieces=pieces
        self.status=status
        self.king=king
        self.hasEnPassawnablePiece=hasEnPassawnablePiece