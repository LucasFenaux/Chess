import pygame
from Square import Square
from Custom_Exceptions import IllegalMoveError


class Piece(pygame.sprite.Sprite):
    def __init__(self, board_square, color, board):
        if not board_square.is_occupied():
            pygame.sprite.Sprite.__init__(self)
            self.color = color
            self.board = board
            self.square = board_square
            self.square.replace(self)
            self.image = None
            self.attackable_squares = []
        else:
            raise IllegalMoveError(
                "Can't spawn this piece at " + str(
                    board_square.get_location()) + " because another piece is already there")

    def update_location(self, new_square):
        self.square.replace(None)
        self.square = new_square
        self.square.replace(self)

    def check_if_move_is_valid(self, new_square, game_orientation, is_simulated):
        return {"valid": False, "piece taken": None}

    def simulate_move(self, new_square):
        # get the locations and squares of all the pieces that are going to "move"
        new_loc = new_square.get_location()
        cur_square = self.square
        loc = cur_square.get_location()
        changes_made = []  # list of dictionaries that store what pieces were changed and what was their original position
        changes_made.append({"square": new_square, "original loc": new_loc})
        changes_made.append({"square": cur_square, "original loc": loc})
        game = self.board.game
        grid = self.board.get_grid()

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

    def update_attackable_squares(self, is_simulated):
        attackable_squares = []
        grid = self.board.get_grid()

        for i in range(8):
            for j in range(8):
                test_move = self.check_if_move_is_valid(grid[i][j], self.board.game.game_orientation, is_simulated)
                if test_move.get("valid", False):
                    attackable_squares.append(grid[i][j])

        self.attackable_squares = attackable_squares

    def highlight_all_attackable_squares(self):
        self.update_attackable_squares(False)
        for square in self.attackable_squares:
            square.highlight("move")

    def un_highlight_all_attackable_squares(self):
        for square in self.attackable_squares:
            square.un_highlight()

    def get_attackable_squares(self):
        return self.attackable_squares

    def move(self, new_square, game_orientation):
        test_move = self.check_if_move_is_valid(new_square, game_orientation, False)
        if test_move["valid"]:
            self.board.handle_piece_taken(test_move.get("piece taken", None))
            self.update_location(new_square)
            return True
        else:
            return False

    def display(self):
        rect = self.square.get_screen_position()
        self.board.screen.blit(self.image, rect)

    def get_color(self):
        return self.color

    def get_square(self):
        return self.square
