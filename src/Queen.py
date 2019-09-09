import pygame
from Piece import Piece


class Queen(Piece):
    def __init__(self, board_square, color, board):
        Piece.__init__(self, board_square, color, board)
        if color == 'black':
            self.image = pygame.image.load("../Display/Black Queen.png")
        else:
            self.image = pygame.image.load("../Display/White Queen.png")

    def check_if_move_is_valid(self, new_square, game_orientation):
        new_loc = new_square.get_location()
        loc = self.square.get_location()
        grid = self.board.get_grid()
        # check if the new square is obtainable by the Queen
        if new_square.get_piece() is not None and new_square.get_piece().get_color() == self.color:
            return {"valid": False, "piece taken": None}
        # check if the move is a bishop move
        x_dif = abs(new_loc[0] - loc[0])
        y_dif = abs(new_loc[1] - loc[1])
        if x_dif == y_dif:
            move_type = "bishop"
        elif x_dif == 0 and y_dif != 0:
            move_type = "rook"
        elif x_dif != 0 and y_dif == 0:
            move_type = "rook"
        else:
            move_type = ""
        if move_type == "":
            return {"valid": False, "piece taken": None}
        elif move_type == "bishop":
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
            # now we check if this moves does not put the king in check or if it does not take him out of check
            # if not then it is not valid
            simulated_data = self.simulate_move(new_square)
            if simulated_data.get("in check"):
                return {"valid": False, "piece taken": None}
            else:
                return {"valid": True, "piece taken": new_square.get_piece()}
        elif move_type == "rook":
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
            # if we reach here, it means that the move is a line and there is no blocking piece and the desired square
            # is obtainable by the rook
            # now we check if this moves does not put the king in check or if it does not take him out of check
            # if not then it is not valid
            simulated_data = self.simulate_move(new_square)
            if simulated_data.get("in check"):
                return {"valid": False, "piece taken": None}
            else:
                return {"valid": True, "piece taken": new_square.get_piece()}
        else:  # We should never but just in case
            return {"valid": False, "piece taken": None}
