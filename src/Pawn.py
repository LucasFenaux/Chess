import pygame
from Piece import Piece


class Pawn(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Pawn.png")
        else:
            self.image = pygame.image.load("../Display/White Pawn.png")
        self.has_moved = False

    def check_if_move_is_valid(self, new_square, game_orientation):
        return True
        # loc = new_square.get_location()
        # if game_orientation == "wb":
        #     if self.color == 'black':
        #         if not self.has_moved:
        #             if loc[1]
        #     else:
        #         if not self.has_moved:
        # elif game_orientation == "bb":
        #     if self.color == 'black':
        #         if not self.has_moved:
        #             if loc[1]
        #     else:
        #         if not self.has_moved:
        # else:
        #     return False