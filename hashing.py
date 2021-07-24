import operator
import random
import re
import string

from colour import Colour


class Hashing:
    def __init__(self):
        self.piece_values = {('p', Colour.WHITE.value): 0,
                             ('b', Colour.WHITE.value): 1,
                             ('n', Colour.WHITE.value): 2,
                             ('r', Colour.WHITE.value): 3,
                             ('q', Colour.WHITE.value): 4,
                             ('k', Colour.WHITE.value): 5,
                             ('p', Colour.BLACK.value): 6,
                             ('b', Colour.BLACK.value): 7,
                             ('n', Colour.BLACK.value): 8,
                             ('r', Colour.BLACK.value): 9,
                             ('q', Colour.BLACK.value): 10,
                             ('k', Colour.BLACK.value): 11
                             }

        self.number_array = Hashing.zobrist_generator()

    @staticmethod
    def zobrist_generator():
        """Generates pseudo-random numbers for each piece type and colour for each square on the board."""
        random.seed(1)  # pseudo-random number generation for reproducibility

        array = [random.randint(1, 1000000) for _ in range(768)]  # 12 random numbers for each piece at each square
        array.extend([random.randint(1, 1000000) for _ in range(8)])  # en passant files
        array.extend([random.randint(1, 1000000) for _ in range(4)])  # castling rights
        array.append(random.randint(1, 1000000))  # side to move

        return array

    def zobrist_hash(self, board):
        """Hashes a board position to a unique number."""
        value = 0

        for i, row in enumerate(board.array):
            for j, square in enumerate(row):
                if square:
                    index = (i * 8) + j
                    piece_constant = self.piece_values[square.symbol, square.colour.value]
                    value = operator.xor(value, self.number_array[index + piece_constant])

        if board.side_to_move == Colour.BLACK:
            if re.fullmatch("[a-h][2][-][a-h][4]", board.last_move):
                file = board.last_move[0]
                value = operator.xor(value, self.number_array[-13 + string.ascii_lowercase.index(file)])

            value = operator.xor(value, self.number_array[-1])

        else:
            if re.fullmatch("[a-h][7][-][a-h][5]", board.last_move):
                file = board.last_move[0]
                value = operator.xor(value, self.number_array[-13 + string.ascii_lowercase.index(file)])

        for i, c in enumerate(board.castling_rights):
            if c:
                value = operator.xor(value, self.number_array[-5 + i])

        return value

    def update_hash(self, current_hash, move, board):
        """Updates a board hash after a move has been made."""
        colour = move.colour
        start = (move.start[0] * 8) + move.start[1]
        destination = (move.destination[0] * 8) + move.destination[1]
        index = -5 if colour == Colour.WHITE else -3  # for castling rights

        if colour == Colour.WHITE:
            enemy_colour = colour.value + 1
        else:
            enemy_colour = colour.value - 1

        if move.is_capture:
            if str.islower(board.last_move[0]):
                symbol = "p"
                if move.en_passant:
                    current_hash = operator.xor(current_hash, self.number_array[
                        -13 + string.ascii_lowercase.index(board.last_move[0])])
            else:
                symbol = board.last_move[0].lower()

            current_hash = operator.xor(
                current_hash, self.number_array[destination + self.piece_values[symbol, enemy_colour]]
            )

            if symbol == "r":
                rook = board.array[move.destination[0]][move.destination[1]]

                if not rook.moves_made:
                    if move.destination[0] == 0:
                        current_hash = operator.xor(current_hash, self.number_array[index])
                    else:
                        current_hash = operator.xor(current_hash, self.number_array[index + 1])

        current_hash = operator.xor(
            current_hash, self.number_array[start + self.piece_values[move.piece_symbol, colour.value]]
        )

        if move.promotion:
            current_hash = operator.xor(
                current_hash, self.number_array[destination + self.piece_values[move.promotion.symbol, colour.value]]
            )
        else:
            current_hash = operator.xor(
                current_hash, self.number_array[destination + self.piece_values[move.piece_symbol, colour.value]]
            )

        if move.piece_symbol == "k":
            current_hash = operator.xor(current_hash, self.number_array[index])
            current_hash = operator.xor(current_hash, self.number_array[index + 1])

        elif move.piece_symbol == "r":
            piece = board.array[move.start[0]][move.start[1]]

            if not piece.moves_made:
                if move.start[0] == 0:
                    current_hash = operator.xor(current_hash, self.number_array[index])
                else:
                    current_hash = operator.xor(current_hash, self.number_array[index + 1])

        current_hash = operator.xor(current_hash, self.number_array[-1])

        return current_hash
