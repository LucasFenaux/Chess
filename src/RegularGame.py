import pygame
from pygame.locals import *
import sys
import time
import random
from Board import Board
from PieceFactory import PieceFactory


class RegularGame:
    def __init__(self, background_screen, screen, player1, player2):
        self.background_screen = background_screen
        self.board = Board(screen, self)
        self.current_order = -1
        self.first_selected_square = None
        self.turn = 'white'
        self.state = 0
        self.scale = (screen.get_size()[0] / self.background_screen.get_size()[0],
                      screen.get_size()[1] / self.background_screen.get_size()[1])
        self.game_orientation = ""
        self.player1 = player1
        self.player2 = player2
        self.end_game_data = {"replay_rect": None, "menu_rect": None}
        self.end_game_sprite = None
        self.end_game_screen = pygame.Surface(self.board.get_screen().get_size(), HWSURFACE | DOUBLEBUF | RESIZABLE)

    def display_game(self):
        self.background_screen.blit(pygame.transform.scale(self.board.screen, self.background_screen.get_size()),
                                    (0, 0))

    def populate_game(self, order):
        piece_factory = PieceFactory(self.board)
        i = random.uniform(0, 1)
        if order == 0:
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

    def start(self, order):
        self.current_order = order
        self.populate_game(order)
        self.display_game()
        self.board.update_board()
        self.display_game()

        # display the name of each of the players then remove them after the first click
        # so that they know where they are
        self.display_names_at_start()

        # have the game start
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
                        pygame.quit()
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

    ''' Starts a new game after at least 1 other game was just player
    Do not use if no game was already played'''
    def start_new_game(self):
        # cleanup the board
        self.board.cleanup_board()
        self.state = 0
        self.turn = "white"
        if self.current_order == 0:
            self.current_order = 1
        else:
            self.current_order = 0
        self.start(self.current_order)

    def display_end_game_screen(self, winner):
        self.end_game_screen.blit(pygame.transform.scale(self.end_game_sprite, self.end_game_screen.get_size()), (0, 0))
        end_game_font = pygame.font.SysFont('Comic Sans MS', 30)
        screen_size = self.end_game_screen.get_size()

        # create congratulations text
        congrats_text = end_game_font.render(
            ' {} won! Congratulations! '.format(winner.name), False, (0, 0, 0))

        congrats_rect = congrats_text.get_rect()
        congrats_size = congrats_rect.size
        # create score texts

        most_wins = max(self.player1.num_of_wins, self.player2.num_of_wins)
        if self.player1.num_of_wins == most_wins:
            most_wins_player = self.player1
            least_wins_player = self.player2
        else:
            most_wins_player = self.player2
            least_wins_player = self.player1

        first_score_text = end_game_font.render(
            ' {} has {} wins '.format(most_wins_player.name, most_wins_player.num_of_wins), False, (0, 0, 0))
        first_score_rect = first_score_text.get_rect()
        first_score_size = first_score_rect.size

        second_score_text = end_game_font.render(
            ' {} has {} wins '.format(least_wins_player.name, least_wins_player.num_of_wins), False, (0, 0, 0))
        second_score_rect = second_score_text.get_rect()
        second_score_size = second_score_rect.size

        # create play again button
        replay_button = end_game_font.render(
            ' Play Again ', False, (0, 0, 0)
        )
        replay_rect = replay_button.get_rect()
        replay_size = replay_rect.size

        # create the go back to menu button
        menu_button = end_game_font.render(
            ' Go Back To Menu ', False, (0, 0, 0)
        )
        menu_rect = menu_button.get_rect()
        menu_size = menu_rect.size

        # compute the center (positions) of each button/text
        total_y_size = congrats_size[1] + replay_size[1] + menu_size[1] + first_score_size[1] + second_score_size[1]
        increment_size = (screen_size[1] - total_y_size) // 10
        congrats_rect.center = (screen_size[0] // 2, (screen_size[1] - total_y_size) // 3)
        first_score_rect.center = (screen_size[0] // 2, congrats_rect.center[1] + (first_score_size[1] // 2)
                                   + increment_size)
        second_score_rect.center = (screen_size[0] // 2, first_score_rect.center[1] + (second_score_size[1] // 2)
                                    + increment_size)
        replay_rect.center = (screen_size[0] // 2, second_score_rect.center[1] + (replay_size[1] // 2) + increment_size)
        menu_rect.center = (screen_size[0] // 2, replay_rect.center[1] + (menu_size[1] // 2) + increment_size)

        # save the rectangles for handling clicks
        self.end_game_data["replay_rect"] = replay_rect
        self.end_game_data["menu_rect"] = menu_rect

        # blit the texts on screen
        self.end_game_screen.blit(first_score_text, first_score_rect)
        self.end_game_screen.blit(second_score_text, second_score_rect)
        self.end_game_screen.blit(menu_button, menu_rect)
        self.end_game_screen.blit(congrats_text, congrats_rect)
        self.end_game_screen.blit(replay_button, replay_rect)

        # draw the squares around the two buttons
        pygame.draw.rect(self.end_game_screen, (0, 0, 0), replay_rect, 2)
        pygame.draw.rect(self.end_game_screen, (0, 0, 0), menu_rect, 2)

        # blit it all on the background_screen
        self.background_screen.blit(pygame.transform.scale(self.end_game_screen, self.background_screen.get_size()),
                                    (0, 0))
        pygame.display.flip()

    def handle_end_game_click(self, is_down):
        pos = pygame.mouse.get_pos()
        scaled_pos = (int(pos[0] * self.scale[0]), int(pos[1] * self.scale[1]))
        selected = None

        # check if the replay button was selected
        if self.end_game_data["replay_rect"].collidepoint(scaled_pos):
            selected = "replay"
        elif self.end_game_data["menu_rect"].collidepoint(scaled_pos):
            selected = "menu"
        else:
            return

        if selected == "replay":
            self.start_new_game()
        elif selected == "menu":
            # TODO: add a menu page
            sys.exit()
        else:   # we should never reach here
            sys.exit()

    def end_game(self, player):
        player.num_of_wins += 1
        pygame.image.save(self.background_screen, "../Display/end_game_screen.png")
        time.sleep(0.5)
        self.end_game_sprite = pygame.image.load("../Display/end_game_screen.png")

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
                pygame.display.flip()
            self.display_end_game_screen(player)

    def display_names_at_start(self):
        name_font = pygame.font.SysFont('Comic Sans MS', 30)
        screen_size = self.end_game_screen.get_size()

        player1_text = name_font.render(
            " {} ".format(self.player1.get_name()), False, (0, 0, 0))
        player1_rect = player1_text.get_rect()
        player1_rect.center = (screen_size[0] // 2, screen_size[1] - player1_rect.size[1] - (9*screen_size[1]) // 10)

        player2_text = name_font.render(
            " {} ".format(self.player2.get_name()), False, (0, 0, 0))
        player2_rect = player2_text.get_rect()
        player2_rect.center = (screen_size[0] // 2, screen_size[1] + player2_rect.size[1] - (screen_size[1] // 10))
        screen = self.board.get_screen()

        while 1:
            self.board.update_board()
            screen.blit(player1_text, player1_rect)
            screen.blit(player2_text, player2_rect)
            self.display_game()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    new_size = event.dict['size']
                    self.update_background_size(new_size)
                elif event.type == MOUSEBUTTONDOWN:
                    return
                elif event.type == MOUSEBUTTONUP:
                    return

    def get_player(self, color):
        if self.player1.get_current_color() == color:
            return self.player1
        elif self.player2.get_current_color() == color:
            return self.player2
        else:
            return None