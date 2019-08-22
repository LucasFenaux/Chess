import pygame
from pygame.locals import *
import sys
from Piece import Piece
from Board import Board


class Game:
    def __init__(self, background_screen, screen):
        self.background_screen = background_screen
        self.board = Board(screen)

    def display_game(self):
        self.background_screen.blit(pygame.transform.scale(self.board.screen, self.background_screen.get_size()), (0, 0))

    def start(self):
        self.display_game()
        grid = self.board.get_grid()
        # if grid[0][0].get_piece() is not None: print(grid[0][0].get_piece().get_square().get_location())
        print("-----------------------------------")
        piece = Piece(grid[0][0], 'white', self.board)
        # if grid[0][0].get_piece() is not None: print(grid[0][0].get_piece().get_square().get_location())
        piece.move(grid[1][0])
        print("-----------------------------------")
        # if grid[1][0].get_piece() is not None: print(grid[1][0].get_piece().get_square().get_location())
        # if grid[0][0].get_piece() is not None: print(grid[0][0].get_piece().get_square().get_location())
        self.board.update_board()
        self.display_game()
        i = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    new_size = event.dict['size']
                    self.background_screen = pygame.display.set_mode(new_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                    if i == 0:
                        piece.move(grid[1][1])
                        i = 1
                    else:
                        piece.move(grid[2][2])
                        i = 0
                    self.board.update_board()
                    self.display_game()
            pygame.display.flip()
