"Module providing the board class."
import string

from chess_engine import attributes as attrs, pieces, lan_parser as lp


class Board:
    """A class representing the chessboard and special move states.

    Attributes:
        array (list): A 2D array of all board positions.
        side_to_move (int): A value indicating the colour of the side to move.
        castling_rights (list): a list of bools storing the castling rights
            for the side to move: [WQ, WK, BQ, BK]
        en_passant_square (tuple): The position of a pawn that can be captured
        en passant in the next move, or None if no such pawn exists.
        halfmove_clock (int): The number of halfmoves since the last capture
        or pawn advance.
        fullmove_num (int): The number of the full moves. starts at 1.
        prev_state (list): Contains aspects of the position prior to the last
        move that was made, if applicable:
            [captured piece, castling rights, en passant square, halfmove clock]
    """

    @staticmethod
    def starting_array():
        """Returns the board array corresponding to the starting position."""
        arr = [[None for _ in range(8)] for _ in range(8)]

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
                arr[index][i] = piece

                pawn = pieces.Pawn(c, (index + offset, i))
                arr[index + offset][i] = pawn

        return arr

    def __init__(
        self,
        arr=None,
        side=attrs.Colour.WHITE,
        cr=None,
        ep_sqr=None,
        hm_clk=0,
        fm_num=1,
    ):
        self.array = Board.starting_array() if arr is None else arr
        self.side_to_move = side
        self.castling_rights = [True, True, True, True] if cr is None else cr
        self.en_passant_square = ep_sqr
        self.halfmove_clock = hm_clk
        self.fullmove_num = fm_num
        self.prev_state = [None, 0x00, None, 0]

    @classmethod
    def of_string(cls, fen_str):
        """Converts a FEN string to a board object."""
        piece_types = {
            "b": pieces.Bishop,
            "k": pieces.King,
            "n": pieces.Knight,
            "q": pieces.Queen,
            "r": pieces.Rook,
            "p": pieces.Pawn,
        }
        info = fen_str.split(" ")

        if len(info) != 6:
            raise ValueError

        # info[0]: the squares on the board
        # info[1]: the side to move
        # info[2]: the castling rights
        # info[3]: the en passant square
        # info[4]: the halfmove clock
        # info[5]: the full move number

        rows = info[0].split("/")

        if len(rows) != 8:
            raise ValueError

        arr = []

        for i, row in enumerate(rows):
            rank = []

            for j, sqr in enumerate(row):
                if sqr in string.digits[1:9]:
                    rank.extend([None for _ in range(int(sqr))])
                else:
                    for s, p_type in piece_types.items():
                        if sqr.casefold() == s.casefold():
                            colour = (
                                attrs.Colour.WHITE
                                if sqr.isupper()
                                else attrs.Colour.BLACK
                            )
                            rank.append(p_type(colour, (i, j)))

            arr.append(rank)

        return cls(
            list(reversed(arr)),
            attrs.Colour.WHITE if info[1] == "w" else attrs.Colour.BLACK,
            ["Q" in info[2], "K" in info[2], "q" in info[2], "k" in info[2]],
            None if info[3] == "-" else lp.to_index(info[3]),
            int(info[4]),
            int(info[5]),
        )

    def to_string(self):
        """Returns a string representation of the board."""
        board_to_print = reversed(self.array)
        output = ""

        for _, row in enumerate(board_to_print):
            symbols = ["-" if not piece else piece.symbol for piece in row]
            output += "".join(symbols) + "\n"

        return output

    def __eq__(self, other):
        return (
            self.to_string() == other.to_string()
            and self.side_to_move == other.side_to_move
            and self.castling_rights == other.castling_rights
            and self.en_passant_square == other.en_passant_square
            and self.halfmove_clock == other.halfmove_clock
            and self.fullmove_num == other.fullmove_num
        )

    def __repr__(self):  # overrides the built-in print function
        board_to_print = reversed(self.array)
        ranks = list(range(8, 0, -1))
        output = "\n"

        for i, row in enumerate(board_to_print):
            symbols = ["\u2003" if not piece else piece.icon for piece in row]
            symbols.insert(0, str(ranks[i]))
            output += "".join(symbols) + "\n"

        # add letters A-H in unicode
        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"

        return output

    def switch_side(self):
        """Changes the side to move on the board."""
        if self.side_to_move == attrs.Colour.WHITE:
            self.side_to_move = attrs.Colour.BLACK
        else:
            self.side_to_move = attrs.Colour.WHITE

    def find_king(self, colour):
        """Returns the king of the specified colour on the board.

        Args:
            colour (Colour): The colour of the king to search for.

        Returns:
            King: The King object in the board array.

        Raises:
            ValueError: If the King object is not found
        """
        king = None

        for i in range(8):
            for piece in self.array[i]:
                if piece is not None and piece.symbol == "k" and piece.colour == colour:
                    king = piece
                    break

        if king is None:
            raise ValueError  # king must be present in a valid board position

        return king
