"Module providing the board class."

from chess_engine import constants as cs, utils


class Board:
    """A class representing the chessboard and special move states.

    Attributes:
        array (list): An list of 256 integers consisting of the pieces on
            the board, plus off-board sentinel values and padding.
        black (int): Indicates whether the side to move is black.
        castling_rights (list): a list storing the castling rights:
            [WK, WQ, BK, BQ]
        ep_square (int): The target square index of an en passant capture
            (which may not actually be possible).
        halfmove_clock (int): The number of halfmoves since the last capture
        or pawn advance.
        fullmove_num (int): The number of the full moves. starts at 1.
        check (int): Whether the side to move is in check. Possible values:
            -1: uninitalised, 0: not in check, 1: contact check, 2: distant check,
            3: double check
        checker (int): The position of a piece giving check, if in check.
        piece_list (list): Associates each piece with its position.
        prev_state (list): A list of tuples containing irreversible state from
            the previous moves:
        (halfmove clock, ep square, castling rights, check, captured piece type)
    """

    # pylint: disable=too-many-instance-attributes
    # 10 attributes is reasonable here.

    def __init__(
        self,
        arr=None,
        black=cs.WHITE,
        cr=None,
        ep_sqr=-1,
        hm_clk=0,
        fm_num=1,
        check=0,
        p_list=None,
    ):
        self.array = arr or list(cs.STARTING_ARRAY)
        self.black = black
        self.castling_rights = cr or [True, True, True, True]
        self.ep_square = ep_sqr
        self.halfmove_clock = hm_clk
        self.fullmove_num = fm_num
        self.check = check
        self.checker = -1
        self.prev_state = []
        self.piece_list = p_list or list(cs.STARTING_PIECE_LIST)

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
        output = "\n"

        for i in range(0xB4, 0x34, -0x10):
            output += str(int((i - 0x44) / 0x10 + 1))
            for j in range(8):
                output += cs.ICONS[self.array[i + j] & 15]
            output += "\n"

        # add letters A-H in unicode
        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"

        return output

    def debug_print(self):
        """Prints out string representation of entire board array."""

        def check_board(start, end, symbol, value, out):
            for i in range(start, end):
                if self.array[i] == value:
                    out[i] = symbol
                else:
                    out[i] = cs.LETTERS[self.array[i] & 15]

        output = ["" for _ in range(256)]

        for off in (0x00, 0x10, 0xE0, 0xF0):
            check_board(off, off + 16, "X", 0, output)

        for off in range(0x20, 0xE0, 0x10):
            check_board(off, off + 2, "X", 0, output)
            check_board(off + 2, off + 4, "G", cs.GD, output)
            check_board(off + 12, off + 14, "G", cs.GD, output)
            check_board(off + 14, off + 16, "X", 0, output)

        for off in (0x20, 0x30, 0xC0, 0xD0):
            check_board(off + 2, off + 14, "G", cs.GD, output)

        for i in range(0x44, 0xC4, 0x10):
            for j in range(8):
                if self.array[i + j]:
                    output[i + j] = cs.LETTERS[self.array[i + j] & 15]
                else:
                    output[i + j] = "-"

        out_str = ""

        for i in range(0x000, 0x100, 0x10):
            out_str += "".join(output[i : i + 16])
            out_str += "\n"

        print(out_str)

    def to_fen(self):
        """Converts a board object to a FEN string."""
        result = ""
        rows = ""
        i = 0

        for i in range(0x44, 0xC4, 0x10):
            j = 0
            while j < 8:
                if not self.array[i + j]:
                    n = 0
                    while not self.array[i + j]:
                        j += 1
                        n += 1
                        if j > 7:
                            break
                    rows += str(n)
                else:
                    rows += cs.LETTERS[self.array[i + j] & 15]
                    j += 1
            rows += "/"

        result += "/".join(reversed(rows[:-1].split("/")))
        result += " b " if self.black else " w "

        if any(self.castling_rights):
            for i, c in enumerate("KQkq"):
                if self.castling_rights[i]:
                    result += c
            result += " "
        else:
            result += "- "

        result += "-" if self.ep_square == -1 else utils.coord_to_string(self.ep_square)
        result += " " + str(self.halfmove_clock)
        return result + " " + str(self.fullmove_num)

    def switch_side(self):
        """Changes the side to move on the board."""
        self.black ^= 1

    def save_state(self, p_type, promotion):
        """Saves board state prior to a move to the stack prev_state.

        Args:
            p_type (int): The type of the captured piece.
            promotion (bool): Whether the move was a promotion.
        """

        self.prev_state.append(
            (
                self.halfmove_clock,
                self.ep_square,
                list(self.castling_rights),
                self.check,
                self.checker,
                p_type,
                promotion,
            )
        )

    def get_prev_state(self):
        """Returns the state saved prior to the most recent move."""
        return self.prev_state.pop()
