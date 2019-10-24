import pygame
from pygame.locals import *
import sys
import random
from Board import Board
from PieceFactory import PieceFactory


class RegularGame:
    def __init__(self, background_screen, screen, player1, player2):
        self.background_screen = background_screen
        self.board = Board(screen, self)
        self.first_selected_square = None
        self.turn = 'white'
        self.state = 0
        self.scale = (screen.get_size()[0] / self.background_screen.get_size()[0],
                      screen.get_size()[1] / self.background_screen.get_size()[1])
        self.game_orientation = ""
        self.player1 = player1
        self.player2 = player2

    def display_game(self):
        self.background_screen.blit(pygame.transform.scale(self.board.screen, self.background_screen.get_size()),
                                    (0, 0))

    def populate_game(self):
        piece_factory = PieceFactory(self.board)
        i = random.uniform(0, 1)
        if i < 0.5:
            self.game_orientation = "wb"
            self.player1.set_game(self, "white")
            self.player2.set_game(self, "black")
            piece_factory.populate_regular_game_wb()
        else:
            self.game_orientation = "bb"
            self.player1.set_game(self, "black")
            self.player2.set_game(self, "white")
            piece_factory.populate_regular_game_bb()

    def handle_click(self, is_down):
        pos = pygame.mouse.get_pos()
        scaled_pos = (int(pos[0] * self.scale[0]), int(pos[1] * self.scale[1]))
        selected_square = None
        grid = self.board.get_grid()
        for square in self.board.get_squares():
            if square.rect.collidepoint(scaled_pos):
                selected_square = square
                break
        # first click of the turn
        if self.state == 0 and is_down:
            if selected_square.get_piece() is not None and selected_square.get_piece().get_color() == self.turn:
                self.first_selected_square = selected_square
                self.first_selected_square.highlight('selected')
                self.first_selected_square.get_piece().highlight_all_attackable_squares()
                self.state = 1
        # going up after the first click, which leads to either a drag or nothing
        elif self.state == 1 and not is_down:
            if selected_square != self.first_selected_square:
                moved = self.first_selected_square.get_piece().move(selected_square, self.game_orientation)
                if not moved:
                    print("invalid move, failed to move")
                else:
                    if self.turn == 'white':
                        self.turn = 'black'
                    else:
                        self.turn = 'white'
                    self.state = 0
                    # self.first_selected_square.un_highlight()
                    # self.first_selected_square.un_highlight_all_attackable_squares()
                    for i in range(8):
                        for j in range(8):
                            grid[i][j].un_highlight()
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
                # self.first_selected_square.un_highlight()
                for i in range(8):
                    for j in range(8):
                        grid[i][j].un_highlight()
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
                    # self.first_selected_square.un_highlight()
                    for i in range(8):
                        for j in range(8):
                            grid[i][j].un_highlight()
                    self.first_selected_square = None

    def take_piece(self, piece):
        if piece.get_color() == self.player1.get_current_color():
            self.player2.take_piece(piece)
        else:
            self.player1.take_piece(piece)

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
            if self.player1.is_in_checkmate(False):
                player = self.player2
                break
            elif self.player2.is_in_checkmate(False):
                player = self.player1
                break
            else:
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
        print("{} won".format(player.name))
        self.end_game(player)

    def display_end_game_screen(self, player):
        end_game_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_screen = end_game_font.render(
            '{} won! Congratulations! He has {} consecutive wins'.format(player.name, player.num_of_wins), False,
            (0, 0, 0))
        screen = self.board.screen
        size = screen.get_size()
        self.background_screen.blit(pygame.transform.scale(self.board.screen, self.background_screen.get_size()),
                                    (0, 0))

    def handle_end_game_click(self, is_down):
        pass

    def end_game(self, player):
        while 1:
            self.display_end_game_screen(player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    new_size = event.dict['size']
                    self.update_background_size(new_size)
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_end_game_click(True)
                elif event.type == MOUSEBUTTONUP:
                    self.handle_end_game_click(False)
            self.display_end_game_screen(player)

    def get_player(self, color):
        if self.player1.get_current_color() == color:
            return self.player1
        elif self.player2.get_current_color() == color:
            return self.player2
        else:
            return None