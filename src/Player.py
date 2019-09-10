

class Player:
    def __init__(self, name):
        self.name = name
        self.current_game_info = {"current game": None, "current color": "", "pieces taken": []}
        self.num_of_wins = 0
        self.attackable_squares = []
        self.king = None  # a pointer to the player's king piece

    def update_attackable_squares(self, is_simulated):
        grid = self.current_game_info.get("current game", None).board.get_grid()
        attackable_squares = []
        for i in range(8):
            for j in range(8):
                square = grid[i][j]
                if square.get_piece() is not None and square.get_piece().get_color() == self.current_game_info.get(
                                                                                        "current color", ""):
                    square.get_piece().update_attackable_squares(is_simulated)
                    for att in square.get_piece().get_attackable_squares():
                        if att not in attackable_squares:
                            attackable_squares.append(att)
        self.attackable_squares = attackable_squares

    # noinspection PyUnresolvedReferences
    def check_if_in_check(self, is_simulated):
        game = self.current_game_info.get("current game", None)
        if game is not None:
            if self == game.player1:
                other_player = game.player2
            else:
                other_player = game.player1
            other_player.update_attackable_squares(is_simulated)
            if self.king.square in other_player.attackable_squares:
                self.king.square.highlight("in check")
                return True
            else:
                self.king.square.un_highlight()
                return False
        else:
            print("Coudn't get the game's information")
            self.king.square.un_highlight()
            return False

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
