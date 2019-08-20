import pygame


class Board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load("../Display/Board.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]
