from BoardUtils import NUM_TILES, getPosition
from Move import MajorAttackMove, MajorMove, Move
from Pieces.Piece import Piece
from Pieces.PieceType import PieceType


class Queen(Piece):
    def __init__(self, position: str, alliance: str ,piecetype=PieceType.QUEEN):
        super().__init__(position, alliance ,piecetype)
    def calculateMoves(self, board: list):
        moves=[]
        directions=((-1,1),(1,-1),(1,1),(-1,-1),(0,1),(0,-1),(-1,0),(1,0))
        row,column=getPosition(self.position)
        for x,y in directions:
            newRow,newColumn=row,column
            while True:
                newRow,newColumn=newRow+x,newColumn+y
                if 0<=newRow<NUM_TILES and 0<=newColumn<NUM_TILES:
                    if isinstance(board[newRow][newColumn],Piece):
                        if board[newRow][newColumn].alliance==self.alliance:
                            break
                        else:
                            # maximum move in that direction
                            moves.append(MajorAttackMove(self,(newRow,newColumn)))
                            break
                    else:
                        moves.append(MajorMove(self,(newRow,newColumn)))
                else:
                    break
        return moves