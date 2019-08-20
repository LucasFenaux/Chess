import pygame
import sys
from Piece import Piece
from Board import Board
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight


if __name__ == '__main__':
    pygame.init()

    size = width, height = 1024, 1024
    speed = [0, 0]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    screen.fill(black)
    BackGround = Board(screen)
    rook = Rook([0, 0], 'white', BackGround)
    ballrect = rook.rect
    rook.move([1, 0])
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            BackGround.display_pieces()
        pygame.display.flip()


