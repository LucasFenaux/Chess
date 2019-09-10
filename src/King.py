import pygame
from Piece import Piece


class King(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black King.png")
        else:
            self.image = pygame.image.load("../Display/White King.png")

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
        if x_dif <= 1 and y_dif <= 1 and (x_dif, y_dif) != (0, 0):
            if is_simulated:
                return {"valid": True, "piece taken": new_square.get_piece()}
            else:
                simulated_data = self.simulate_move(new_square)
                if simulated_data.get("in check"):
                    return {"valid": False, "piece taken": None}
                else:
                    return {"valid": True, "piece taken": new_square.get_piece()}
        else:
            return {"valid": False, "piece taken": None}
