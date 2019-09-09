import pygame
from Piece import Piece


class Rook(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Rook.png")
        else:
            self.image = pygame.image.load("../Display/White Rook.png")

    def check_if_move_is_valid(self, new_square, game_orientation):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()
        # First check if the move is in a line
        x_dif = abs(new_loc[0] - loc[0])
        y_dif = abs(new_loc[1] - loc[1])
        if x_dif != 0 and y_dif != 0:
            return {"valid": False, "piece taken": None}
        # Then check if the rook can actually occupy the desired square
        if new_square.get_piece() is not None and new_square.get_piece().get_color() == self.color:
            return {"valid": False, "piece taken": None}
        # Then check if there are other pieces in between the Rook and it's target location
        min_x = min(new_loc[0], loc[0])
        min_y = min(new_loc[1], loc[1])
        if x_dif == 0:
            for i in range(y_dif - 1):
                if grid[min_x][min_y + i + 1].get_piece() is not None:
                    return {"valid": False, "piece taken": None}
        elif y_dif == 0:
            for i in range(x_dif - 1):
                if grid[min_x + i + 1][min_y].get_piece() is not None:
                    return {"valid": False, "piece taken": None}
        else:  # should never happen
            return {"valid": False, "piece taken": None}
        # if we reach here, it means that the move is in a line and there is no blocking piece and the desired square
        # is obtainable by the rook
        # now we check if this moves does not put the king in check or if it does not take him out of check
        # if not then it is not valid
        simulated_data = self.simulate_move(new_square)
        if simulated_data.get("in check"):
            return {"valid": False, "piece taken": None}
        else:
            return {"valid": True, "piece taken": new_square.get_piece()}
