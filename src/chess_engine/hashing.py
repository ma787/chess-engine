"Module providing board hashing utilities."

import operator
import random

from chess_engine import attributes as attrs


class Hashing:
    """A class that provides zobrist signatures for board positions.

    Attributes:
        piece_values (dict): Associates each piece type on the board with an integer.
        offsets (dict): Gives the offsets of values associated with board state
        information in the array, i.e., en passant files, castling rights and
        the side to move.
        array (list): A list of pseudo-random values assigned to each piece and
        position, and other game state information.
    """

    def __init__(self):
        self.piece_values = {"p": 1, "b": 2, "n": 3, "r": 4, "q": 5, "k": 6}

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

    def get_hash(self, position, symbol, colour):
        """Gets the number assigned to a piece with a given position and colour.

        Args:
            position (tuple): The coordinates of the piece on the board.
            symbol (string): The letter associated with the piece type.
            colour (Colour): The colour of the piece at this position.

        Returns:
            int: The entry in the number array associated with this piece.
        """
        return self.array[
            self.to_array_index(position)
            + self.piece_values[symbol]
            - 1
            + 6 * colour.value
        ]

    def get_piece_hash(self, piece):
        """Calls get_hash using the attributes of a piece."""
        return self.get_hash(piece.position, piece.symbol, piece.colour)

    def zobrist_hash(self, board):
        """Hashes a board position to a unique number."""
        value = 0

        for row in board.array:
            for square in row:
                if square is not None:
                    piece_constant = self.get_piece_hash(square)
                    value = operator.xor(value, piece_constant)

        if board.side_to_move == attrs.Colour.BLACK:
            value = operator.xor(value, self.array[self.offsets["black"]])

        if board.en_passant_square is not None:
            value = operator.xor(
                value,
                self.array[self.offsets["en_passant"] + board.en_passant_square[1]],
            )

        for i, c in enumerate(board.castling_rights):
            if c:
                value = operator.xor(value, self.array[self.offsets["castling"] + i])

        return value

    def remove_castling_rights(self, current_hash, piece, board):
        """Removes castling values from the hash after a move/capture.

        Args:
            current_hash (int): The board hash to update.
            piece (Piece): The piece that has moved.
            board (Board): The board to analyse.

        Returns:
            int: The hash updated with any changes to castling rights.
        """
        if piece.symbol not in ("k", "r"):
            return current_hash

        c_off = 0 if piece.colour == attrs.Colour.WHITE else 2

        if piece.symbol == "k":
            for i in range(0, 2):
                if board.castling_rights[c_off + i]:
                    current_hash = operator.xor(
                        current_hash, self.array[self.offsets["castling"] + c_off + i]
                    )

        elif piece.symbol == "r":
            c_type = 0 if piece.position[1] == 0 else 1

            if board.castling_rights[c_off + c_type]:
                current_hash = operator.xor(
                    current_hash, self.array[self.offsets["castling"] + c_off + c_type]
                )

        return current_hash

    def update_castle(self, current_hash, move, board):
        """Updates the board hash after a castle move."""
        king = board.find_king(board.side_to_move)
        current_hash = self.remove_castling_rights(current_hash, king, board)

        first_rank = 0 if board.side_to_move == attrs.Colour.WHITE else 7
        rook_file = 0 if move.castling == attrs.Castling.QUEEN_SIDE else 7
        new_file = 3 if move.castling == attrs.Castling.QUEEN_SIDE else 5

        old_rook_hash = self.get_hash((first_rank, rook_file), "r", board.side_to_move)
        new_rook_hash = self.get_hash((first_rank, new_file), "r", board.side_to_move)

        # moving rook
        current_hash = operator.xor(current_hash, old_rook_hash)
        current_hash = operator.xor(current_hash, new_rook_hash)

        return current_hash

    def update_hash(self, current_hash, move, board):
        """Updates a board hash for a move to be made.

        Args:
            current_hash (int): The board hash to update.
            move (Move): The castle move used to update the hash.
            board (Board): The board state before the move is made.

        Returns:
            int: The hash of the board position after the move is made.
        """
        piece = board.array[move.start[0]][move.start[1]]

        start_hash = self.get_piece_hash(piece)

        if move.promotion:
            destination_hash = self.get_hash(
                move.destination, move.promotion.symbol, board.side_to_move
            )
        else:
            destination_hash = self.get_hash(
                move.destination, piece.symbol, board.side_to_move
            )

        # moving piece
        current_hash = operator.xor(current_hash, start_hash)
        current_hash = operator.xor(current_hash, destination_hash)

        en_passant_file = -1

        if move.capture:
            captured = (
                board.array[board.en_passant_square[0]][board.en_passant_square[1]]
                if board.en_passant_square is not None
                else board.array[move.destination[0]][move.destination[1]]
            )

            captured_hash = self.get_piece_hash(captured)

            # removing captured piece
            current_hash = operator.xor(current_hash, captured_hash)

            # removing castling rights after rook capture
            current_hash = self.remove_castling_rights(current_hash, captured, board)

        elif move.castling is not None:
            current_hash = self.update_castle(current_hash, move, board)

        else:
            # removing castling rights after king/rook move
            current_hash = self.remove_castling_rights(current_hash, piece, board)

            # updating en passant file after pawn move of 2 squares
            if (
                piece.symbol == "p"
                and move.start[0] in (1, 6)
                and move.destination[0] in (3, 4)
            ):
                en_passant_file = move.destination[1]

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
