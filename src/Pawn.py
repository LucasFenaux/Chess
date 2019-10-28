import pygame
from Piece import Piece
from Square import Square


class Pawn(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Pawn.png")
        else:
            self.image = pygame.image.load("../Display/White Pawn.png")
        self.has_moved = False

    def check_if_move_is_valid(self, new_square, game_orientation, is_simulated):
        if game_orientation == "wb":
            return self.check_for_move(new_square, "black", "white", is_simulated)
        elif game_orientation == "bb":
            return self.check_for_move(new_square, "white", "black", is_simulated)

    def check_for_move(self, new_square, color1, color2, is_simulated):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()

        if self.color == color1:
            if (new_loc[0], new_loc[1]) == (loc[0], loc[1] + 1):
                # move forward by 1 square
                if new_square.get_piece() is None:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}
                else:
                    return {"valid": False, "piece taken": None}

            elif (new_loc[0], new_loc[1]) == (loc[0], loc[1] + 2):
                # move forward by 2 squares if the pawn hasn't moved yet
                if self.has_moved:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                elif grid[loc[0]][loc[1] + 1].get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                else:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}

            elif (new_loc[0], new_loc[1]) == (loc[0] + 1, loc[1] + 1):
                # take a diagonal piece
                # first check if it an en-passant
                if new_square.get_piece() is None:
                    piece = grid[loc[0] + 1][loc[1]].get_piece()
                    if type(piece) == Pawn and piece.get_color() != self.color:
                        latest_move = self.board.get_game().get_player(piece.get_color()).get_current_latest_move()
                        # check if the last piece that the other player moved was the piece we got
                        if latest_move[1].get_piece() == piece:
                            lm_loc = latest_move[0].get_location()
                            lm_new_loc = latest_move[1].get_location()
                            # check if it moved 2 squares
                            if (lm_new_loc[0], lm_new_loc[1]) == (lm_loc[0], lm_loc[1] - 2):
                                if is_simulated:
                                    return {"valid": True, "piece taken": piece}
                                else:
                                    simulated_data = self.simulate_move(new_square, {"is_ep": True, "piece": piece})
                                    if simulated_data.get("in check"):
                                        return {"valid": False, "piece taken": None}
                                    else:
                                        return {"valid": True, "piece taken": piece}

                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color1:
                    return {"valid": False, "piece taken": None}
                else:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}

            elif (new_loc[0], new_loc[1]) == (loc[0] - 1, loc[1] + 1):
                # take a diagonal piece
                if new_square.get_piece() is None:
                    piece = grid[loc[0] - 1][loc[1]].get_piece()
                    if type(piece) == Pawn and piece.get_color() != self.color:
                        latest_move = self.board.get_game().get_player(piece.get_color()).get_current_latest_move()
                        # check if the last piece that the other player moved was the piece we got
                        if latest_move[1].get_piece() == piece:
                            lm_loc = latest_move[0].get_location()
                            lm_new_loc = latest_move[1].get_location()
                            # check if it moved 2 squares
                            if (lm_new_loc[0], lm_new_loc[1]) == (lm_loc[0], lm_loc[1] - 2):
                                if is_simulated:
                                    return {"valid": True, "piece taken": piece}
                                else:
                                    simulated_data = self.simulate_move(new_square, {"is_ep": True, "piece": piece})
                                    if simulated_data.get("in check"):
                                        return {"valid": False, "piece taken": None}
                                    else:
                                        return {"valid": True, "piece taken": piece}
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color1:
                    return {"valid": False, "piece taken": None}
                else:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}
            else:
                return {"valid": False, "piece taken": None}
        else:

            if (new_loc[0], new_loc[1]) == (loc[0], loc[1] - 1):
                # move forward by 1 square
                if new_square.get_piece() is None:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}
                else:
                    return {"valid": False, "piece taken": None}

            elif (new_loc[0], new_loc[1]) == (loc[0], loc[1] - 2):
                # move forward by 2 squares if the pawn hasn't moved yet
                if self.has_moved:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                elif grid[loc[0]][loc[1] - 1].get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                else:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}

            elif (new_loc[0], new_loc[1]) == (loc[0] - 1, loc[1] - 1):
                # take a diagonal piece
                if new_square.get_piece() is None:
                    piece = grid[loc[0] - 1][loc[1]].get_piece()
                    if type(piece) == Pawn and piece.get_color() != self.color:
                        latest_move = self.board.get_game().get_player(piece.get_color()).get_current_latest_move()
                        # check if the last piece that the other player moved was the piece we got
                        if latest_move[1].get_piece() == piece:
                            lm_loc = latest_move[0].get_location()
                            lm_new_loc = latest_move[1].get_location()
                            # check if it moved 2 squares
                            if (lm_new_loc[0], lm_new_loc[1]) == (lm_loc[0], lm_loc[1] + 2):
                                if is_simulated:
                                    return {"valid": True, "piece taken": piece}
                                else:
                                    simulated_data = self.simulate_move(new_square, {"is_ep": True, "piece": piece})
                                    if simulated_data.get("in check"):
                                        return {"valid": False, "piece taken": None}
                                    else:
                                        return {"valid": True, "piece taken": piece}
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color2:
                    return {"valid": False, "piece taken": None}
                else:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}

            elif (new_loc[0], new_loc[1]) == (loc[0] + 1, loc[1] - 1):
                # take a diagonal piece
                if new_square.get_piece() is None:
                    if new_square.get_piece() is None:
                        piece = grid[loc[0] + 1][loc[1]].get_piece()
                        if type(piece) == Pawn and piece.get_color() != self.color:
                            latest_move = self.board.get_game().get_player(piece.get_color()).get_current_latest_move()
                            # check if the last piece that the other player moved was the piece we got
                            if latest_move[1].get_piece() == piece:
                                lm_loc = latest_move[0].get_location()
                                lm_new_loc = latest_move[1].get_location()
                                # check if it moved 2 squares
                                if (lm_new_loc[0], lm_new_loc[1]) == (lm_loc[0], lm_loc[1] + 2):
                                    if is_simulated:
                                        return {"valid": True, "piece taken": piece}
                                    else:
                                        simulated_data = self.simulate_move(new_square, {"is_ep": True, "piece": piece})
                                        if simulated_data.get("in check"):
                                            return {"valid": False, "piece taken": None}
                                        else:
                                            return {"valid": True, "piece taken": piece}
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color2:
                    return {"valid": False, "piece taken": None}
                else:
                    if is_simulated:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                    else:
                        simulated_data = self.simulate_move(new_square, {"is_ep": False, "piece": None})
                        if simulated_data.get("in check"):
                            return {"valid": False, "piece taken": None}
                        else:
                            return {"valid": True, "piece taken": new_square.get_piece()}
            else:
                return {"valid": False, "piece taken": None}

    def simulate_move(self, new_square, en_passant):
        if not en_passant.get("is_ep"):
            return super().simulate_move(new_square)
        else:
            new_loc = new_square.get_location()
            cur_square = self.square
            loc = cur_square.get_location()
            piece_taken = en_passant.get("piece")
            pt_square = piece_taken.get_square()
            pt_loc = pt_square.get_location()
            changes_made = []  # list of dictionaries that store what pieces were changed and what was their original position
            changes_made.append({"square": new_square, "original loc": new_loc})
            changes_made.append({"square": cur_square, "original loc": loc})
            changes_made.append({"square": pt_square, "original loc": pt_loc})
            game = self.board.game
            grid = self.board.get_grid()

            # fill the square where the piece taken is supposed to be with an empty square
            empty_square = Square(self.board, pt_loc, None)
            grid[pt_loc[0]][pt_loc[1]] = empty_square

            # force the move by moving square around
            grid[new_loc[0]][new_loc[1]] = cur_square
            cur_square.set_location(new_loc)
            filling_square = Square(self.board, loc, None)
            grid[loc[0]][loc[1]] = filling_square
            color = cur_square.get_piece().get_color()

            # check if the player is in check
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

    def move(self, new_square, game_orientation):
        print(self.square.get_location())
        print(new_square.get_location())
        moved = super().move(new_square, game_orientation)
        if moved:
            self.has_moved = True
        return moved
