import operator
import random

from chess_engine import attributes as attrs


class Hashing:
    def __init__(self):
        self.piece_values = {
            ("p", attrs.Colour.WHITE.value): 0,
            ("b", attrs.Colour.WHITE.value): 1,
            ("n", attrs.Colour.WHITE.value): 2,
            ("r", attrs.Colour.WHITE.value): 3,
            ("q", attrs.Colour.WHITE.value): 4,
            ("k", attrs.Colour.WHITE.value): 5,
            ("p", attrs.Colour.BLACK.value): 6,
            ("b", attrs.Colour.BLACK.value): 7,
            ("n", attrs.Colour.BLACK.value): 8,
            ("r", attrs.Colour.BLACK.value): 9,
            ("q", attrs.Colour.BLACK.value): 10,
            ("k", attrs.Colour.BLACK.value): 11,
        }

        self.number_array = Hashing.zobrist_generator()

    @staticmethod
    def zobrist_generator():
        """Generates pseudo-random numbers for each piece type and colour for each square on the board."""
        random.seed(1)  # pseudo-random number generation for reproducibility

        array = [
            random.randint(1, 1000000) for _ in range(768)
        ]  # 12 random numbers for each piece at each square
        array.extend([random.randint(1, 1000000) for _ in range(8)])  # en passant files
        array.extend([random.randint(1, 1000000) for _ in range(4)])  # castling rights
        array.append(random.randint(1, 1000000))  # side to move

        return array

    @staticmethod
    def to_array_index(coord):
        """Converts board array coordinates to number array index."""
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
                    value = operator.xor(
                        value, self.number_array[index + piece_constant]
                    )

        if board.side_to_move == attrs.Colour.BLACK:
            value = operator.xor(value, self.number_array[-1])

        if board.en_passant_file != -1:
            value = operator.xor(value, self.number_array[-13 + board.en_passant_file])

        for i, c in enumerate(board.castling_rights):
            if c:
                value = operator.xor(value, self.number_array[-5 + i])

        return value

    def update_hash(self, current_hash, move):
        """Updates a board hash for a move to be made."""
        offset = self.piece_values[move.piece.symbol, move.piece.colour.value]
        start_hash = Hashing.to_array_index(move.start) + offset
        destination_hash = Hashing.to_array_index(move.destination) + offset

        current_hash = operator.xor(
            current_hash, self.number_array[start_hash]
        )  # removing piece from start

        if move.capture:
            if move.board.en_passant_file == -1:
                captured = move.board.array[move.destination[0]][move.destination[1]]
            else:
                i = -1 if move.piece.colour == attrs.Colour.WHITE else 1
                captured = move.board.array[move.destination[0] + i][
                    move.destination[1]
                ]

            captured_position = Hashing.to_array_index(captured.position)
            captured_position += self.piece_values[
                captured.symbol, captured.colour.value
            ]

            current_hash = operator.xor(
                current_hash, self.number_array[captured_position]
            )  # removing captured piece

            if (
                captured.symbol == "r" and captured.move_count == 0
            ):  # updating castling rights after rook capture
                colour = 0 if captured.colour == attrs.Colour.WHITE else 2
                castle = 0 if captured.position[1] == 0 else 1
                current_hash = operator.xor(
                    current_hash, self.number_array[-5 + colour + castle]
                )

        if move.promotion:
            destination_hash -= offset
            destination_hash += self.piece_values[
                move.promotion.symbol, move.piece.colour.value
            ]
            current_hash = operator.xor(
                current_hash, self.number_array[destination_hash]
            )  # placing promoted piece

        elif move.castling:
            if move.piece.colour == attrs.Colour.WHITE:
                if move.castling == attrs.Castling.QUEEN_SIDE:
                    rook = move.board.array[0][0]
                    rook_destination = (
                        Hashing.to_array_index((0, 3))
                        + self.piece_values["r", attrs.Colour.WHITE.value]
                    )
                else:
                    rook = move.board.array[0][7]
                    rook_destination = (
                        Hashing.to_array_index((0, 5))
                        + self.piece_values["r", attrs.Colour.WHITE.value]
                    )

                current_hash = operator.xor(current_hash, self.number_array[-5])
                current_hash = operator.xor(
                    current_hash, self.number_array[-4]
                )  # updating castling rights for castle

            else:
                if move.castling == attrs.Castling.QUEEN_SIDE:
                    rook = move.board.array[7][0]
                    rook_destination = (
                        Hashing.to_array_index((7, 3))
                        + self.piece_values["r", attrs.Colour.BLACK.value]
                    )
                else:
                    rook = move.board.array[7][7]
                    rook_destination = (
                        Hashing.to_array_index((7, 5))
                        + self.piece_values["r", attrs.Colour.BLACK.value]
                    )

                current_hash = operator.xor(current_hash, self.number_array[-3])
                current_hash = operator.xor(
                    current_hash, self.number_array[-2]
                )  # updating castling rights for castle

            rook_position = (
                Hashing.to_array_index(rook.position)
                + self.piece_values["r", rook.colour.value]
            )

            current_hash = operator.xor(
                current_hash, self.number_array[rook_position]
            )  # removing rook from start
            current_hash = operator.xor(
                current_hash, self.number_array[rook_destination]
            )  # moving rook to destination
            current_hash = operator.xor(
                current_hash, self.number_array[destination_hash]
            )  # moving king to destination

        else:
            current_hash = operator.xor(
                current_hash, self.number_array[destination_hash]
            )  # placing piece

            if move.piece.move_count == 0:
                index = 0 if move.piece.colour == attrs.Colour.WHITE else 2

                if move.piece.symbol == "k":  # updating castling rights after king move
                    current_hash = operator.xor(
                        current_hash, self.number_array[-5 + index]
                    )
                    current_hash = operator.xor(
                        current_hash, self.number_array[-4 + index]
                    )

                elif (
                    move.piece.symbol == "r"
                ):  # updating castling rights after rook move
                    castle = 0 if move.start[0] == 0 else 1
                    current_hash = operator.xor(
                        current_hash, self.number_array[-5 + index + castle]
                    )

        if move.board.en_passant_file != -1:  # removing previous en passant file
            current_hash = operator.xor(
                current_hash, self.number_array[-13 + move.board.en_passant_file]
            )

        en_passant_rank = -1

        if move.piece.symbol == "p" and move.piece.move_count == 0:
            if move.distance[0] == 2:
                for shift in (1, -1):
                    if move.destination[1] + shift in range(8):
                        enemy_pawn = move.board.array[move.destination[0]][
                            move.destination[1] + shift
                        ]
                        if enemy_pawn:
                            if (
                                enemy_pawn.symbol == "p"
                                and enemy_pawn.colour != move.piece.colour
                            ):
                                en_passant_rank = move.destination[
                                    1
                                ]  # updating en passant rank if applicable

        if en_passant_rank != -1:
            current_hash = operator.xor(
                current_hash, self.number_array[-13 + en_passant_rank]
            )

        current_hash = operator.xor(
            current_hash, self.number_array[-1]
        )  # switching sides
        return current_hash
