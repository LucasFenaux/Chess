import pygame
from Custom_Exceptions import IllegalMoveError


class Piece(pygame.sprite.Sprite):
    def __init__(self, board_location, color, board):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Display/Black Pawn.png")
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [board_location[0] * int(board.size[0] / 8),
                                         board_location[1] * int(board.size[1] / 8)]
        self.board = board
        if self.board.is_square_empty(board_location):
            self.location = board_location
            self.board.add_piece(self)
        else:
            raise IllegalMoveError(
                "Can't spawn this piece at " + str(board_location) + " because another piece is already there")

    def update_location(self, new_location):
        self.board.remove_piece(self)
        self.location = new_location
        self.rect.left, self.rect.top = [new_location[0] * int(self.board.size[0] / 8),
                                         new_location[1] * int(self.board.size[1] / 8)]
        self.board.add_piece(self)

    def check_if_move_is_valid(self, new_location):
        return self.check_if_move_is_within_board(new_location)

    @staticmethod
    def check_if_move_is_within_board(new_location):
        if 0 <= new_location[0] <= 8 and 0 <= new_location[1] <= 8:
            return True
        else:
            print('Cannot move this piece to this position, it is outside the board')
            return False

    def move(self, new_location):
        if self.check_if_move_is_valid(new_location):
            self.update_location(new_location)
            return True
        else:
            return False

    def display(self):
        self.board.screen.blit(self.image, (self.rect.left, self.rect.top))
