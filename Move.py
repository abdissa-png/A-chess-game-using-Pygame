from abc import ABC

from Pieces.Piece import Piece

class Move(ABC):
    def __init__(self,movedPiece:Piece,destination:tuple[int]):
        self.movedPiece=movedPiece
        self.destination=destination
    @property
    def getDestination(self):
        return self.destination
    @property
    def getMoveAlliance(self):
        return self.movedPiece.getAlliance
    def __hash__(self) -> int:
        return hash((self.movedPiece,self.destination))
class MajorMove(Move):
    pass
class MajorAttackMove(Move):
    pass
class PawnMove(Move):
    pass
class EnPassantMove(PawnMove):
    pass
class PawnPromotion(PawnMove):
    pass
class PawnAttackPromotion(PawnPromotion):
    pass
class PawnJump(PawnMove):
    pass
class PawnAttackMove(PawnMove):
    pass
class CastleMove(Move):
    pass
class ShortSideCastleMove(CastleMove):
    pass
class LongSideCastleMove(CastleMove):
    pass