import pygame


class Square(pygame.sprite.Sprite):
    def __init__(self, board, location, piece):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.location = location
        self.piece = piece
        square_size = int(self.board.get_size()[1] / 8)
        self.rect = pygame.Rect(location[0] * square_size, location[1] * square_size, square_size, square_size)

    def is_occupied(self):
        if self.piece is None:
            return False
        else:
            print(self.piece)
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

    def get_screen_position(self):
        return (self.rect.left, self.rect.top)
