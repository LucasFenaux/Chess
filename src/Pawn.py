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
            return self.check_for_move(new_square, "black", "white")
        elif game_orientation == "bb":
            return self.check_for_move(new_square, "white", "black")

    def check_for_move(self, new_square, color1, color2):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()
        if self.color == color1:
            if (new_loc[0], new_loc[1]) == (loc[0], loc[1] + 1):  # move forward by 1 square
                if new_square.get_piece() is None:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                else:
                    return {"valid": False, "piece taken": None}
            elif (new_loc[0], new_loc[1]) == (
                    loc[0], loc[1] + 2):  # move forward by 2 squares if the pawn hasn't moved yet
                if self.has_moved:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                elif grid[loc[0]][loc[1] + 1].get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
            elif (new_loc[0], new_loc[1]) == (loc[0] + 1, loc[1] + 1):  # take a diagonal piece
                if new_square.get_piece() is None:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color1:
                    return {"valid": False, "piece taken": None}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
            elif (new_loc[0], new_loc[1]) == (loc[0] - 1, loc[1] + 1):  # take a diagonal piece
                if new_square.get_piece() is None:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color1:
                    return {"valid": False, "piece taken": None}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
            else:
                return {"valid": False, "piece taken": None}
        else:
            if (new_loc[0], new_loc[1]) == (loc[0], loc[1] - 1):  # move forward by 1 square
                if new_square.get_piece() is None:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
                else:
                    return {"valid": False, "piece taken": None}
            elif (new_loc[0], new_loc[1]) == (
                    loc[0], loc[1] - 2):  # move forward by 2 squares if the pawn hasn't moved yet
                if self.has_moved:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                elif grid[loc[0]][loc[1] - 1].get_piece() is not None:
                    return {"valid": False, "piece taken": None}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
            elif (new_loc[0], new_loc[1]) == (loc[0] - 1, loc[1] - 1):  # take a diagonal piece
                if new_square.get_piece() is None:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color2:
                    return {"valid": False, "piece taken": None}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
            elif (new_loc[0], new_loc[1]) == (loc[0] + 1, loc[1] - 1):  # take a diagonal piece
                if new_square.get_piece() is None:
                    return {"valid": False, "piece taken": None}
                elif new_square.get_piece().get_color() == color2:
                    return {"valid": False, "piece taken": None}
                else:
                    simulated_data = self.simulate_move(new_square)
                    if simulated_data.get("in check"):
                        return {"valid": False, "piece taken": None}
                    else:
                        return {"valid": True, "piece taken": new_square.get_piece()}
            else:
                return {"valid": False, "piece taken": None}

    def move(self, new_square, game_orientation):
        moved = super().move(new_square, game_orientation)
        if moved:
            self.has_moved = True
        return moved
