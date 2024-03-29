import pygame
from pygame.locals import *
import os
import ctypes
from RegularGame import RegularGame
from Player import Player


black = 0, 0, 0
screen_size = (1024, 1024)


def microsoft_set_up():
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # centers the window
    user32 = ctypes.windll.user32
    screensize = (int(user32.GetSystemMetrics(0) - user32.GetSystemMetrics(0) / 4),  # proper proportions
                  int(user32.GetSystemMetrics(1) - user32.GetSystemMetrics(1) / 8))  # leaves some breathing room
    return screensize


def start_regular_game():
    pygame.init()
    pygame.font.init()
    background_screen_size = microsoft_set_up()
    background_screen = pygame.display.set_mode(screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
    background_screen.fill(black)
    screen = background_screen.copy()
    background_screen = pygame.display.set_mode(background_screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
    player1 = Player("player1")
    player2 = Player("player2")
    game = RegularGame(background_screen, screen, player1, player2)
    game.start(0)


if __name__ == '__main__':
    start_regular_game()
