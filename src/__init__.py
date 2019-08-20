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

    rook = Knight([0, 0], 'white')
    ballrect = rook.rect
    BackGround = Board()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(BackGround.image, BackGround.rect)
        screen.blit(rook.image, ballrect)
        pygame.display.flip()


