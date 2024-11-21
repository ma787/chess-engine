"Module providing the board class."

from chess_engine import constants as cs, utils


class Board:
    """A class representing the chessboard and special move states.

    Attributes:
        array (list): An list of 128 integers consisting of a real
            and a 'dummy' board for off-board move checks.
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
        piece_list (list): Associates each piece type with the positions
            on the board where they are present.
        prev_state (list): A list of tuples containing irreversible state from
            the previous moves:
        (halfmove clock, ep square, castling rights, check, captured piece type)
    """

    # pylint: disable=too-many-instance-attributes
    # 10 attributes is reasonable here.

    def __init__(
        self, arr=None, black=cs.WHITE, cr=None, ep_sqr=-1, hm_clk=0, fm_num=1, check=0
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
        self.piece_list = self.build_piece_list()

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

        for i in range(0x70, -0x10, -0x10):
            output += str(int(i / 0x10 + 1))
            for j in range(8):
                output += cs.ICONS[self.array[i + j]]
            output += "\n"

        # add letters A-H in unicode
        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"

        return output

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

    def to_fen(self):
        """Converts a board object to a FEN string."""
        result = ""
        rows = ""
        i = 0

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
                rows += cs.LETTERS[self.array[i]]
                i += 1

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
        """Parses the state saved prior to the most recent move."""
        return self.prev_state.pop()

    def find_king(self, black):
        """Returns the position of the king on the board."""
        return min(self.piece_list[cs.K | (black << 3)])
