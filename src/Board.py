import pygame
from Piece import Piece


class Board(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load("../Display/Board.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]
        self.size = screen.get_size()
        self.grid = [[None] * 8 for _ in range(8)]
        screen.blit(self.image, self.rect)

    def is_square_empty(self, location):
        if self.grid[location[0]][location[1]] is None:
            return True
        else:
            return False

    def add_piece(self, piece):
        self.grid[piece.location[0]][piece.location[1]] = piece

    def remove_piece(self, piece):
        self.grid[piece.location[0]][piece.location[1]] = None

    def display_pieces(self):
        self.screen.blit(self.image, self.rect)
        for i in range(8):
            for k in range(8):
                if self.grid[i][k] is not None:
                    self.grid[i][k].display()
