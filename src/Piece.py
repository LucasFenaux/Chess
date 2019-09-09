import pygame
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

    def check_if_move_is_valid(self, new_square, game_orientation):
        return {"valid": False, "piece taken": None}

    def update_attackable_squares(self):
        attackable_squares = []
        grid = self.board.get_grid()
        for i in range(8):
            for j in range(8):
                test_move = self.check_if_move_is_valid(grid[i][j], self.board.game.game_orientation)
                if test_move.get("valid", False):
                    attackable_squares.append(grid[i][j])
        self.attackable_squares = attackable_squares

    def get_attackable_squares(self):
        return self.attackable_squares

    def move(self, new_square, game_orientation):
        test_move = self.check_if_move_is_valid(new_square, game_orientation)
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
