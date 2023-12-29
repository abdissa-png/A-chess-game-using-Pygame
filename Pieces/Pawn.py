from Alliance import Alliance
from BoardUtils import NUM_TILES, getPosition
from Move import EnPassantMove, MajorAttackMove, MajorMove, Move, PawnAttackMove, PawnAttackPromotion, PawnJump, PawnMove, PawnPromotion
from Pieces.Piece import Piece
from Pieces.PieceType import PieceType


class Pawn(Piece):
    def __init__(self, position: str, alliance: str,pieceType=PieceType.PAWN):
        super().__init__(position, alliance ,pieceType)
    def calculateMoves(self, board: list):
        moves=[]
        row,column=getPosition(self.position)
        # vertical one forward(white),one backward(black)
        newRow,newColumn=row+1 if self.alliance==Alliance.WHITE else row-1,column
        if 0<newRow<NUM_TILES-1 and 0<=newColumn<NUM_TILES:
            if not isinstance(board[newRow][newColumn],Piece):
                moves.append(PawnMove(self,(newRow,newColumn)))
        # last rows
        elif (newRow==0 or newRow==NUM_TILES-1) and 0<=newColumn<NUM_TILES:
            # slot must be empty to promote
            if not isinstance(board[newRow][newColumn],Piece):
                # to promote white it must reach 8th row
                if newRow==NUM_TILES-1 and self.alliance==Alliance.WHITE:
                    moves.append(PawnPromotion(self,(newRow,newColumn)))
                # to promote black it must reach 0th row
                elif newRow==0 and self.alliance==Alliance.BLACK:
                    moves.append(PawnPromotion(self,(newRow,newColumn)))
        # vertical two forward(white),two backward(black)
        newRow,newColumn=row+2 if self.alliance==Alliance.WHITE else row-2,column
        inbetween=newRow
        if self.alliance==Alliance.WHITE:
            inbetween-=1
        else:
            inbetween+=1
        if 0<newRow<NUM_TILES-1 and 0<=newColumn<NUM_TILES:
            if (not isinstance(board[newRow][newColumn],Piece)) and (not isinstance(board[inbetween][newColumn],Piece)) and self.nomovesyet:
                moves.append(PawnJump(self,(newRow,newColumn)))
        # thought promotion can be possible with a jump
        # # last rows promotion
        # elif (newRow==0 or newRow==NUM_TILES-1) and 0<=newColumn<NUM_TILES:
        #     # slot must be empty to promote
        #     if not isinstance(board[newRow][newColumn],Piece):
        #         # to promote white it must reach 8th row
        #         if newRow==NUM_TILES-1 and self.alliance==Alliance.WHITE:
        #             moves.append(PawnPromotion(self,(newRow,newColumn)))
        #         # to promote black it must reach 0th row
        #         elif newRow==0 and self.alliance==Alliance.BLACK:
        #             moves.append(PawnPromotion(self,(newRow,newColumn)))
        # diagonal left moves
        newRow,newColumn=row+1 if self.alliance==Alliance.WHITE else row-1,column-1
        if 0<newRow<NUM_TILES-1 and 0<=newColumn<NUM_TILES:
            # if a pawn is to the left
            if isinstance(board[row][newColumn],Pawn):
                if board[row][newColumn].isFirstMove:
                    moves.append(EnPassantMove(self,(newRow,newColumn)))
            if isinstance(board[newRow][newColumn],Piece):
                # diagonal left take
                if board[newRow][newColumn].alliance!=self.alliance:
                    moves.append(PawnAttackMove(self,(newRow,newColumn)))
        # last rows promotion
        elif (newRow==0 or newRow==NUM_TILES-1) and 0<=newColumn<NUM_TILES:
            # for diagonal promotion it must take the piece
            if  isinstance(board[newRow][newColumn],Piece) and board[newRow][newColumn].alliance!=self.alliance:
                if newRow==NUM_TILES-1 and self.alliance==Alliance.WHITE:
                    moves.append(PawnAttackPromotion(self,(newRow,newColumn)))
                elif newRow==0 and self.alliance==Alliance.BLACK:
                    moves.append(PawnAttackPromotion(self,(newRow,newColumn)))
        # diagonal right moves
        newRow,newColumn=row+1 if self.alliance==Alliance.WHITE else row-1,column+1
        if 0<newRow<NUM_TILES-1 and 0<=newColumn<NUM_TILES:
            # if a piece is in right diagonal
            if isinstance(board[newRow][newColumn],Piece):
                if board[newRow][newColumn].alliance!=self.alliance:
                    moves.append(PawnAttackMove(self,(newRow,newColumn)))
            # if a pawn is to the right
            if isinstance(board[row][newColumn],Pawn):
                if board[row][newColumn].isFirstMove:
                    moves.append(EnPassantMove(self,(newRow,newColumn)))
        # last rows promotion
        elif (newRow==0 or newRow==NUM_TILES-1) and 0<=newColumn<NUM_TILES:
            # diagonal promotion works only by taking piece and the piece is not yours
            if  isinstance(board[newRow][newColumn],Piece) and board[newRow][newColumn].alliance!=self.alliance:
                if newRow==NUM_TILES-1 and self.alliance==Alliance.WHITE:
                    moves.append(PawnAttackPromotion(self,(newRow,newColumn)))
                elif newRow==0 and self.alliance==Alliance.BLACK:
                    moves.append(PawnAttackPromotion(self,(newRow,newColumn)))
        return moves