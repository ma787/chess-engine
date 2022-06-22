from colour import *
from pieces import *


class Board:
    def __init__(self):
        self.array = [[None for _ in range(8)] for _ in range(8)]
        self.side_to_move = Colour.WHITE
        self.castling_rights = [True, True, True, True]  # white then black, queen side then king side
        self.en_passant_file = -1
        self.half_move_clock = 0
        self.captured_piece = None

        for c in Colour:
            index = 0 if c == Colour.WHITE else 7
            offset = 1 if c == Colour.WHITE else -1

            for i, p in enumerate((Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)):
                piece = p(c, (index, i))
                self.array[index][i] = piece

                pawn = Pawn(c, (index + offset, i))
                self.array[index + offset][i] = pawn

    def __repr__(self):  # overrides the built-in print function
        board_to_print = reversed(self.array)
        ranks = list(range(8, 0, -1))

        output = "\n"

        for i, row in enumerate(board_to_print):
            symbols = ["\u2003" if not piece else piece.icon for piece in row]
            symbols.insert(0, str(ranks[i]))
            output += "".join(symbols) + "\n"

        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"  # letters A-H in unicode

        return output

    def to_string(self):
        board_to_print = reversed(self.array)
        output = ""

        for i, row in enumerate(board_to_print):
            symbols = ["-" if not piece else piece.symbol for piece in row]
            output += "".join(symbols) + "\n"

        return output
