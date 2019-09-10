import pygame
from Piece import Piece


class Bishop(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Bishop.png")
        else:
            self.image = pygame.image.load("../Display/White Bishop.png")

    def check_if_move_is_valid(self, new_square, game_orientation, is_simulated):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()
        # check if target destination is an obtainable piece for the rook
        if new_square.get_piece() is not None and new_square.get_piece().get_color() == self.color:
            return {"valid": False, "piece taken": None}
        # check if the move is actually in a diagonal
        x_dif = abs(new_loc[0] - loc[0])
        y_dif = abs(new_loc[1] - loc[1])
        if x_dif != y_dif:
            return {"valid": False, "piece taken": None}
        # check if there are pieces blocking the bishop on its way
        if new_loc[0] > loc[0]:
            if new_loc[1] > loc[1]:
                for i in range(x_dif - 1):
                    if grid[loc[0] + i + 1][loc[1] + i + 1].get_piece() is not None:
                        return {"valid": False, "piece taken": None}
            else:
                for i in range(x_dif - 1):
                    if grid[loc[0] + i + 1][loc[1] - i - 1].get_piece() is not None:
                        return {"valid": False, "piece taken": None}
        else:
            if new_loc[1] > loc[1]:
                for i in range(x_dif - 1):
                    if grid[loc[0] - i - 1][loc[1] + i + 1].get_piece() is not None:
                        return {"valid": False, "piece taken": None}
            else:
                for i in range(x_dif - 1):
                    if grid[loc[0] - i - 1][loc[1] - i - 1].get_piece() is not None:
                        return {"valid": False, "piece taken": None}
        # if we reach here, it means that there is no piece blocking the bishop and hence his move is valid
        # now we check if this moves does not put the king in check or if it does not take him out of check, if not
        # then it is not valid
        if is_simulated:
            return {"valid": True, "piece taken": new_square.get_piece()}
        else:
            simulated_data = self.simulate_move(new_square)
            if simulated_data.get("in check"):
                return {"valid": False, "piece taken": None}
            else:
                return {"valid": True, "piece taken": new_square.get_piece()}
