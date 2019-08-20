import pygame


class Piece(pygame.sprite.Sprite):
    def __init__(self, board_location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Display/Black Pawn.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = board_location
