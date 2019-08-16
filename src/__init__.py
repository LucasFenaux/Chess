import pygame
import sys


class Ship(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


if __name__ == '__main__':
    pygame.init()

    size = width, height = 1024, 1024
    speed = [0, 0]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    pawn = pygame.image.load("../Display/Black Rook.png")
    ballrect = pawn.get_rect()
    BackGround = Background('../Display/Board.png', [0, 0])
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
        screen.blit(pawn, ballrect)
        pygame.display.flip()


