from enum import Enum
import sys


class Colour(Enum):
    WHITE = 0
    BLACK = 1

# number corresponds to black/white pieces


class Piece:
    value = 0
    symbol = ""

    def __init__(self, colour, position, board):
        self.colour = colour
        self.position = position
        self.board = board

    def check_if_move_possible(self, destination):
        """Simulates the move to check if it is legal."""
        return True

    def perform_move(self, destination):
        """Moves the piece to the destination square"""
        return True

# piece class as a template with a basic move function


class Pawn(Piece):
    value = 1
    symbol = "p"


class Knight(Piece):
    value = 3
    symbol = "n"


class Bishop(Piece):
    value = 3
    symbol = "b"


class Rook(Piece):
    value = 5
    symbol = "r"


class Queen(Piece):
    value = 9
    symbol = "q"


class King(Piece):
    value = sys.maxsize - 39  # total value of pieces, prevents overflow
    symbol = "k"


class ChessBoard:
    def __init__(self):
        self.piece_list = []
        self.discarded_pieces = []
        self.fifty_move_count = 0
        self.board = [[None for x in range(8)] for x in range(8)]

        # black pieces
        self.board[0][0] = Rook(Colour.BLACK, (0, 0), self)
        self.board[0][1] = Knight(Colour.BLACK, (0, 1), self)
        self.board[0][2] = Bishop(Colour.BLACK, (0, 2), self)
        self.board[0][3] = Queen(Colour.BLACK, (0, 3), self)
        self.board[0][4] = King(Colour.BLACK, (0, 4), self)
        self.board[0][5] = Bishop(Colour.BLACK, (0, 5), self)
        self.board[0][6] = Knight(Colour.BLACK, (0, 6), self)
        self.board[0][7] = Rook(Colour.BLACK, (0, 7), self)

        # black pawns
        self.board[1][0] = Pawn(Colour.BLACK, (1, 0), self)
        self.board[1][1] = Pawn(Colour.BLACK, (1, 1), self)
        self.board[1][2] = Pawn(Colour.BLACK, (1, 2), self)
        self.board[1][3] = Pawn(Colour.BLACK, (1, 3), self)
        self.board[1][4] = Pawn(Colour.BLACK, (1, 4), self)
        self.board[1][5] = Pawn(Colour.BLACK, (1, 5), self)
        self.board[1][6] = Pawn(Colour.BLACK, (1, 6), self)
        self.board[1][7] = Pawn(Colour.BLACK, (1, 7), self)

        # white pieces
        self.board[7][0] = Rook(Colour.WHITE, (7, 0), self)
        self.board[7][1] = Knight(Colour.WHITE, (7, 1), self)
        self.board[7][2] = Bishop(Colour.WHITE, (7, 2), self)
        self.board[7][3] = Queen(Colour.WHITE, (7, 3), self)
        self.board[7][4] = King(Colour.WHITE, (7, 4), self)
        self.board[7][5] = Bishop(Colour.WHITE, (7, 5), self)
        self.board[7][6] = Knight(Colour.WHITE, (7, 6), self)
        self.board[7][7] = Rook(Colour.WHITE, (7, 7), self)

        # white pawns
        self.board[6][0] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][1] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][2] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][3] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][4] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][5] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][6] = Pawn(Colour.WHITE, (6, 0), self)
        self.board[6][7] = Pawn(Colour.WHITE, (6, 0), self)

        for row in self.board:
            for square in row:
                if square:
                    self.piece_list.append(Piece)  # adds the pieces to the piece list


class Game:
    def __init__(self):
        self.board = ChessBoard()

    def change_move_string(self, move_string):
        """Changes the move entered by the user to a class and coordinates."""
        return

    def check_end_of_game(self):
        """Checks if the game is over due to checkmate, the fifty move rule or threefold repetition."""
        return
