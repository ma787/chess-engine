"Module providing the board class."

from chess_engine import attributes as attrs, pieces


class Board:
    """A class representing the chessboard and special move states.

    Attributes:
        array (list): A 2D array of all board positions.
        side_to_move (int): A value indicating the colour of the side to move.
        castling_rights (list): a list of bools storing the castling rights
            for the side to move: [WQ, WK, BQ, BK]
        en_passant_file (int): The index of the file where an en passant
            capture can occur, and -1 if none are possible.
        captured_pieces (list): A list of all captured pieces.
    """

    def __init__(self):
        self.array = [[None for _ in range(8)] for _ in range(8)]
        self.side_to_move = attrs.Colour.WHITE
        self.final_rank = 7
        self.castling_rights = [True, True, True, True]
        self.en_passant_file = -1
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

        # add letters A-H in unicode
        output += "\u2005a\u2005b\u2005c\u2005d\u2005e\u2005f\u2005g\u2005h"

        return output

    def switch_side(self):
        """Changes the side to move on the board."""
        if self.side_to_move == attrs.Colour.WHITE:
            self.side_to_move = attrs.Colour.BLACK
            self.final_rank = 0
        else:
            self.side_to_move = attrs.Colour.WHITE
            self.final_rank = 7

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

    def to_string(self):
        """Returns a string representation of the board."""
        board_to_print = reversed(self.array)
        output = ""

        for _, row in enumerate(board_to_print):
            symbols = ["-" if not piece else piece.symbol for piece in row]
            output += "".join(symbols) + "\n"

        return output
