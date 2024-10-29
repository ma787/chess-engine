"Module providing the board class."
import string

from chess_engine import constants as cs, utils


class Board:
    """A class representing the chessboard and special move states.

    Attributes:
        array (list): An array of length 128, consisting of a real
            and a 'dummy' board for off-board move checks.
        black (int): Indicates whether the side to move is black.
        castling_rights (int): a nibble storing the castling rights:
            [BK][BQ][WK][WQ]
        ep_square (int): The position of a pawn that can be captured
        en passant in the next move, or 0 if no such pawn exists.
        halfmove_clock (int): The number of halfmoves since the last capture
        or pawn advance.
        fullmove_num (int): The number of the full moves. starts at 1.
        piece_list (list): Associates each piece type with the positions
            on the board where they are present.
        prev_state (list): A list of integers containing irreversible state from
            the previous moves:
        [ type* ][ piece type* ][ castling rights ][ valid ][ ep file ][ --- ][ halfmove clock ]
        |-1 bit-||---3 bits----||-----4 bits------||-1 bit-||--3 bits-||1 bit||-----7 bits-----|
            *of captured piece (if any)
    """

    @staticmethod
    def starting_array():
        """Returns the board array corresponding to the starting position."""
        arr = [0 for _ in range(128)]
        row = [
            cs.ROOK,
            cs.KNIGHT,
            cs.BISHOP,
            cs.QUEEN,
            cs.KING,
            cs.BISHOP,
            cs.KNIGHT,
            cs.ROOK,
        ]

        for i in range(8):
            arr[i] = row[i]
            arr[0x70 + i] = -row[i]

        for i in range(0x10, 0x18):
            arr[i] = cs.PAWN
            arr[0x50 + i] = -cs.PAWN

        return arr

    def build_piece_list(self):
        """Builds a piece list from a board array."""
        piece_list = {p: set() for p in cs.ALL_PIECES}
        i = 0

        while i < 128:
            if self.array[i]:
                piece_list[self.array[i]].add(i)
            i += 1
            if i & 0x88:
                i += 8

        return piece_list

    def __init__(
        self,
        arr=None,
        black=cs.WHITE,
        cr=None,
        ep_sqr=None,
        hm_clk=0,
        fm_num=1,
    ):
        self.array = Board.starting_array() if arr is None else arr
        self.black = black
        self.castling_rights = 0b1111 if cr is None else cr
        self.ep_square = 0 if ep_sqr is None else ep_sqr
        self.halfmove_clock = hm_clk
        self.fullmove_num = fm_num
        self.prev_state = []
        self.piece_list = self.build_piece_list()

    @classmethod
    def of_string(cls, fen_str):
        """Converts a FEN string to a board object."""
        info = fen_str.split(" ")

        if len(info) != 6:
            raise ValueError

        # info[0]: the squares on the board
        # info[1]: the side to move
        # info[2]: the castling rights
        # info[3]: the en passant square
        # info[4]: the halfmove clock
        # info[5]: the full move number

        rows = "/".join(reversed(info[0].split("/")))
        arr = [0 for _ in range(128)]
        i = 0

        for sqr in rows:
            if sqr == "/":
                i += 8
            elif sqr in string.digits[1:9]:
                i += int(sqr)
            else:
                arr[i] = cs.PIECE_FROM_SYM[sqr.lower()] * (-1 + 2 * int(sqr.isupper()))
                i += 1

        c_rights = 0

        if info[2] != "-":
            for c in info[2]:
                c_rights |= 1 << (3 - "kqKQ".index(c))

        ep = 0 if info[3] == "-" else utils.string_to_coord(info[3])

        return cls(arr, int(info[1] == "b"), c_rights, ep, int(info[4]), int(info[5]))

    def to_string(self):
        """Converts a board object to a FEN string."""

        def run_len(s, i, acc):
            try:
                return acc if s[i] != "0" else run_len(s, i + 1, acc + 1)
            except IndexError:
                return acc

        result = ""
        i = 0
        rows = ""

        while i < 128:
            if i & 0x88:
                rows += "/"
                i += 8
            elif not self.array[i]:
                n = 0
                while not self.array[i]:
                    i += 1
                    n += 1
                    if i & 0x88:
                        break
                rows += str(n)
            else:
                sqr = self.array[i]
                symbol = cs.SYM_FROM_PIECE[abs(sqr)]
                rows += symbol if sqr < 0 else symbol.upper()
                i += 1

        result += "/".join(reversed(rows[:-1].split("/")))
        result += " b " if self.black else " w "

        if self.castling_rights:
            if self.get_castling_rights(2):
                result += "K"
            if self.get_castling_rights(3):
                result += "Q"
            if self.get_castling_rights(0):
                result += "k"
            if self.get_castling_rights(1):
                result += "q"
            result += " "
        else:
            result += "- "

        result += "-" if not self.ep_square else utils.coord_to_string(self.ep_square)
        result += " " + str(self.halfmove_clock)
        return result + " " + str(self.fullmove_num)

    def __eq__(self, other):
        return (
            self.array == other.array
            and self.black == other.black
            and self.castling_rights == other.castling_rights
            and self.ep_square == other.ep_square
            and self.halfmove_clock == other.halfmove_clock
            and self.fullmove_num == other.fullmove_num
        )

    def __repr__(self):
        icons = {
            -1: "\u265d",
            1: "\u2657",
            -2: "\u265a",
            2: "\u2654",
            -3: "\u265e",
            3: "\u2658",
            -4: "\u265f",
            4: "\u2659",
            -5: "\u265b",
            5: "\u2655",
            -6: "\u265c",
            6: "\u2656",
        }
        output = "\n"

        for i in range(0x70, -0x10, -0x10):
            output += str(int(i / 0x10 + 1))
            for j in range(8):
                sqr = self.array[i + j]
                output += "\u2003" if sqr == 0 else icons[sqr]
            output += "\n"

        # add letters A-H in unicode
        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"

        return output

    def switch_side(self):
        """Changes the side to move on the board."""
        self.black ^= 1

    def get_castling_rights(self, i):
        "Returns the ith bit of the castling rights value."
        return self.castling_rights & (1 << (3 - i))

    def remove_castling_rights(self, i):
        "Sets the ith bit of the castling rights value to False"
        self.castling_rights &= ~(1 << (3 - i))

    def save_state(self, is_ep, p_type):
        """Saves board state prior to a move to the stack prev_state.

        Args:
            is_ep (int): Whether the piece captured by the move
                (if any) was captured en passant.
            p_type (int): The type of the captured piece.
        """
        current_state = self.halfmove_clock

        if self.ep_square:
            current_state |= (self.ep_square & 0x0F) << 8
            current_state |= 1 << 11  # valid bit set for ep file

        current_state |= self.castling_rights << 12
        current_state |= p_type << 16
        current_state |= is_ep << 19

        self.prev_state.append(current_state)

    def get_prev_state(self):
        """Parses the state saved prior to the most recent move."""
        prev_state = self.prev_state.pop()

        state = [(prev_state >> 19) & 1]  # en passant capture
        state.append((prev_state >> 16) & 7)  # type of captured piece
        state.append((prev_state >> 12) & 0xF)  # castling rights
        state.append((prev_state >> 8) & 0xF)  # ep file and valid bit
        state.append(prev_state & 0x7F)  # halfmove clock

        return state

    def find_king(self, black):
        """Returns the position of the king on the board.

        Args:
            black (int): Whether the king to search for is black.

        Returns:
            int: The position of the king in the board array.
        """
        return min(self.piece_list[cs.KING * (1 - 2 * black)])
