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
                if square:
                    piece_constant = self.get_piece_hash(square)
                    value = operator.xor(value, piece_constant)

        if board.side_to_move == attrs.Colour.BLACK:
            value = operator.xor(value, self.array[self.offsets["black"]])

        if board.en_passant_file != -1:
            value = operator.xor(
                value, self.array[self.offsets["en_passant"] + board.en_passant_file]
            )

        for i, c in enumerate(board.castling_rights):
            if c:
                value = operator.xor(value, self.array[self.offsets["castling"] + i])

        return value

    def update_hash(self, current_hash, move, board):
        """Updates a board hash for a move to be made."""
        piece = board.array[move.start[0]][move.start[1]]

        start_hash = self.get_piece_hash(piece)
        destination_hash = self.get_hash(
            move.destination, piece.symbol, board.side_to_move
        )

        # removing piece from start
        current_hash = operator.xor(current_hash, start_hash)

        if move.capture:
            if board.en_passant_file == -1:
                captured = board.array[move.destination[0]][move.destination[1]]
            else:
                i = -1 if board.side_to_move == attrs.Colour.WHITE else 1
                captured = board.array[move.destination[0] + i][move.destination[1]]

            captured_hash = self.get_piece_hash(captured)

            # removing captured piece
            current_hash = operator.xor(current_hash, captured_hash)

            # removing castling rights after rook capture
            if captured.symbol == "r" and captured.move_count == 0:
                c_off = 0 if captured.colour == attrs.Colour.WHITE else 2
                c_type = 0 if captured.position[1] == 0 else 1
                current_hash = operator.xor(
                    current_hash, self.array[self.offsets["castling"] + c_off + c_type]
                )

        if move.promotion:
            destination_hash = self.get_hash(
                move.destination, move.promotion.symbol, board.side_to_move
            )

            # placing promoted piece
            current_hash = operator.xor(current_hash, destination_hash)

        elif move.castling:
            c_off = 0 if board.side_to_move == attrs.Colour.WHITE else 2

            first_rank = 7 - board.final_rank
            rook_file = 0 if move.castling == attrs.Castling.QUEEN_SIDE else 7
            new_file = 3 if move.castling == attrs.Castling.QUEEN_SIDE else 5

            rook = board.array[first_rank][rook_file]
            rook_destination_hash = self.get_hash(
                (first_rank, new_file), "r", board.side_to_move
            )

            # removing castling rights after castle move
            current_hash = operator.xor(
                current_hash, self.array[self.offsets["castling"] + c_off]
            )
            current_hash = operator.xor(
                current_hash, self.array[self.offsets["castling"] + c_off + 1]
            )

            # removing rook from start
            current_hash = operator.xor(current_hash, self.get_piece_hash(rook))

            # moving rook to destination
            current_hash = operator.xor(current_hash, rook_destination_hash)

            # moving king to destination
            current_hash = operator.xor(current_hash, destination_hash)

        else:
            # placing piece
            current_hash = operator.xor(current_hash, destination_hash)

            en_passant_file = -1

            if piece.move_count == 0:
                c_off = 0 if board.side_to_move == attrs.Colour.WHITE else 2

                # removing castling rights after king move
                if piece.symbol == "k":
                    current_hash = operator.xor(
                        current_hash, self.array[self.offsets["castling"] + c_off]
                    )
                    current_hash = operator.xor(
                        current_hash, self.array[self.offsets["castling"] + c_off + 1]
                    )

                # removing castling rights after rook move
                elif piece.symbol == "r":
                    c_type = 0 if move.start[0] == 0 else 1
                    current_hash = operator.xor(
                        current_hash,
                        self.array[self.offsets["castling"] + c_off + c_type],
                    )

                # updating en passant file after pawn move of 2 squares
                elif (
                    piece.symbol == "p"
                    and (abs(move.destination[0] - move.start[0])) == 2
                ):
                    for off in (1, -1):
                        if move.destination[1] + off in range(8):
                            enemy_pawn = board.array[move.destination[0]][
                                move.destination[1] + off
                            ]
                            if (
                                enemy_pawn
                                and enemy_pawn.symbol == "p"
                                and enemy_pawn.colour != piece.colour
                            ):
                                en_passant_file = move.destination[1]

        # removing previous en passant file, if any
        if board.en_passant_file != -1:
            current_hash = operator.xor(
                current_hash,
                self.array[self.offsets["en_passant"] + board.en_passant_file],
            )

        # set new en passant file if necessary
        if en_passant_file != -1:
            current_hash = operator.xor(
                current_hash, self.array[self.offsets["en_passant"] + en_passant_file]
            )

        # switching side to move
        current_hash = operator.xor(current_hash, self.array[self.offsets["black"]])

        return current_hash
