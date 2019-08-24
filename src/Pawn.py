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
        if game_orientation == "wb":
            return self.check_for_wb(new_square)
        elif game_orientation == "bb":
            return self.check_for_bb(new_square)

    def check_for_wb(self, new_square):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()
        if self.color == 'black':
            if not self.has_moved:
                if new_loc[1] == loc[1] + 2 and new_square.get_piece() is None and grid[loc[0]][
                    new_loc[1] - 1].get_piece() is None:
                    return True
            if new_loc[1] == loc[1] + 1 and new_square.get_piece() is None:
                return True
            elif new_loc[1] == loc[1] + 1 and (new_loc[0] == loc[0] + 1 or new_loc[0] == loc[
                0] - 1) and new_square.get_piece().get_color() == 'white':
                return True
            elif new_loc[1] - 1 >= 0:
                if type(grid[new_loc[0]][new_loc[1] - 1].get_piece()) == Pawn and grid[new_loc[0]][
                    new_loc[1] - 1].get_piece().get_color() == 'white':
                    return True
            else:
                return False
        else:
            return True

    def check_for_bb(self, new_square):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()

    def move(self, new_square, game_orientation):
        moved = super().move(new_square, game_orientation)
        if moved:
            self.has_moved = True
        return moved
