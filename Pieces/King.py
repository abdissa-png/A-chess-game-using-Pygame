from Alliance import Alliance
from BoardUtils import NUM_TILES, getPosition
from Move import LongSideCastleMove, MajorAttackMove, Move,MajorMove, ShortSideCastleMove
from Pieces.Piece import Piece
from Pieces.PieceType import PieceType


class King(Piece):
    def __init__(self, position: str, alliance: str,pieceType=PieceType.KING):
        super().__init__(position, alliance, pieceType)
    def calculateMoves(self, board: list):
        moves=[]
        row,column=getPosition(self.position)
        directions=((0,1),(1,0),(0,-1),(-1,0),
                    (1,1),(1,-1),(-1,1),(-1,-1))
        for x,y in directions:
            newRow,newColumn=row+x,column+y
            if 0<=newRow<NUM_TILES and 0<=newColumn<NUM_TILES:
                if isinstance(board[newRow][newColumn],Piece):
                    if board[newRow][newColumn].alliance==self.alliance:
                        continue
                    else:
                        moves.append(MajorAttackMove(self,(newRow,newColumn)))
                else:
                    moves.append(MajorMove(self,(newRow,newColumn)))
            else:
                continue
        # to handle castling
        if self.nomovesyet:
            # castle white
            if self.alliance==Alliance.WHITE:
                # short castle
                if isinstance(board[0][7],Piece) and board[0][7].isRook and board[0][7].alliance==self.alliance\
                    and board[0][7].nomovesyet and not isinstance(board[0][5],Piece) \
                    and not isinstance(board[0][6],Piece):
                        moves.append(ShortSideCastleMove(self,(0,6)))
                # long castle
                if isinstance(board[0][0],Piece) and board[0][0].isRook and board[0][0].alliance==self.alliance\
                    and board[0][0].nomovesyet and not isinstance(board[0][1],Piece) \
                    and not isinstance(board[0][2],Piece) and not isinstance(board[0][3],Piece):
                        moves.append(LongSideCastleMove(self,(0,2)))
            # castle black
            else:
                if self.alliance==Alliance.BLACK:
                    # short castle
                    if isinstance(board[7][7],Piece) and board[7][7].isRook and board[7][7].alliance==self.alliance\
                        and board[7][7].nomovesyet and not isinstance(board[7][5],Piece) \
                        and not isinstance(board[7][6],Piece):
                            moves.append(ShortSideCastleMove(self,(7,6)))
                    # long castle
                    if isinstance(board[7][0],Piece) and board[7][0].isRook and board[7][0].alliance==self.alliance\
                        and board[7][0].nomovesyet and not isinstance(board[7][1],Piece) \
                        and not isinstance(board[7][2],Piece) and not isinstance(board[7][3],Piece):
                            moves.append(LongSideCastleMove(self,(7,2)))
        return moves