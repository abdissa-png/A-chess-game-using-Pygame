from Alliance import Alliance
from Pieces.PieceType import PieceType


class Piece:
    def __init__(self,position:str,alliance:Alliance,pieceType:PieceType):
        self.position=position
        self.alliance=alliance
        self.pieceType=pieceType
        self.nmoves=0
    def calculateMoves(self,board:list):
        raise NotImplementedError
    # def __str__(self) -> str:
    #     return self.pieceType.name + f"piece of alliance {self.alliance.name} at position {self.position}"
    def __eq__(self, other: object) -> bool:
        if isinstance(other,Piece):
            return self.pieceType==other.pieceType and \
                   self.position==other.position and \
                   self.alliance==other.alliance and \
                   self.isFirstMove==other.isFirstMove
        return False
    def incrementMoves(self):
        self.nmoves+=1
    @property
    def nomovesyet(self):
        return self.nmoves==0
    @property
    def isFirstMove(self):
        return self.nmoves==1
    @property
    def getAlliance(self):
        return self.alliance
    @property
    def getPosition(self):
        return self.position
    @property
    def isKing(self):
        return self.pieceType==PieceType.KING
    @property
    def isRook(self):
        return self.pieceType==PieceType.ROOK
    def __str__(self):
        return self.alliance.name[0]+(self.pieceType.name[0] if self.pieceType!=PieceType.KNIGHT else self.pieceType.name[1])
    def __hash__(self):
        return hash((self.alliance,self.pieceType,self.getPosition))