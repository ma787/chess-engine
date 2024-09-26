"Module providing board hashing utilities."

import operator
import random

from chess_engine import move


class Hashing:
    """A class that provides zobrist signatures for board positions.

    Attributes:
        offsets (dict): Gives the offsets of values associated with board state
        information in the array, i.e., en passant files, castling rights and
        the side to move.
        array (list): A list of pseudo-random values assigned to each piece and
        position, and other game state information.
    """

    def __init__(self):
        self.offsets = {"en_passant": -13, "castling": -5, "black": -1}
        self.array = Hashing.zobrist_generator()

    @staticmethod
    def zobrist_generator():
        """Generates pseudo-random numbers for each piece type and colour
        for each square on the board, along with other board state info.

        Returns:
            list: A list of 781 random 64-bit integers.
        """
        random.seed(1)  # set seed for reproducibility
        max_val = 2**64 - 1

        # 1 number for each piece at each square (= 768)
        # 1 number to indicate that it's black's turn
        # 4 numbers to indicate castling rights
        # 8 numbers to indicate valid en passant files, if there are any
        array_length = 782

        return [random.randint(0, max_val) for _ in range(array_length - 1)]

    @staticmethod
    def to_array_index(coord):
        """Converts board array coordinates to a number array index."""
        return (coord[0] * 96) + (coord[1] * 12)

    def get_hash(self, position, piece):
        """Gets the number assigned to a piece with a given position and colour.

        Args:
            position (tuple): The coordinates of the piece on the board.
            piece (int): The piece type and colour.

        Returns:
            int: The entry in the number array associated with this piece.
        """
        return self.array[
            int(self.to_array_index(position) + abs(piece) - 1 + 6 * int(piece < 0))
        ]

    def zobrist_hash(self, board):
        """Hashes a board position to a unique number."""
        value = 0

        for i, row in enumerate(board.array):
            for j, square in enumerate(row):
                if square:
                    piece_constant = self.get_hash((i, j), square)
                    value = operator.xor(value, piece_constant)

        if board.black:
            value = operator.xor(value, self.array[self.offsets["black"]])

        if board.en_passant_square is not None:
            value = operator.xor(
                value,
                self.array[self.offsets["en_passant"] + board.en_passant_square[1]],
            )

        for i in range(4):
            if board.get_castling_rights(i):
                value = operator.xor(value, self.array[self.offsets["castling"] + i])

        return value

    def remove_castling_rights(self, current_hash, pos, board):
        """Removes castling values from the hash after a move/capture.

        Args:
            current_hash (int): The board hash to update.
            pos (tuple): The position of the piece to move.
            board (Board): The board to analyse.

        Returns:
            int: The hash updated with any changes to castling rights.
        """
        piece = board.array[pos[0]][pos[1]]

        if abs(piece) not in (2, 6):
            return current_hash

        c_off = 0 if piece > 0 else 2

        if abs(piece) == 2:
            for i in range(0, 2):
                if board.get_castling_rights(c_off + i):
                    current_hash = operator.xor(
                        current_hash, self.array[self.offsets["castling"] + c_off + i]
                    )

        elif abs(piece) == 6:
            c_type = 0 if pos[1] == 0 else 1

            if board.get_castling_rights(c_off + c_type):
                current_hash = operator.xor(
                    current_hash, self.array[self.offsets["castling"] + c_off + c_type]
                )

        return current_hash

    def update_hash(self, current_hash, mv, board):
        """Updates a board hash for a move to be made.

        Args:
            current_hash (int): The board hash to update.
            mv (int): The move to be made.
            board (Board): The board state before the move is made.

        Returns:
            int: The hash of the board position after the move is made.
        """
        [start, dest, capture, castling, promotion] = move.get_info(mv)
        piece = board.array[start[0]][start[1]]
        mul = -1 if board.black else 1

        # moving piece
        current_hash = operator.xor(current_hash, self.get_hash(start, piece))
        current_hash = operator.xor(
            current_hash, self.get_hash(dest, promotion * mul if promotion else piece)
        )

        en_passant_file = -1

        if capture:
            cap_pos = (
                board.en_passant_square if not board.array[dest[0]][dest[1]] else dest
            )

            # removing captured piece
            current_hash = operator.xor(
                current_hash,
                self.get_hash(cap_pos, board.array[cap_pos[0]][cap_pos[1]]),
            )

            # removing castling rights after rook capture
            current_hash = self.remove_castling_rights(current_hash, cap_pos, board)

        elif castling:
            first_rank = 7 if board.black else 0
            files = (0, 3) if castling == 2 else (7, 5)

            # moving rook
            current_hash = operator.xor(
                current_hash, self.get_hash((first_rank, files[0]), 6 * mul)
            )
            current_hash = operator.xor(
                current_hash, self.get_hash((first_rank, files[1]), 6 * mul)
            )

        # updating en passant file after pawn move of 2 squares
        elif abs(piece) == 4 and start[0] in (1, 6) and dest[0] in (3, 4):
            en_passant_file = dest[1]

        # removing castling rights after king/rook move
        current_hash = self.remove_castling_rights(current_hash, start, board)

        # removing previous en passant file, if any
        if board.en_passant_square is not None:
            current_hash = operator.xor(
                current_hash,
                self.array[self.offsets["en_passant"] + board.en_passant_square[1]],
            )

        # set new en passant file if necessary
        if en_passant_file != -1:
            current_hash = operator.xor(
                current_hash, self.array[self.offsets["en_passant"] + en_passant_file]
            )

        # switching side to move
        current_hash = operator.xor(current_hash, self.array[self.offsets["black"]])

        return current_hash
