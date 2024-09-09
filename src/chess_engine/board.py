from chess_engine import attributes as attrs, pieces


class Board:
    def __init__(self):
        self.array = [[None for _ in range(8)] for _ in range(8)]
        self.side_to_move = attrs.Colour.WHITE
        self.castling_rights = [
            True,
            True,
            True,
            True,
        ]  # white then black, queen side then king side
        self.en_passant_file = -1
        self.half_move_clock = 0
        self.captured_pieces = []

        for c in attrs.Colour:
            index = 0 if c == attrs.Colour.WHITE else 7
            offset = 1 if c == attrs.Colour.WHITE else -1

            rows = [
                pieces.Rook,
                pieces.Knight,
                pieces.Bishop,
                pieces.Queen,
                pieces.King,
                pieces.Bishop,
                pieces.Knight,
                pieces.Rook,
            ]

            for i, p in enumerate(rows):
                piece = p(c, (index, i))
                self.array[index][i] = piece

                pawn = pieces.Pawn(c, (index + offset, i))
                self.array[index + offset][i] = pawn

    def __eq__(self, other):
        return (
            self.to_string() == other.to_string()
            and self.side_to_move == other.side_to_move
            and self.castling_rights == other.castling_rights
            and self.en_passant_file == other.en_passant_file
            and self.half_move_clock == other.half_move_clock
            and self.captured_pieces == other.captured_pieces
        )

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

        for _, row in enumerate(board_to_print):
            symbols = ["-" if not piece else piece.symbol for piece in row]
            output += "".join(symbols) + "\n"

        return output
