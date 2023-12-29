from typing import List
from Alliance import Alliance
from BoardUtils import *
from ComputerPlayer import ComputerPlayer
from GameExceptions import IllegalMoveException
from HumanPlayer import HumanPlayer
from Move import CastleMove, EnPassantMove, LongSideCastleMove, MajorAttackMove, MajorMove, Move, PawnAttackMove, PawnAttackPromotion, PawnJump, PawnMove, PawnPromotion, ShortSideCastleMove
from Pieces.Piece import Piece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.King import King
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Player import Player
from Status import Status
from Type import Type
import copy
import pickle
class Board:
    def __init__(self,whiteplayer:Player,blackplayer:Player,currentPlayer:Alliance):
        self.whiteplayer=whiteplayer
        self.blackplayer=blackplayer
        self.currentPlayer=currentPlayer
        self.takenPieces=[]
        self.board=self.createBoard([*self.whiteplayer.pieces,*self.blackplayer.pieces])
        moves=[]
        initialMoves=self.calculateMoves(self.board,self.currentPlayer)
        for key in initialMoves.keys():
            moves.extend(initialMoves[key])
        self.legalMoves=self.computeLegalMoves(moves)
        if not self.legalMoves:
            self.getCurrentPlayer.status=Status.CHECKMATE
    def isGameOver(self):
        return self.getCurrentPlayer.status==Status.CHECKMATE
    def builder(self,move,promotionPiece=None):
        if move in self.legalMoves.keys():
            board,enPassawnable,takenPiece=self.legalMoves[move]
            if isinstance(move,PawnPromotion):
                destination=move.getDestination
                if promotionPiece=='Queen':
                    board[destination[0]][destination[1]]=Queen(getStrPosition(destination),alliance=self.currentPlayer)
                elif promotionPiece=='Bishop':
                    board[destination[0]][destination[1]]=Bishop(getStrPosition(destination),alliance=self.currentPlayer)
                elif promotionPiece=='Rook':
                    board[destination[0]][destination[1]]=Rook(getStrPosition(destination),alliance=self.currentPlayer)
                elif promotionPiece=='Knight':
                    board[destination[0]][destination[1]]=Knight(getStrPosition(destination),alliance=self.currentPlayer)
                else:
                    board[destination[0]][destination[1]]=Queen(getStrPosition(destination),alliance=self.currentPlayer)
            newCurrentPlayer=self.getCurrentPlayer
            newOtherPlayer=self.getOtherPlayer
            black,white=self.separateColors(board)
            if self.currentPlayer==Alliance.WHITE:
                Current,Other=white,black
            else:
                Current,Other=black,white
            OtherKing,CurrentKing=self.getKing(Other),self.getKing(Current)
            OtherInCheck=False
            newCurrentPlayer.pieces=Current
            newCurrentPlayer.hasEnPassawnablePiece=enPassawnable
            newCurrentPlayer.king=CurrentKing
            newCurrentPlayer.status=Status.GAME
            newOtherPlayer.pieces=Other
            newOtherPlayer.king=OtherKing
            newOtherPlayer.hasEnPassawnablePiece=False
            if self.currentPlayer==Alliance.WHITE:
                moves=self.calculateMoves(board,Alliance.WHITE)
            else:
                moves=self.calculateMoves(board,Alliance.BLACK)
            for key in moves.keys():
                if OtherInCheck:
                    break
                for move in moves[key]:
                    if move.getDestination==getPosition(OtherKing.position):
                        OtherInCheck=True
                        break
            if OtherInCheck:newOtherPlayer.status=Status.CHECK
            else:newOtherPlayer.status=Status.GAME
            if self.currentPlayer==Alliance.WHITE:
                newBoard=Board(newCurrentPlayer,newOtherPlayer,Alliance.BLACK)
            else:
                newBoard=Board(newOtherPlayer,newCurrentPlayer,Alliance.WHITE)
            if takenPiece:
                newBoard.takenPieces=[*self.takenPieces,takenPiece] 
            else:
                newBoard.takenPieces=self.takenPieces
            return newBoard
        else:
            raise IllegalMoveException("Current move is not valid")
    def createBoard(self,pieces:List[Piece])->List:
        board=[[0 for j in range(NUM_TILES)] for i in range(NUM_TILES)]
        for piece in pieces:
            row,column=getPosition(piece.getPosition)
            board[row][column]=piece
        return board
    def getKing(self,pieces):
        for piece in pieces:
            if piece.isKing:
                return piece
    def initialize(player1_type:Type,player2_type:Type):
        whiteAlliance=Alliance.WHITE
        blackAlliance=Alliance.BLACK
        whiteKing=King(f'{START_ROW}e',whiteAlliance)
        blackKing=King(f'{END_ROW}e',blackAlliance)
        whitePieces=[
            Rook(f'{START_ROW}a',whiteAlliance),Knight(f'{START_ROW}b',whiteAlliance),Bishop(f'{START_ROW}c',whiteAlliance),
            whiteKing,Queen(f'{START_ROW}d',whiteAlliance),Bishop(f'{START_ROW}f',whiteAlliance),
            Knight(f'{START_ROW}g',whiteAlliance),Rook(f'{START_ROW}h',whiteAlliance),Pawn(f'{START_ROW+1}a',whiteAlliance),
            Pawn(f'{START_ROW+1}b',whiteAlliance),Pawn(f'{START_ROW+1}c',whiteAlliance),Pawn(f'{START_ROW+1}d',whiteAlliance),
            Pawn(f'{START_ROW+1}e',whiteAlliance),Pawn(f'{START_ROW+1}f',whiteAlliance),Pawn(f'{START_ROW+1}g',whiteAlliance),
            Pawn(f'{START_ROW+1}h',whiteAlliance),
        ]
        blackPieces=[
            Rook(f'{END_ROW}a',blackAlliance),Knight(f'{END_ROW}b',blackAlliance),Bishop(f'{END_ROW}c',blackAlliance),
            blackKing,Queen(f'{END_ROW}d',blackAlliance),Bishop(f'{END_ROW}f',blackAlliance),
            Knight(f'{END_ROW}g',blackAlliance),Rook(f'{END_ROW}h',blackAlliance),Pawn(f'{END_ROW-1}a',blackAlliance),
            Pawn(f'{END_ROW-1}b',blackAlliance),Pawn(f'{END_ROW-1}c',blackAlliance),Pawn(f'{END_ROW-1}d',blackAlliance),
            Pawn(f'{END_ROW-1}e',blackAlliance),Pawn(f'{END_ROW-1}f',blackAlliance),Pawn(f'{END_ROW-1}g',blackAlliance),
            Pawn(f'{END_ROW-1}h',blackAlliance),
        ]
        if player1_type==Type.HUMAN:
            WHITE=HumanPlayer(whitePieces,king=whiteKing,alliance=whiteAlliance,status=Status.GAME)
        else:
            WHITE=ComputerPlayer(whitePieces,king=whiteKing,alliance=whiteAlliance,status=Status.GAME)
        if player2_type==Type.HUMAN:
            BLACK=HumanPlayer(blackPieces,king=blackKing,alliance=blackAlliance,status=Status.GAME)
        else:
            BLACK=ComputerPlayer(blackPieces,king=blackKing,alliance=blackAlliance,status=Status.GAME)
        return Board(WHITE,BLACK,whiteAlliance)
    def calculateMoves(self,board,currentPlayer):
        moves={}
        black,white=self.separateColors(board)
        if currentPlayer==Alliance.WHITE:
            for piece in white:
                moves[piece]=piece.calculateMoves(board)
        else:
            for piece in black:
                moves[piece]=piece.calculateMoves(board)
        return moves
    @property
    def getCurrentPlayer(self):
        if self.currentPlayer==Alliance.WHITE:
            return self.whiteplayer
        else:
            return self.blackplayer
    @property
    def getOtherPlayer(self):
        if self.currentPlayer==Alliance.WHITE:
            return self.blackplayer
        else:
            return self.whiteplayer 
    def computeLegalMoves(self,moves):
        legalMoves={}
        for move in moves:
            dontAdd=False
            board,enPassawnable,takenPiece=self.executeMove(move,self.board)
            # print(str(move.movedPiece),move.getDestination)
            # for row in board:
            #     print(['00' if piece==0 else str(piece) for piece in row ])
            # print('\n\n')
            if not board:
                dontAdd=True
            if board:
                otherMoves=[]
                black,white=self.separateColors(board)
                if self.getOtherPlayer.alliance==Alliance.WHITE:
                    # for piece in white:otherMoves.extend(piece.calculateMoves(board))
                    otherMovesKey=self.calculateMoves(board,Alliance.WHITE)
                    king=self.getKing(black)
                    for key in otherMovesKey.keys():
                        otherMoves.extend(otherMovesKey[key])
                else:
                    # for piece in black:otherMoves.extend(piece.calculateMoves(board))
                    otherMovesKey=self.calculateMoves(board,Alliance.BLACK)
                    king=self.getKing(white)
                    for key in otherMovesKey.keys():
                        otherMoves.extend(otherMovesKey[key])
                for othermove in otherMoves:
                    if getPosition(king.position)==othermove.getDestination:
                        dontAdd=True
                        break
                if isinstance(move,CastleMove):
                    if isinstance(move,ShortSideCastleMove):
                        if move.movedPiece.alliance==Alliance.WHITE:
                            for othermove in otherMoves:
                                if (0,1)==othermove.getDestination or (0,2)==othermove.getDestination:
                                    dontAdd=True
                                    break
                        else:
                            for othermove in otherMoves:
                                if (7,1)==othermove.getDestination or (7,2)==othermove.getDestination:
                                    dontAdd=True
                                    break
                    else:
                        if move.movedPiece.alliance==Alliance.WHITE:
                            for othermove in otherMoves:
                                if (0,4)==othermove.getDestination or (0,5)==othermove.getDestination\
                                    or (0,6)==othermove.getDestination:
                                    dontAdd=True
                                    break
                        else:
                            for othermove in otherMoves:
                                if (7,4)==othermove.getDestination or (7,5)==othermove.getDestination\
                                    or (7,6)==othermove.getDestination:
                                    dontAdd=True
                                    break
                if not dontAdd:
                    legalMoves[move]=[board,enPassawnable,takenPiece]
        return legalMoves
    def separateColors(self,board):
        blackPlayers=[]
        whitePlayers=[]
        for row in board:
            for piece in row:
                if isinstance(piece,Piece):
                    if piece.alliance==Alliance.WHITE:
                        whitePlayers.append(piece)
                    else:
                        blackPlayers.append(piece)
        return blackPlayers,whitePlayers
    def executeMove(self,move:Move,board):
        newboard = pickle.loads(pickle.dumps(board))
        destination=move.getDestination
        piece=move.movedPiece
        otherPlayer=self.getOtherPlayer
        thisPlayer=self.getCurrentPlayer
        origin=getPosition(piece.getPosition)
        if isinstance(move,MajorMove):
            pieceToMove=copy.copy(piece)
            pieceToMove.position=getStrPosition(destination)
            pieceToMove.incrementMoves()
            newboard[origin[0]][origin[1]]=0
            newboard[destination[0]][destination[1]]=pieceToMove
            return (newboard,False,None) # is there enpassawnable piece 2nd entry,3rd entry taken piece
        elif isinstance(move,MajorAttackMove):
            pieceToBeTaken=copy.copy(newboard[destination[0]][destination[1]])
            TakingPiece=copy.copy(piece)
            if pieceToBeTaken.isKing:
                return (None,False,None)
            else:
                TakingPiece.position=getStrPosition(destination)
                TakingPiece.incrementMoves()
                newboard[origin[0]][origin[1]]=0
                newboard[destination[0]][destination[1]]=TakingPiece
                return (newboard,False,pieceToBeTaken)
        elif isinstance(move,PawnMove):
            if isinstance(move,PawnJump): 
                pieceToMove=copy.copy(piece)
                pieceToMove.position=getStrPosition(destination)
                pieceToMove.incrementMoves()
                newboard[origin[0]][origin[1]]=0
                newboard[destination[0]][destination[1]]=pieceToMove
                sideCoor=((destination[0],destination[1]-1),(destination[0],destination[1]+1))
                for x,y in sideCoor:
                    if 0<=x<NUM_TILES and 0<=y<NUM_TILES and isinstance(newboard[x][y],Pawn) \
                        and pieceToMove.alliance!=newboard[x][y].alliance:
                        return (newboard,True,None)
                return (newboard,False,None)
            elif isinstance(move,PawnAttackMove):
                pieceToBeTaken=copy.copy(newboard[destination[0]][destination[1]])
                TakingPiece=copy.copy(piece)
                if pieceToBeTaken.isKing:
                    return (None,False,None)
                else:
                    newboard[origin[0]][origin[1]]=0
                    TakingPiece.position=getStrPosition(destination)
                    TakingPiece.incrementMoves()
                    newboard[destination[0]][destination[1]]=TakingPiece
                    return (newboard,False,pieceToBeTaken)
            elif isinstance(move,EnPassantMove):
                if otherPlayer.hasEnPassawnablePiece:
                    if self.getCurrentPlayer.alliance==Alliance.WHITE:
                        pieceToBeTaken=copy.copy(newboard[destination[0]-1][destination[1]])
                        TakingPiece=copy.copy(piece)
                        newboard[destination[0]-1][destination[1]]=0
                        TakingPiece.incrementMoves()
                        TakingPiece.position=getStrPosition((destination[0],destination[1]))
                        newboard[origin[0]][origin[1]]=0
                        newboard[destination[0]][destination[1]]=TakingPiece
                        return (newboard,False,pieceToBeTaken)
                    else:
                        pieceToBeTaken=copy.copy(newboard[destination[0]+1][destination[1]])
                        TakingPiece=copy.copy(piece)
                        newboard[destination[0]+1][destination[1]]=0
                        TakingPiece.incrementMoves()
                        TakingPiece.position=getStrPosition((destination[0],destination[1]))
                        newboard[origin[0]][origin[1]]=0
                        newboard[destination[0]][destination[1]]=TakingPiece
                        return (newboard,False,pieceToBeTaken)
                else:
                    return (None,False,None)
            elif isinstance(move,PawnPromotion):
                if isinstance(move,PawnAttackPromotion):
                    pieceToBeTaken=copy.copy(self.board[destination[0]][destination[1]])
                    if pieceToBeTaken.isKing:
                        return (None,False,None)
                    else:
                        TakingPiece=copy.copy(piece)
                        TakingPiece.incrementMoves()
                        TakingPiece.position=getStrPosition(destination)
                        newboard[origin[0]][origin[1]]=0
                        newboard[destination[0]][destination[1]]=TakingPiece
                        return (newboard,False,pieceToBeTaken)
                else:
                    pieceToMove=copy.copy(piece)
                    pieceToMove.incrementMoves()
                    newboard[origin[0]][origin[1]]=0
                    newboard[destination[0]][destination[1]]=pieceToMove
                    return (newboard,False,None)
            # normal one up/down pawn move
            else:
                pieceToMove=copy.copy(piece)
                pieceToMove.position=getStrPosition(destination)
                pieceToMove.incrementMoves()
                newboard[origin[0]][origin[1]]=0
                newboard[destination[0]][destination[1]]=pieceToMove
                return (newboard,False,None)
        elif isinstance(move,CastleMove):
            if isinstance(move,ShortSideCastleMove):
                if piece.alliance==Alliance.WHITE and thisPlayer.status==Status.GAME:
                    rookToMove=newboard[0][7]
                    kingToMove=newboard[0][4]
                    newboard[0][7],newboard[0][4]=0,0
                    rookToMove.position=getStrPosition((0,5))
                    kingToMove.position=getStrPosition((0,6))
                    rookToMove.incrementMoves()
                    kingToMove.incrementMoves()
                    newboard[0][5],newboard[0][6]=rookToMove,kingToMove
                    return (newboard,False,None)
                elif piece.alliance==Alliance.BLACK and thisPlayer.status==Status.GAME:
                    rookToMove=newboard[7][7]
                    kingToMove=newboard[7][4]
                    newboard[7][7],newboard[7][4]=0,0
                    rookToMove.position=getStrPosition((7,5))
                    kingToMove.position=getStrPosition((7,6))
                    rookToMove.incrementMoves()
                    kingToMove.incrementMoves()
                    newboard[7][5],newboard[7][6]=rookToMove,kingToMove
                    return (newboard,False,None)
            elif isinstance(move,LongSideCastleMove):
                if piece.alliance==Alliance.WHITE and thisPlayer.status==Status.GAME:
                    rookToMove=newboard[0][0]
                    kingToMove=newboard[0][4]
                    newboard[0][0],newboard[0][4]=0,0
                    rookToMove.position=getStrPosition((0,3))
                    kingToMove.position=getStrPosition((0,2))
                    rookToMove.incrementMoves()
                    kingToMove.incrementMoves()
                    newboard[0][3],newboard[0][2]=rookToMove,kingToMove
                    return (newboard,False,None)
                elif piece.alliance==Alliance.BLACK and thisPlayer.status==Status.GAME:
                    rookToMove=newboard[7][0]
                    kingToMove=newboard[7][4]
                    newboard[7][0],newboard[7][4]=0,0
                    rookToMove.position=getStrPosition((7,3))
                    kingToMove.position=getStrPosition((7,2))
                    rookToMove.incrementMoves()
                    kingToMove.incrementMoves()
                    newboard[7][3],newboard[7][2]=rookToMove,kingToMove
                    return (newboard,False,None)
        return (None,False,None)
    def evaluate(self):
        Sum=0
        if self.currentPlayer==Alliance.WHITE:
            for piece in self.whiteplayer.pieces:
                if piece!=0:
                    x,y=getPosition(piece.getPosition)
                    name=str(piece)[1]
                    Sum+=(POSITIONS[name][x][y]+piece.pieceType.value)
        else:
            for piece in self.blackplayer.pieces:
                if piece!=0:
                    x,y=getPosition(piece.getPosition)
                    name=str(piece)[1]
                    positions=POSITIONS[name][::-1]
                    Sum+=(positions[x][y]+piece.pieceType.value)
        return Sum
# newBoard=Board.initialize()