import pygame
from Piece import Piece


class Bishop(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Bishop.png")
        else:
            self.image = pygame.image.load("../Display/White Bishop.png")


