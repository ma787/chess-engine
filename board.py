from colour import Colour
from pieces import Bishop, King, Knight, Pawn, Queen, Rook


class Board:
    def __init__(self):
        self.piece_list = []
        self.discarded_pieces = []
        self.array = [[None for _ in range(8)] for _ in range(8)]
        self.side_to_move = Colour.WHITE
        self.last_move = ""
        self.castling_rights = [True, True, True, True]  # white then black, queen side then king side
        self.in_check = [False, False]  # white then black

        for c in Colour:
            index = 0 if c == Colour.WHITE else 7
            offset = 1 if c == Colour.WHITE else -1

            for i, p in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                piece = p(c, (index, i))
                self.piece_list.append(piece)
                self.array[index][i] = piece

                pawn = Pawn(c, (index + offset, i))
                self.piece_list.append(pawn)
                self.array[index + offset][i] = pawn

    def __repr__(self):  # overrides the built-in print function
        board_to_print = reversed(self.array)
        ranks = list(range(8, 0, -1))

        output = ""

        for i, row in enumerate(board_to_print):
            symbols = [str(ranks[i])]
            for piece in row:
                if piece:
                    symbols.append(piece.icon)
                else:
                    symbols.append("\u2003")  # empty space unicode character

            output += "".join(symbols) + "\n"

        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"  # letters A-H in unicode

        return output
