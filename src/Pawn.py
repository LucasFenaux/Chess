import pygame
from Piece import Piece


class Pawn(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Pawn.png")
        else:
            self.image = pygame.image.load("../Display/White Pawn.png")

