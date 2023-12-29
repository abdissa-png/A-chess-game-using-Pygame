import pygame
from Alliance import Alliance
from colors import WHITE
class TakenPiecesSideBar:
    def __init__(self,screen,takenPieces,font):
        self.screen=screen
        self.font=font
        self.takenPieces=takenPieces
        self.heightPiece=self.widthPiece=5
        self.whiteTop=self.blackTop=25
        self.whiteLeft=25
        self.blackLeft=120
    def draw(self):
        game_over_text = self.font.render("Taken Pieces", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(90,18))
        self.screen.blit(game_over_text, game_over_rect)
        game_over_text = self.font.render("White", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(35,50))
        self.screen.blit(game_over_text, game_over_rect)
        game_over_text = self.font.render("Black", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(165,50))
        self.screen.blit(game_over_text, game_over_rect)     
        for piece in self.takenPieces:
            image=pygame.image.load(f'simple/{str(piece)}.gif')
            image_rect=image.get_rect()
            image_rect.width=image.get_size()[0]
            image_rect.height=image.get_size()[1]
            if piece.alliance==Alliance.WHITE:
                self.whiteTop+=50
                left,top=self.whiteLeft,self.whiteTop 
                if self.whiteTop+image.get_size()[1]>600:
                    self.whiteTop=25
                    self.whiteLeft+=image.get_size()[0]
            else:
                self.blackTop+=50
                left,top=self.blackLeft,self.blackTop
                if self.blackTop+image.get_size()[1]>600:
                    self.blackTop=25
                    self.blackLeft+=image.get_size()[0]
            image_rect.topleft=(left,top+self.heightPiece/2)
            self.screen.blit(image,image_rect)
        