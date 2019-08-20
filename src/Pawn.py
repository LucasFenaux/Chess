import pygame
from Piece import Piece


class Pawn(Piece):
    def __init__(self, board_location, color):
        Piece.__init__(self, board_location)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Pawn.png")
        else:
            self.image = pygame.image.load("../Display/White Pawn.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = board_location
