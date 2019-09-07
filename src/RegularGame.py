import pygame
from pygame.locals import *
import sys
import random
from Board import Board
from PieceFactory import PieceFactory


class RegularGame:
    def __init__(self, background_screen, screen):
        self.background_screen = background_screen
        self.board = Board(screen, self)
        self.first_selected_square = None
        self.turn = 'white'
        self.state = 0
        self.scale = (screen.get_size()[0] / self.background_screen.get_size()[0],
                      screen.get_size()[1] / self.background_screen.get_size()[1])
        self.game_orientation = ""
        self.white_pieces_taken = []
        self.black_pieces_taken = []

    def display_game(self):
        self.background_screen.blit(pygame.transform.scale(self.board.screen, self.background_screen.get_size()),
                                    (0, 0))

    def populate_game(self):
        piece_factory = PieceFactory(self.board)
        i = random.uniform(0, 1)
        # if i < 0.5:
        piece_factory.populate_regular_game_wb()
        self.game_orientation = "wb"
        # else:
        #     piece_factory.populate_regular_game_bb()
        #     self.game_orientation = "bb"

    def handle_click(self, is_down):
        pos = pygame.mouse.get_pos()
        scaled_pos = (int(pos[0] * self.scale[0]), int(pos[1] * self.scale[1]))
        selected_square = None
        for square in self.board.get_squares():
            if square.rect.collidepoint(scaled_pos):
                selected_square = square
                break
        # first click of the turn
        if self.state == 0 and is_down:
            if selected_square.get_piece() is not None and selected_square.get_piece().get_color() == self.turn:
                self.first_selected_square = selected_square
                self.first_selected_square.highlight('selected')
                self.state = 1
        # going up after the first click, which leads to either a drag or nothing
        elif self.state == 1 and not is_down:
            if selected_square != self.first_selected_square:
                moved = self.first_selected_square.get_piece().move(selected_square, self.game_orientation)
                print(moved)
                if not moved:
                    print("invalid move, failed to move")
                else:
                    if self.turn == 'white':
                        self.turn = 'black'
                    else:
                        self.turn = 'white'
                    self.state = 0
                    self.first_selected_square.un_highlight()
            else:
                self.state = 2
        # the second click of the turn/process, right now do nothing because we act only when the player releases the
        # button (this allows to add something at this moment, maybe coloring
        elif self.state == 2 and is_down:
            self.state = 3
        # the release of the second click
        elif self.state == 3 and not is_down:
            # the player clicked again on the same piece -> unselect it
            if self.first_selected_square == selected_square:
                self.first_selected_square.un_highlight()
                self.first_selected_square = None
                self.state = 0
            # move
            else:
                moved = self.first_selected_square.get_piece().move(selected_square, self.game_orientation)
                if not moved:
                    print("invalid move, failed to move")
                else:
                    if self.turn == 'white':
                        self.turn = 'black'
                    else:
                        self.turn = 'white'
                    self.state = 0
                    self.first_selected_square.un_highlight()
                    self.first_selected_square = None

    def take_piece(self, piece):
        if piece.get_color() == "black":
            self.black_pieces_taken.append(piece)
        else:
            self.white_pieces_taken.append(piece)
        print(self.white_pieces_taken)
        print(self.black_pieces_taken)

    def update_background_size(self, new_size):
        self.background_screen = pygame.display.set_mode(new_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.scale = (self.board.get_size()[0] / self.background_screen.get_size()[0],
                      self.board.get_size()[1] / self.background_screen.get_size()[1])

    def start(self):
        self.populate_game()
        self.display_game()
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
