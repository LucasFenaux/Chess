import pygame
from Piece import Piece


class Knight(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Knight.png")
        else:
            self.image = pygame.image.load("../Display/White Knight.png")

    def check_if_move_is_valid(self, new_square, game_orientation, is_simulated):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        possible_actions = [(1, 2), (-1, 2), (2, 1), (-2, 1), (2, -1), (-2, -1), (1, -2), (-1, -2)]
        # check if square is obtainable by the knight
        if new_square.get_piece() is not None and new_square.get_piece().get_color() == self.color:
            return {"valid": False, "piece taken": None}
        # check if the move follows a valid pattern
        for action in possible_actions:
            if (loc[0] + action[0], loc[1] + action[1]) == (new_loc[0], new_loc[1]):
                # now we check if this moves does not put the king in check or if it does not take him out of check
                # if not then it is not valid
                if is_simulated:
                    return {"valid": True, "piece taken": new_square.get_piece()}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
        # if we reach here, it means the move was not in the allowed list of patterns
        return {"valid": False, "piece taken": None}
