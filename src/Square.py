import pygame


class Square(pygame.sprite.Sprite):
    def __init__(self, board, location, piece):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.location = location
        self.piece = piece
        self.rect = pygame.rect
        self.rect.left, self.rect.top = [location[0] * int(self.board.get_size()[0] / 8),
                                         location[1] * int(self.board.get_size()[1] / 8)]

        print([self.rect.left, self.rect.top])

    def is_occupied(self):
        if self.piece is None:
            return False
        else:
            return True

    """replaces the piece at this square with the given new_piece and returns the removed piece"""
    def replace(self, new_piece):
        previous_piece = self.piece
        self.piece = new_piece
        return previous_piece

    def get_piece(self):
        return self.piece

    def get_location(self):
        return self.location

    def get_rect(self):
        return self.rect
