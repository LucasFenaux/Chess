import pygame


class Square(pygame.sprite.Sprite):
    def __init__(self, board, location, piece):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.location = location
        self.piece = piece
        square_size = int(self.board.get_size()[1] / 8)
        self.rect = pygame.Rect(location[0] * square_size, location[1] * square_size, square_size, square_size)
        self.highlighted = False
        self.highlight_color = None

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

    def highlight(self, type):
        if not self.highlighted:
            if type == 'selected':
                self.highlight_color = (0, 0, 255)
                self.highlighted = True
            elif type == 'move':
                self.highlight_color = (0, 128, 0)
                self.highlighted = True
            elif type == 'in check':
                self.highlight_color = (255, 0, 0)
                self.highlighted = True

    def un_highlight(self):
        self.highlighted = False
        self.highlight_color = None

    def display_highlight(self):
        if self.highlighted and self.highlight_color is not None:
            pygame.draw.rect(self.board.get_screen(), self.highlight_color, self.rect, 1)

    def get_piece(self):
        return self.piece

    def get_location(self):
        return self.location

    def get_rect(self):
        return self.rect

    def get_screen_position(self):
        return (self.rect.left, self.rect.top)
