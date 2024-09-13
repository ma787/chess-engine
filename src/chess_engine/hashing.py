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

    def zobrist_hash(self, board):
        """Hashes a board position to a unique number."""
        value = 0

        for i, row in enumerate(board.array):
            for j, square in enumerate(row):
                if square:
                    index = Hashing.to_array_index((i, j))
                    piece_constant = self.piece_values[
                        square.symbol, square.colour.value
                    ]
                    value = operator.xor(value, self.array[index + piece_constant])

        if board.side_to_move == attrs.Colour.BLACK:
            value = operator.xor(value, self.array[-1])

        if board.en_passant_file != -1:
            value = operator.xor(value, self.array[-13 + board.en_passant_file])

        for i, c in enumerate(board.castling_rights):
            if c:
                value = operator.xor(value, self.array[-5 + i])

        return value

    def update_hash(self, current_hash, move, board):
        """Updates a board hash for a move to be made."""
        piece = board.array[move.start[0]][move.start[1]]

        offset = self.piece_values[piece.symbol, board.side_to_move]
        start_hash = Hashing.to_array_index(move.start) + offset
        destination_hash = Hashing.to_array_index(move.destination) + offset

        current_hash = operator.xor(
            current_hash, self.array[start_hash]
        )  # removing piece from start

        if move.capture:
            if board.en_passant_file == -1:
                captured = board.array[move.destination[0]][move.destination[1]]
            else:
                i = -1 if board.side_to_move == attrs.Colour.WHITE else 1
                captured = board.array[move.destination[0] + i][move.destination[1]]

            captured_position = Hashing.to_array_index(captured.position)
            captured_position += self.piece_values[
                captured.symbol, captured.colour.value
            ]

            current_hash = operator.xor(
                current_hash, self.array[captured_position]
            )  # removing captured piece

            if (
                captured.symbol == "r" and captured.move_count == 0
            ):  # updating castling rights after rook capture
                colour = 0 if captured.colour == attrs.Colour.WHITE else 2
                castle = 0 if captured.position[1] == 0 else 1
                current_hash = operator.xor(
                    current_hash, self.array[-5 + colour + castle]
                )

        if move.promotion:
            destination_hash -= offset
            destination_hash += self.piece_values[
                move.promotion.symbol, board.side_to_move
            ]
            current_hash = operator.xor(
                current_hash, self.array[destination_hash]
            )  # placing promoted piece

        elif move.castling:
            if board.side_to_move == attrs.Colour.WHITE:
                if move.castling == attrs.Castling.QUEEN_SIDE:
                    rook = board.array[0][0]
                    rook_destination = (
                        Hashing.to_array_index((0, 3))
                        + self.piece_values["r", attrs.Colour.WHITE.value]
                    )
                else:
                    rook = board.array[0][7]
                    rook_destination = (
                        Hashing.to_array_index((0, 5))
                        + self.piece_values["r", attrs.Colour.WHITE.value]
                    )

                current_hash = operator.xor(current_hash, self.array[-5])
                current_hash = operator.xor(
                    current_hash, self.array[-4]
                )  # updating castling rights for castle

            else:
                if move.castling == attrs.Castling.QUEEN_SIDE:
                    rook = board.array[7][0]
                    rook_destination = (
                        Hashing.to_array_index((7, 3))
                        + self.piece_values["r", attrs.Colour.BLACK.value]
                    )
                else:
                    rook = board.array[7][7]
                    rook_destination = (
                        Hashing.to_array_index((7, 5))
                        + self.piece_values["r", attrs.Colour.BLACK.value]
                    )

                current_hash = operator.xor(current_hash, self.array[-3])
                current_hash = operator.xor(
                    current_hash, self.array[-2]
                )  # updating castling rights for castle

            rook_position = (
                Hashing.to_array_index(rook.position)
                + self.piece_values["r", rook.colour.value]
            )

            current_hash = operator.xor(
                current_hash, self.array[rook_position]
            )  # removing rook from start
            current_hash = operator.xor(
                current_hash, self.array[rook_destination]
            )  # moving rook to destination
            current_hash = operator.xor(
                current_hash, self.array[destination_hash]
            )  # moving king to destination

        else:
            current_hash = operator.xor(
                current_hash, self.array[destination_hash]
            )  # placing piece

            if piece.move_count == 0:
                index = 0 if board.side_to_move == attrs.Colour.WHITE else 2

                if piece.symbol == "k":  # updating castling rights after king move
                    current_hash = operator.xor(current_hash, self.array[-5 + index])
                    current_hash = operator.xor(current_hash, self.array[-4 + index])

                elif piece.symbol == "r":  # updating castling rights after rook move
                    castle = 0 if move.start[0] == 0 else 1
                    current_hash = operator.xor(
                        current_hash, self.array[-5 + index + castle]
                    )

        if board.en_passant_file != -1:  # removing previous en passant file
            current_hash = operator.xor(
                current_hash, self.array[-13 + board.en_passant_file]
            )

        en_passant_rank = -1

        if piece.symbol == "p" and piece.move_count == 0:
            if abs(move.destination[0] - move.start[0]) == 2:
                for shift in (1, -1):
                    if move.destination[1] + shift in range(8):
                        enemy_pawn = board.array[move.destination[0]][
                            move.destination[1] + shift
                        ]
                        if enemy_pawn:
                            if (
                                enemy_pawn.symbol == "p"
                                and enemy_pawn.colour != piece.colour
                            ):
                                en_passant_rank = move.destination[
                                    1
                                ]  # updating en passant rank if applicable

        if en_passant_rank != -1:
            current_hash = operator.xor(current_hash, self.array[-13 + en_passant_rank])

        current_hash = operator.xor(current_hash, self.array[-1])  # switching sides
        return current_hash
