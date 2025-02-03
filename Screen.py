import time
import pygame
import sys
from AI import minimax
from Alliance import Alliance
from Board import Board
from GameExceptions import IllegalMoveException
from HumanPlayer import HumanPlayer
from Move import PawnPromotion
from Player import Player
from Status import Status
from TakenPiecesSideBar import TakenPiecesSideBar
from Tile import ChessTile
from Type import Type
import random

from colors import BLACK, BLUE, BROWN, GRAY, WHITE
# Initialize Pygame

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 8
GRID_CELL_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_CELL_HEIGHT= SCREEN_HEIGHT // GRID_SIZE
SIDE_BAR_WIDTH = 200
pygame.init()

class Screen:
    def __init__(self,vsComp=False) -> None:
        self.vsComp=vsComp
        if not vsComp:
           self.board=Board.initialize(Type.HUMAN,Type.HUMAN)
        else:
            self.board=Board.initialize(Type.COMPUTER,Type.HUMAN)
        self.boards=[self.board]
        self.gameOver=False
        self.running=True
        self.highlight=[]
        self.selectedPiece=None
        self.moveTo=None
        self.promoting=False
        self.promotionMove=None
        self.promotionPieces=['Queen','Bishop','Knight','Rook']
        self.font=pygame.font.Font(None,36)
        self.TextColor=BLACK
        self.Promotiontext='Choose the piece you want to promote to: '
        # Create the Pygame screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH + 2*SIDE_BAR_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")
    def run(self):
        pygame.display.set_caption('Chess with Pygame')
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.promoting:
                    for chessTile in TILES:
                        if chessTile.is_mouse_over() and not self.selectedPiece:
                            self.highlight=chessTile.on_click(self.board.currentPlayer,legalMoves)
                            self.selectedPiece=chessTile.piece
                        if chessTile.is_mouse_over() and self.selectedPiece:
                            if chessTile.piece==0:
                                self.moveTo=(chessTile.row,chessTile.col)
                            elif self.selectedPiece.alliance!=chessTile.piece.alliance:
                                self.moveTo=(chessTile.row,chessTile.col)
                            else:
                                self.highlight=chessTile.on_click(self.board.currentPlayer,legalMoves)
                                self.selectedPiece=chessTile.piece
                elif event.type == pygame.KEYDOWN and self.gameOver:
                    if event.key == pygame.K_r:
                        if self.vsComp:
                            self.board=Board.initialize(Type.COMPUTER,Type.HUMAN)
                        else:
                            self.board=Board.initialize(Type.HUMAN,Type.HUMAN)
                        self.boards=[self.board]
                        # Restart the game when 'R' key is pressed
                        self.gameOver = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.promoting:
                    if option1_rect.collidepoint(event.pos):
                        self.board=self.board.builder(move,'Queen')
                    elif option2_rect.collidepoint(event.pos):
                        self.board=self.board.builder(move,'Bishop')
                    elif option3_rect.collidepoint(event.pos):
                        self.board=self.board.builder(move,'Knight')
                    elif option4_rect.collidepoint(event.pos):
                        self.board=self.board.builder(move,'Rook')
                    self.boards.append(self.board)
                    self.promoting=False
                    self.promotionMove=None
            if not self.promoting and not self.gameOver:
                legalMoves=self.board.legalMoves
                # Clear the screen
                self.screen.fill(GRAY)
                TILES=[]
                # Draw the chessboard
                for col in range(GRID_SIZE):
                    for row in range(GRID_SIZE):
                        blue=False
                        if (row,col) in self.highlight:blue=True
                        TILES.append(ChessTile(self.board.board[row][col],col,row,GRID_CELL_HEIGHT,GRID_CELL_WIDTH,\
                                    SCREEN_HEIGHT,SCREEN_WIDTH,SIDE_BAR_WIDTH,self.screen,blue))
                # Draw the sidebar for removed pieces on the left
                pygame.draw.rect(self.screen, BROWN, (0, 0, SIDE_BAR_WIDTH, SCREEN_HEIGHT))

                # Draw the sidebar for moves made on the right
                pygame.draw.rect(self.screen, BROWN, (SCREEN_WIDTH+SIDE_BAR_WIDTH, 0, SIDE_BAR_WIDTH, SCREEN_HEIGHT))

                time.sleep(0.05)
                TakenPiecesSidebar=TakenPiecesSideBar(self.screen,self.board.takenPieces,self.font)
                TakenPiecesSidebar.draw()
                # Update the display
                pygame.display.flip()
                if (self.board.currentPlayer==Alliance.WHITE and self.board.whiteplayer.type==Type.COMPUTER)\
                    or (self.board.currentPlayer==Alliance.BLACK and self.board.blackplayer.type==Type.COMPUTER):
                    if self.selectedPiece and self.moveTo:
                        for move in legalMoves:
                            if self.moveTo==move.getDestination and self.selectedPiece==move.movedPiece:
                                if isinstance(move,PawnPromotion):
                                    self.promoting=True
                                    self.promotionMove=move
                                    print('promoting')
                                    break
                                else:
                                    # print(type(move))
                                    try:
                                        self.board=self.board.builder(move)
                                        self.boards.append(self.board)
                                        # print(self.board.blackplayer.status.name)
                                        # print(self.board.whiteplayer.status.name)
                                        if self.board.getCurrentPlayer.status==Status.CHECKMATE:
                                            self.gameOver=false
                                        break
                                        # print(vars(board))
                                    except IllegalMoveException:
                                        break
                        self.selectedPiece=None
                        self.moveTo=None
                        self.highlight=[]
                else:
                    start=time.time()
                    bestValue,bestMove=minimax(self.board,2,0,float('-inf'),float('inf'))
                    print(time.time()-start)
                    self.board=self.board.builder(bestMove)
                    self.boards.append(self.board)
            elif self.gameOver:
                self.screen.fill(BLACK)
                game_over_text = self.font.render(f"Game Over {self.board.getOtherPlayer.alliance.name} won", True, WHITE)
                game_over_rect = game_over_text.get_rect(center=((SCREEN_WIDTH +400)// 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(game_over_text, game_over_rect)
                restart_text = self.font.render("Press 'R' to Restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=((SCREEN_WIDTH+400 )// 2,SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(restart_text, restart_rect)
                pygame.display.flip()
            else:
                self.screen.fill(GRAY)
                color=self.board.currentPlayer.name
                option1_rect = pygame.Rect(300, 270, 80, 50)
                image1=pygame.image.load(f'simple/{color[0]+"Q"}.gif')
                image1_rect=image1.get_rect()
                image1_rect.width=30
                image1_rect.height=15
                image1_rect.topleft=(300+(80-30)/2,270+(30-15)/4)
                option2_rect = pygame.Rect(400, 270, 80, 50)
                image2=pygame.image.load(f'simple/{color[0]+"B"}.gif')
                image2_rect=image2.get_rect()
                image2_rect.width=30
                image2_rect.height=15
                image2_rect.topleft=(400+(80-30)/2,270+(30-15)/4)
                option3_rect = pygame.Rect(500, 270, 80, 50)
                image3=pygame.image.load(f'simple/{color[0]+"N"}.gif')
                image3_rect=image3.get_rect()
                image3_rect.width=30
                image3_rect.height=15
                image3_rect.topleft=(500+(80-30)/2,270+(30-15)/4)
                option4_rect = pygame.Rect(600, 270, 80, 50)
                image4=pygame.image.load(f'simple/{color[0]+"R"}.gif')
                image4_rect=image2.get_rect()
                image4_rect.width=30
                image4_rect.height=15
                image4_rect.topleft=(600+(80-30)/2,270+(30-15)/4)
                text_surface = self.font.render(self.Promotiontext, True, self.TextColor)
                text_rect = text_surface.get_rect(center=(500,100))
                pygame.draw.rect(self.screen, BLUE, text_rect, 2)  # Draws a rectangle around the text
                self.screen.blit(text_surface, text_rect)
                pygame.draw.rect(self.screen, BROWN, option1_rect)
                pygame.draw.rect(self.screen, BROWN, option2_rect)
                pygame.draw.rect(self.screen, BROWN, option3_rect)
                pygame.draw.rect(self.screen, BROWN, option4_rect)
                self.screen.blit(image1,image1_rect)
                self.screen.blit(image2,image2_rect)
                self.screen.blit(image3,image3_rect)
                self.screen.blit(image4,image4_rect)
                pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()
Screen(vsComp=True).run()
