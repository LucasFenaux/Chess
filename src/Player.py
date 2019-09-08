import pygame


class Player:
    def __init__(self, name):
        self.name = name
        self.current_game_info = {"current game": None, "current color": "", "pieces taken": []}
        self.num_of_wins = 0

    def set_game(self, game, color):
        self.current_game_info["current game"] = game
        self.current_game_info["current color"] = color
        self.current_game_info["pieces taken"] = []

    def winner(self):
        self.num_of_wins += 1

    def take_piece(self, piece):
        self.current_game_info.get("pieces taken", []).append(piece)

    def get_current_game(self):
        return self.current_game_info.get("current game", None)

    def get_current_color(self):
        return self.current_game_info.get("current color", "")

    def get_current_pieces_taken(self):
        return self.current_game_info.get("pieces taken", [])
