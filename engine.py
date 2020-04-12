import math
import operator
import random
import board_rep


class Searching:
    def __init__(self):
        self.number_array = zobrist_generator()
        self.transposition_table = []  # contains (hashed board position, move class, score, node type)


def evaluate(board):
    """Returns the value of a certain position."""
    test_board = board_rep.ChessBoard()
    test_board.__dict__ = board.__dict__

    pieces = [x for x in board.piece_list if x.colour == board.side_to_move]
    enemy_pieces = list(set(board.piece_list) - set(pieces))

    value = 0

    for piece_type in (board_rep.Bishop, board_rep.Knight, board_rep.Rook, board_rep.Queen, board_rep.King):
        pos_score = sum([x.value for x in pieces if x.symbol == piece_type.symbol])
        neg_score = sum([x.value for x in enemy_pieces if x.symbol == piece_type.symbol])
        value += pos_score - neg_score

    value += len(board.check_possible_moves(test_board))

    return value


def zobrist_generator():
    """Generates pseudo-random numbers for each piece type and colour for each square on the board."""
    random.seed(1)  # pseudo-random number generation for reproducibility
    array = [[random.randint(1, 1000000) for x in range(1, 13)] for y in range(64)]
    return array


def zobrist_hash(board, array):  # does not consider castling rights or en passant status
    """Hashes a board position to a unique number."""
    value = 0

    piece_values = {("p", board_rep.Colour.WHITE): 0,
                    ("b", board_rep.Colour.WHITE): 1,
                    ("n", board_rep.Colour.WHITE): 2,
                    ("r", board_rep.Colour.WHITE): 3,
                    ("q", board_rep.Colour.WHITE): 4,
                    ("k", board_rep.Colour.WHITE): 5,
                    ("p", board_rep.Colour.BLACK): 6,
                    ("b", board_rep.Colour.BLACK): 7,
                    ("n", board_rep.Colour.BLACK): 8,
                    ("r", board_rep.Colour.BLACK): 9,
                    ("q", board_rep.Colour.BLACK): 10,
                    ("k", board_rep.Colour.BLACK): 11
                    }

    for i, row in enumerate(board.array):
        for j, square in enumerate(row):
            if square:
                index = piece_values[(square.symbol, square.colour)]
                value = operator.xor(value, array[i * j][index])

    operator.xor(value, board.side_to_move.value)

    return value


def convert_move_to_lan(move):
    """Converts a move class to LAN."""
    user_input = []

    if move.castling:
        if move.castling == board_rep.Castling.QUEEN_SIDE:
            return "0-0-0"
        else:
            return "0-0"

    if move.piece_class != board_rep.Pawn:
        user_input.append(move.piece.symbol.upper())

    user_input.append(list(move.virtual_board.letter_ref.keys())[list(move.virtual_board.letter_ref.values()).index(
        move.start[1]
    )])

    user_input.append(str(move.start[0] + 1))

    if move.is_capture:
        user_input.append("x")
    else:
        user_input.append("-")

    user_input.append(list(move.virtual_board.letter_ref.keys())[list(move.virtual_board.letter_ref.values()).index(
        move.destination[1]
    )])

    user_input.append(str(move.destination[0] + 1))

    if move.promotion:
        user_input.append(move.promotion.symbol.upper())

    user_input = "".join(user_input)

    return user_input
