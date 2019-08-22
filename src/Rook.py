import pygame
from Piece import Piece


class Rook(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Rook.png")
        else:
            self.image = pygame.image.load("../Display/White Rook.png")
