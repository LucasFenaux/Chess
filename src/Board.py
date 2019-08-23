import pygame
from Piece import Piece
from Square import Square


class Board(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load("../Display/Board.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]
        self.size = screen.get_size()
        self.grid = self.fill_grid_with_empty_squares()

    def is_square_occupied(self, location):
        return self.grid[location[0]][location[1]].is_occupied()

    def add_piece(self, piece):
        self.grid[piece.location[0]][piece.location[1]].replace(piece)

    def remove_piece(self, piece):
        self.grid[piece.location[0]][piece.location[1]].replace(None)

    def update_board(self):
        self.display_board()
        self.display_pieces()

    def display_board(self):
        self.screen.blit(self.image, (0, 0))

    def display_pieces(self):
        for i in range(8):
            for k in range(8):
                if self.grid[i][k].get_piece() is not None:
                    self.grid[i][k].get_piece().display()

    def fill_grid_with_empty_squares(self):
        grid = [[None] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                grid[i][j] = Square(self, [i, j], None)
        return grid

    def get_size(self):
        return self.size

    def get_grid(self):
        return self.grid

    def get_squares(self):
        all_squares= []
        for i in range(8):
            for j in range(8):
                all_squares.append(self.grid[i][j])
        return all_squares
