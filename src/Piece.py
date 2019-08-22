import pygame
from Custom_Exceptions import IllegalMoveError


class Piece(pygame.sprite.Sprite):
    def __init__(self, board_square, color, board):
        if not board_square.is_occupied():
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("../Display/Black Pawn.png")
            self.color = color
            self.board = board
            self.square = board_square
            self.square.replace(self)
        else:
            raise IllegalMoveError(
                "Can't spawn this piece at " + str(
                    board_square.get_location()) + " because another piece is already there")

    def update_location(self, new_square):
        self.square.replace(None)
        self.square = new_square
        self.square.replace(self)

    def check_if_move_is_valid(self, new_square):
        return True

    def move(self, new_square):
        if self.check_if_move_is_valid(new_square):
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
