import pygame
from Square import Square


class Board(pygame.sprite.Sprite):
    def __init__(self, screen, game):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load("../Display/Board.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]
        self.size = screen.get_size()
        self.grid = self.fill_grid_with_empty_squares()
        self.game = game

    def is_square_occupied(self, location):
        return self.grid[location[0]][location[1]].is_occupied()

    def add_piece(self, piece, square):
        self.grid[square.get_location()[0]][square.get_location()[1]].replace(piece)

    def remove_piece(self, square):
        self.grid[square.get_location()[0]][square.get_location()[1]].replace(None)

    def update_board(self):
        self.display_board()
        self.display_pieces()
        self.display_highlighted()

    def display_board(self):
        self.screen.blit(self.image, (0, 0))

    def display_pieces(self):
        for i in range(8):
            for k in range(8):
                if self.grid[i][k].get_piece() is not None:
                    self.grid[i][k].get_piece().display()

    def display_highlighted(self):
        for square in self.get_squares():
            if square.highlighted:
                square.display_highlight()

    def fill_grid_with_empty_squares(self):
        grid = [[None] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                grid[i][j] = Square(self, [i, j], None)
        return grid

    def cleanup_board(self):
        new_grid = self.fill_grid_with_empty_squares()
        self.grid = new_grid

    def update_latest_move(self, player_color, initial_square, new_square):
        player = self.game.get_player(player_color)
        player.set_current_latest_move((initial_square, new_square))

    def handle_piece_taken(self, piece):
        if piece is not None:
            self.game.take_piece(piece)
            self.remove_piece(piece.get_square())

    def get_size(self):
        return self.size

    def get_grid(self):
        return self.grid

    def get_screen(self):
        return self.screen

    def get_game(self):
        return self.game

    def get_squares(self):
        all_squares = []
        for i in range(8):
            for j in range(8):
                all_squares.append(self.grid[i][j])
        return all_squares
