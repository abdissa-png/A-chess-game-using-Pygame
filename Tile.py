import pygame
from Alliance import Alliance
from Pieces.Piece import Piece

from colors import BLACK, BLUE, GREEN, WHITE


class ChessTile:
    def __init__(self,piece,col,row,gridHeight,gridWidth,screenHeight,screenWidth,sideBarWidth,screen,highlight):
        self.piece=piece
        self.row=row
        self.col=col
        self.borderWidth=2
        self.borderColor=BLACK
        self.color = WHITE if (self.col + self.row) % 2 != 0 else GREEN
        self.top= screenHeight-gridHeight-self.row * gridHeight
        self.left= self.col * gridWidth+sideBarWidth
        self.rect = pygame.Rect(self.left,self.top, gridWidth, gridHeight)
        if highlight:self.color=BLUE
        pygame.draw.rect(screen, self.color, (self.left, self.top, gridWidth, gridHeight))
        border_rect = self.rect.inflate(self.borderWidth * 2, self.borderWidth * 2)
        pygame.draw.rect(screen, self.borderColor, border_rect, self.borderWidth)
        if piece!=0:
            image=pygame.image.load(f'simple/{str(piece)}.gif')
            image_rect=image.get_rect()
            image_rect.width=gridHeight
            image_rect.height=gridWidth
            image_rect.topleft=(self.left+gridWidth/4,self.top+gridHeight/4)
            screen.blit(image,image_rect)
    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)
    def on_click(self,currentPlayer,legalMoves):
        highlight=[]
        if isinstance(currentPlayer,Alliance):
            if self.piece!=0:
                if currentPlayer==self.piece.alliance:
                    for key in legalMoves.keys():
                        if key.movedPiece==self.piece:
                            highlight.append(key.destination)
        # print(currentPlayer,self.piece.alliance,highlight,self.piece.pieceType,self.piece.nmoves,self.piece.nomovesyet)
        return highlight