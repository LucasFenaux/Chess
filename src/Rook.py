import pygame
from Piece import Piece


class Rook(Piece):
    def __init__(self, board_location, color):
        Piece.__init__(self, board_location)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Rook.png")
        else:
            self.image = pygame.image.load("../Display/White Rook.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = board_location
