import pygame
from Piece import Piece
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King


class PieceFactory:
    def __init__(self, board):
        self.board = board

    def create_piece(self, piece, square, color):
        if piece == "Pawn":
            return Pawn(square, color, self.board)
        elif piece == "Rook":
            return Rook(square, color, self.board)
        elif piece == "Bishop":
            return Bishop(square, color, self.board)
        elif piece == "Knight":
            return Knight(square, color, self.board)
        elif piece == "Queen":
            return Queen(square, color, self.board)
        elif piece == "King":
            return King(square, color, self.board)
        else:
            return None

    def populate_regular_game_wb(self):
        grid = self.board.get_grid()
        self.create_piece("Rook", grid[0][0], 'black')
        self.create_piece('Rook', grid[7][0], 'black')
        self.create_piece('Knight', grid[1][0], 'black')
        self.create_piece('Knight', grid[6][0], 'black')
        self.create_piece('Bishop', grid[2][0], 'black')
        self.create_piece('Bishop', grid[5][0], 'black')
        self.create_piece('Queen', grid[3][0], 'black')
        self.create_piece('King', grid[4][0], 'black')
        for i in range(8):
            self.create_piece('Pawn', grid[i][1], 'black')
            self.create_piece('Pawn', grid[i][6], 'white')
        self.create_piece('Rook', grid[0][7], 'white')
        self.create_piece('Rook', grid[7][7], 'white')
        self.create_piece('Knight', grid[1][7], 'white')
        self.create_piece('Knight', grid[6][7], 'white')
        self.create_piece('Bishop', grid[2][7], 'white')
        self.create_piece('Bishop', grid[5][7], 'white')
        self.create_piece('Queen', grid[3][7], 'white')
        self.create_piece('King', grid[4][7], 'white')

    def populate_regular_game_bb(self):
        grid = self.board.get_grid()
        self.create_piece('Rook', grid[0][0], 'white')
        self.create_piece('Rook', grid[7][0], 'white')
        self.create_piece('Knight', grid[1][0], 'white')
        self.create_piece('Knight', grid[6][0], 'white')
        self.create_piece('Bishop', grid[2][0], 'white')
        self.create_piece('Bishop', grid[5][0], 'white')
        self.create_piece('Queen', grid[4][0], 'white')
        self.create_piece('King', grid[3][0], 'white')
        for i in range(8):
            self.create_piece('Pawn', grid[i][1], 'white')
            self.create_piece('Pawn', grid[i][6], 'black')
        self.create_piece('Rook', grid[0][7], 'black')
        self.create_piece('Rook', grid[7][7], 'black')
        self.create_piece('Knight', grid[1][7], 'black')
        self.create_piece('Knight', grid[6][7], 'black')
        self.create_piece('Bishop', grid[2][7], 'black')
        self.create_piece('Bishop', grid[5][7], 'black')
        self.create_piece('Queen', grid[4][7], 'black')
        self.create_piece('King', grid[3][7], 'black')
