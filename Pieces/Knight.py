from BoardUtils import NUM_TILES, getPosition
from Pieces.Bishop import Bishop
from Move import MajorAttackMove, MajorMove, Move
from Pieces.Piece import Piece
from Pieces.PieceType import PieceType


class Knight(Piece):
    def __init__(self, position: str, alliance: str,pieceType=PieceType.KNIGHT):
        super().__init__(position, alliance ,pieceType)
    def calculateMoves(self,board):
        directions=((2,1),(2,-1),(1,2),(1,-2),(-2,-1),(-2,1),(-1,-2),(-1,2))
        moves=[]
        row,column=getPosition(self.position)
        for x,y in directions:
            newRow,newColumn=row+x,column+y
            if 0<=newRow<NUM_TILES and 0<=newColumn<NUM_TILES:
                if isinstance(board[newRow][newColumn],Piece):
                    if board[newRow][newColumn].alliance==self.alliance:
                        continue
                    else:
                        moves.append(MajorAttackMove(self,(row+x,column+y)))
                else:
                    moves.append(MajorMove(self,(row+x,column+y)))
            else:
                continue
        return moves