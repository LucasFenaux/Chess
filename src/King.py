import pygame
from Piece import Piece
from Rook import Rook
from Square import Square


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
        # TODO: the recursion now works but it doesn't seem to return that an actual castle is valid

        special_move_metadata = self.check_for_castle(new_square)
        if special_move_metadata.get("is_and_can_castle"):
            if is_simulated:
                return {"valid": True, "piece taken": None}
            else:
                simulated_data = self.simulate_castle(new_square, special_move_metadata.get("rook", None))
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

    def check_for_castle(self, new_square):
        grid = new_square.board.get_grid()

        # can't castle if the king has already moved
        if self.has_moved:
            return {"is_and_can_castle": False, "rook": None, "return": {"valid": False, "piece taken": None}}

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

                # move is not valid if the king moves more than 2 tiles
                if x2 < new_x < x1 and x1 - x2 == 2:
                    # check if the way in between is clear
                    is_clear = True

                    for i in range(x2, x1):
                        if grid[i][y].get_piece() is not None:
                            is_clear = False

                    if is_clear:
                        castlelable_rook = rook
                        break

        if castlelable_rook is None:
            return {"is_and_can_castle": False, "rook": None, "return": {"valid": False, "piece taken": None}}
        else:
            return {"is_and_can_castle": True, "rook": castlelable_rook, "return": {"valid": True, "piece taken": None}}

    def move(self, new_square, game_orientation):
        test_move = self.check_if_move_is_valid(new_square, game_orientation, False)
        if test_move["valid"]:
            # check if the move is a castle, if so force move the rook
            check_castle = self.check_for_castle(new_square)
            if check_castle.get("is_and_can_castle"):
                # compute the new location of the rook
                rook = check_castle.get("rook")
                rook_loc = rook.get_square().get_location()
                loc = self.location
                new_loc = new_square.get_location()
                new_rook_loc = (0, 0)
                if rook_loc[1] > loc[1]:
                    new_rook_loc = (new_loc[0] - 1, new_loc[1])
                else:
                    new_rook_loc = (new_loc[0] + 1, new_loc[1])
                rook.update_location(new_rook_loc)

            self.board.handle_piece_taken(test_move.get("piece taken", None))
            self.update_location(new_square)
            moved = True
        else:
            moved = False

        if moved:
            self.has_moved = True
        return moved

    def simulate_castle(self, new_square, rook):
        # get objects we will need later
        game = self.board.get_game()
        grid = self.board.get_grid()

        # get the locations and squares of all the pieces that are going to "move"
        new_loc = new_square.get_location()
        cur_square = self.square
        loc = cur_square.get_location()
        rook_square = rook.get_square()
        rook_loc = rook_square.get_location()

        # compute the new location/square of the rook if he were to move
        new_rook_loc = (0, 0)
        if rook_loc[1] > loc[1]:
            new_rook_loc = (new_loc[0] - 1, new_loc[1])
        else:
            new_rook_loc = (new_loc[0] + 1, new_loc[1])
        new_rook_square = grid[new_rook_loc[0]][new_rook_loc[1]]
        changes_made = []  # list of dictionaries that store what pieces were changed and what was their original position

        # append the rook square, king square and the square we want to move the rook and king to
        changes_made.append({"square": new_square, "original loc": new_loc})
        changes_made.append({"square": cur_square, "original loc": loc})
        changes_made.append({"square": rook_square, "original loc": rook_loc})
        changes_made.append({"square": new_rook_square, "original loc": new_rook_loc})

        # force the move of the king
        grid[new_loc[0]][new_loc[1]] = cur_square
        cur_square.set_location(new_loc)
        king_filling_square = Square(self.board, loc, None)
        grid[loc[0]][loc[1]] = king_filling_square

        # force the move of the rook
        grid[new_rook_loc[0]][new_rook_loc[1]] = rook_square
        rook_square.set_location(new_rook_loc)
        rook_filling_square = Square(self.board, rook_loc, None)
        grid[rook_loc[0]][rook_loc[1]] = rook_filling_square

        # check if the player is in check
        color = cur_square.get_piece().get_color()
        # made a dictionary in case we want to add more metadata on the simulated move later
        in_check = {"in check": True}
        if game.player1.get_current_color() == color:
            if game.player1.check_if_in_check(True):
                in_check = {"in check": True}
            else:
                in_check = {"in check": False}
        else:
            if game.player2.check_if_in_check(True):
                in_check = {"in check": True}
            else:
                in_check = {"in check": False}

        # put everything back in its place
        for change in changes_made:
            square = change.get("square", None)
            loc = change.get("original loc", (0, 0))
            square.location = loc
            grid[loc[0]][loc[1]] = square

        return in_check
