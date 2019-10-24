import pygame
from Piece import Piece


class King(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black King.png")
        else:
            self.image = pygame.image.load("../Display/White King.png")
        self.has_moved = False

    def check_if_move_is_valid(self, new_square, game_orientation, is_simulated):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()

        # check if target destination is an obtainable piece for the king
        if new_square.get_piece() is not None and new_square.get_piece().get_color() == self.color:
            return {"valid": False, "piece taken": None}

        # check for castle
        special_move_metadata = self.check_for_castle(new_square, is_simulated)
        if special_move_metadata.get("is_castle"):
            # simulate
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

    def check_for_castle(self, new_square, is_simulated):
        # can't castle if the king is in check
        player = self.board.game.get_player(self.color)
        # can't castle if the king has already moved
        if not self.has_moved:
            return {"is_castle": False, "return": {"valid": False, "piece taken": None}}

        # can't castle if there is no rook at the right position and if that rook has already moved

    def move(self, new_square, game_orientation):
        moved = super().move(new_square, game_orientation)
        if moved:
            self.has_moved = True
        return moved
