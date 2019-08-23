import pygame
from Piece import Piece


class Queen(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black King.png")
        else:
            self.image = pygame.image.load("../Display/White King.png")
