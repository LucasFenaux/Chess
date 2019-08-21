import pygame
from pygame.locals import *
import sys
import os
import ctypes
from Piece import Piece
from Board import Board
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight


def set_up_game():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # centers the window
    black = 0, 0, 0
    user32 = ctypes.windll.user32
    screensize = (int(user32.GetSystemMetrics(0) - user32.GetSystemMetrics(0) / 8),
                  int(user32.GetSystemMetrics(1) - user32.GetSystemMetrics(1) / 8))  # leaves some breathing room
    screen_size = (1024, 1024)
    background_screen_size = screensize
    background_screen = pygame.display.set_mode(screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
    background_screen.fill(black)
    screen = background_screen.copy()
    background_screen = pygame.display.set_mode(background_screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
    background_screen.blit(pygame.transform.scale(screen, background_screen_size), (0, 0))
    background = Board(screen)
    rook = Rook([0, 0], 'white', background)
    rook.move([1, 0])
    i = 0
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == VIDEORESIZE:
                new_size = event.dict['size']
                background_screen = pygame.display.set_mode(new_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                if i == 0:
                    rook.move([1, 1])
                    i = 1
                else:
                    rook.move([2, 2])
                    i = 0
                background.update_board()
                background_screen.blit(pygame.transform.scale(screen, event.dict['size']), (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    set_up_game()
