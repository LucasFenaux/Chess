import pygame
from Piece import Piece
from Rook import Rook


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
        if special_move_metadata.get("can_castle"):
            if is_simulated:
                return {"valid": True, "piece taken": None}
            else:
                simulated_data = self.simulate_castle(new_square)
                if simulated_data.get("in check"):
                    return {"valid": False, "piece taken": None}
                else:
                    return {"valid": True, "piece taken": None}

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
        grid = new_square.board.get_grid()
        # can't castle if the king is in check
        player = self.board.game.get_player(self.color)
        if player.check_if_in_check(is_simulated):
            return {"can_castle": False, "return": {"valid": False, "piece taken": None}}

        # can't castle if the king has already moved
        if self.has_moved:
            return {"can_castle": False, "return": {"valid": False, "piece taken": None}}

        # can't castle if there is no rook at the right position and if that rook has already moved
        # finding all the rooks that haven't moved yet:
        rooks = []
        for i in range(8):
            for j in range(8):
                piece = grid[i][j].get_piece()
                if type(piece) == Rook and not piece.has_moved:
                    rooks.append(piece)
        x, y = self.square.get_location()
        # find which rook the player would want to castle with
        castlelable_rook = None
        for rook in rooks:
            rx, ry = rook.square.get_location()
            if ry == y:
                x1 = max(rx, x)
                x2 = min(rx, x)
                new_x, new_y = new_square.get_location()
                if x2 < new_x < x1:
                    # check if the way in between is clear


                    castlelable_rook = rook
                    break
        if castlelable_rook is None:
            return {"can_castle": False, "return": {"valid": False, "piece taken": None}}


    def move(self, new_square, game_orientation):
        moved = super().move(new_square, game_orientation)
        if moved:
            self.has_moved = True
        return moved

    def simulate_castle(self, new_square):
        new_loc = new_square.get_location()
        cur_square = self.square
        loc = cur_square.get_location()
        changes_made = []  # list of dictionaries that store what pieces were changed and what was their original position
