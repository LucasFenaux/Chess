import pygame
from pygame.locals import *
import sys
from Piece import Piece
from Board import Board

from Rook import Rook


class Game:
    def __init__(self, background_screen, screen):
        self.background_screen = background_screen
        self.board = Board(screen)
        self.first_selected_square = None
        self.scale = (screen.get_size()[0] / self.background_screen.get_size()[0],
                      screen.get_size()[1] / self.background_screen.get_size()[1])

    def display_game(self):
        self.background_screen.blit(pygame.transform.scale(self.board.screen, self.background_screen.get_size()),
                                    (0, 0))

    def handle_click(self, first_click):
        pos = pygame.mouse.get_pos()
        scaled_pos = (int(pos[0] * self.scale[0]), int(pos[1] * self.scale[1]))
        selected_square = None
        for square in self.board.get_squares():
            if square.rect.collidepoint(scaled_pos):
                selected_square = square
                break
        no_sq_or_no_piece = self.first_selected_square is None or self.first_selected_square.get_piece() is None
        if no_sq_or_no_piece and first_click:
            self.first_selected_square = selected_square
        elif not no_sq_or_no_piece and not first_click:
            moved = self.first_selected_square.get_piece().move(selected_square)
            if not moved:
                print("invalid move, failed to move")

    def update_background_size(self, new_size):
        self.background_screen = pygame.display.set_mode(new_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.scale = (self.board.get_size()[0] / self.background_screen.get_size()[0],
                      self.board.get_size()[1] / self.background_screen.get_size()[1])

    def start(self):
        self.display_game()
        grid = self.board.get_grid()
        Rook(grid[0][0], 'white', self.board)
        self.board.update_board()
        self.display_game()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    new_size = event.dict['size']
                    self.update_background_size(new_size)
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(True)
                elif event.type == MOUSEBUTTONUP:
                    self.handle_click(False)
                self.board.update_board()
                self.display_game()
            pygame.display.flip()
