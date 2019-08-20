import pygame
from Piece import Piece


class Bishop(Piece):
    def __init__(self, board_location, color, board):
        Piece.__init__(self, board_location, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Bishop.png")
        else:
            self.image = pygame.image.load("../Display/White Bishop.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [board_location[0] * int(board.size[0] / 8),
                                         board_location[1] * int(board.size[1] / 8)]

