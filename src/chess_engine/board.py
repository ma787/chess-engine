"Module providing the board class."
import string

from chess_engine import lan_parser as lp


class Board:
    """A class representing the chessboard and special move states.

    Attributes:
        array (list): A 2D array of all board positions.
        black (bool): Indicates whether the side to move is black.
        castling_rights (int): a 4-bit int storing the castling rights
            for the side to move. MSB to LSB: WQ, WK, BQ, BK
        en_passant_square (tuple): The position of a pawn that can be captured
        en passant in the next move, or None if no such pawn exists.
        halfmove_clock (int): The number of halfmoves since the last capture
        or pawn advance.
        fullmove_num (int): The number of the full moves. starts at 1.
        prev_state (list): A list of integers containing irreversible state from
            the previous moves:
        [ type* ][ piece type* ][ castling rights ][ valid ][ ep file ][ --- ][ halfmove clock ]
        [-1 bit-]|---3 bits----||-----4 bits------|[-1 bit-]|--3 bits-|[1 bit]|-----7 bits-----|
        *of captured piece (if any)
    """

    @staticmethod
    def starting_array():
        """Returns the board array corresponding to the starting position."""
        arr = []
        arr.append([6, 3, 1, 5, 2, 1, 3, 6])
        arr.append([4, 4, 4, 4, 4, 4, 4, 4])

        for _ in range(4):
            arr.append([0, 0, 0, 0, 0, 0, 0, 0])

        arr.append([-i for i in arr[1]])
        arr.append([-j for j in arr[0]])

        return arr

    def __init__(
        self,
        arr=None,
        black=False,
        cr=None,
        ep_sqr=None,
        hm_clk=0,
        fm_num=1,
    ):
        self.array = Board.starting_array() if arr is None else arr
        self.black = black
        self.castling_rights = 0b1111 if cr is None else cr
        self.en_passant_square = ep_sqr
        self.halfmove_clock = hm_clk
        self.fullmove_num = fm_num
        self.prev_state = []

    @classmethod
    def of_string(cls, fen_str):
        """Converts a FEN string to a board object."""
        p_types = {"b": 1, "k": 2, "n": 3, "p": 4, "q": 5, "r": 6}
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
        castling = 0

        for i in range(7, -1, -1):
            rank = []

            for sqr in rows[i]:
                if sqr in string.digits[1:9]:
                    rank.extend([0 for _ in range(int(sqr))])
                else:
                    for s, p_type in p_types.items():
                        if sqr.casefold() == s.casefold():
                            mul = 1 if sqr.isupper() else -1
                            rank.append(p_type * mul)

            arr.append(rank)

        for i, c in enumerate("kqKQ"):
            castling |= int(c in info[2]) << i

        ep = None if info[3] == "-" else lp.to_index(info[3])

        return cls(arr, info[1] != "w", castling, ep, int(info[4]), int(info[5]))

    def to_string(self):
        """Converts a board object to a FEN string."""

        def run_len(s, i, acc):
            try:
                return acc if s[i] != "0" else run_len(s, i + 1, acc + 1)
            except IndexError:
                return acc

        symbols = {0: "0", 1: "b", 2: "k", 3: "n", 4: "p", 5: "q", 6: "r"}
        result = ""

        for i in range(7, -1, -1):
            row = ""

            for sqr in self.array[i]:
                row += symbols[abs(sqr)] if sqr <= 0 else symbols[abs(sqr)].upper()

            j = 0

            while j < 8:
                if row[j] == "0":
                    rlen = run_len(row, j + 1, 1)
                    result += str(rlen)
                    j += rlen
                else:
                    result += row[j]
                    j += 1

            if i != 0:
                result += "/"

        result += " b " if self.black else " w "

        if self.castling_rights:
            for i, c in enumerate("KQ"):
                if self.castling_rights & 1 << (2 + i):
                    result += c

            for i, c in enumerate("kq"):
                if self.castling_rights & 1 << i:
                    result += c
            result += " "
        else:
            result += "- "

        result += (
            "-"
            if self.en_passant_square is None
            else lp.to_string(self.en_passant_square)
        )

        result += " " + str(self.halfmove_clock)
        return result + " " + str(self.fullmove_num)

    def __eq__(self, other):
        return (
            self.array == other.array
            and self.black == other.black
            and self.castling_rights == other.castling_rights
            and self.en_passant_square == other.en_passant_square
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
        board_to_print = reversed(self.array)
        ranks = list(range(8, 0, -1))
        output = "\n"

        for i, row in enumerate(board_to_print):
            symbols = ["\u2003" if p == 0 else icons[p] for p in row]
            symbols.insert(0, str(ranks[i]))
            output += "".join(symbols) + "\n"

        # add letters A-H in unicode
        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"

        return output

    def switch_side(self):
        """Changes the side to move on the board."""
        self.black ^= True

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

        if self.en_passant_square is not None:
            current_state |= self.en_passant_square[1] << 8
            current_state |= 1 << 11  # valid bit set for ep file

        current_state |= self.castling_rights << 12
        current_state |= p_type << 16
        current_state |= is_ep << 19

        self.prev_state.append(current_state)

    def get_prev_state(self):
        """Parses the state saved prior to the most recent move."""
        prev_state = self.prev_state.pop()

        state = [((prev_state & 1 << 19) >> 19)]  # en passant capture
        state.append((prev_state & 7 << 16) >> 16)  # type of captured piece
        state.append((prev_state & 0xF << 12) >> 12)  # castling rights
        state.append((prev_state & 0xF << 8) >> 8)  # ep file and valid bit
        state.append(prev_state & 0x7F)  # halfmove clock

        return state

    def find_king(self, black):
        """Returns the position of the king on the board.

        Args:
            black (bool): Whether the king to search for is black.

        Returns:
            King: The King object in the board array.

        Raises:
            ValueError: If the King object is not found
        """
        for i in range(8):
            for j, p in enumerate(self.array[i]):
                if p == 2 and not black or p == -2 and black:
                    return (i, j)

        raise ValueError  # king must be present in a valid board position
