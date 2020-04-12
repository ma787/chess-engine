from enum import Enum
import math
import operator
import random
import board_rep


class NodeType(Enum):
    PV = 1
    CUT = 2
    ALL = 3


class Searching:
    def __init__(self):
        self.number_array = zobrist_generator()
        self.transposition_table = []  # contains (hashed board position, move class, depth, score, node type)

    def alpha_beta_search(self, alpha, beta, depth, board, virtual_game=None):
        """Finds the highest score attainable from the current position."""
        test_board = board_rep.ChessBoard()
        test_board.__dict__ = board.__dict__
        board_hash = zobrist_hash(board, self.number_array)

        # TODO: implement virtual_game for check status and side to move

        if depth == 0:
            score = evaluate(test_board)
            self.transposition_table.append((board_hash, None, depth, score, NodeType.PV))
            return score

        prev_searched = None

        for table in self.transposition_table:  # checks if the current node has already been reached
            if board_hash == table[0]:
                prev_searched = table
                break

        if prev_searched:
            if prev_searched[-1] == NodeType.CUT:
                return beta
            else:
                return alpha

        if len(self.transposition_table) > 128:
            self.transposition_table.remove(self.transposition_table[0])

        possible_moves = board.check_possible_moves(test_board)

        for move in possible_moves:
            new_board = move.check_move()
            move.perform_move(new_board)

            user_input = convert_move_to_lan(move)
            new_board.past_three_moves.append(user_input)

            if new_board.side_to_move == board_rep.Colour.WHITE:
                new_board.side_to_move = board_rep.Colour.BLACK
            else:
                new_board.side_to_move = board_rep.Colour.WHITE  # updating the board state

            score = -self.alpha_beta_search(-beta, -alpha, depth - 1, new_board, virtual_game=virtual_game)
            # applied recursively to reach required depth
            # opponent's gains = engine's losses so values are reversed

            if score >= beta:
                self.transposition_table.append((board_hash, move, depth, beta, NodeType.CUT))
                return beta

            changed = False

            if score > alpha:
                alpha = score
                changed = True
                move_change = move

        if changed:
            self.transposition_table.append((board_hash, move_change, depth, alpha, NodeType.PV))
        else:
            self.transposition_table.append((board_hash, None, depth, alpha, NodeType.ALL))

        return alpha

    def find_move(self, board):  # 'retraces' the path of the alpha-beta search
        """Finds the move that will attain the best score."""
        test_board = board_rep.ChessBoard()
        test_board.__dict__ = board.__dict__

        board_hash = zobrist_hash(board, self.number_array)
        score = self.alpha_beta_search(math.inf, (-math.inf), 3, test_board)

        for t in self.transposition_table:
            if t[0] == board_hash:
                table = t
                break

        depth = table[2]
        move = table[1]

        # incomplete


def evaluate(board):
    """Returns the value of a certain position."""
    test_board = board_rep.ChessBoard()
    test_board.__dict__ = board.__dict__

    white_piece_values = {"p": [[0, 0, 0, 0, 0, 0, 0, 0],
                                [50, 50, 50, 50, 50, 50, 50, 50],
                                [10, 10, 20, 30, 30, 20, 10, 10],
                                [5, 5, 10, 25, 25, 10, 5, 5],
                                [0, 0, 0, 20, 20, 0, 0, 0],
                                [5, -5, -10, 0, 0, -10, -5, 5],
                                [5, 10, 10, -20, -20, 10, 10, 5],
                                [0, 0, 0, 0, 0, 0, 0, 0]],

                          "b": [[-20, -10, -10, -10, -10, -10, -10, -20],
                                [-10, 0, 0, 0, 0, 0, 0, -10],
                                [-10, 0, 5, 10, 10, 5, 0, -10],
                                [-10, 5, 5, 10, 10, 5, 5, -10],
                                [-10, 0, 10, 10, 10, 10, 0, -10],
                                [-10, 10, 10, 10, 10, 10, 10, -10],
                                [-10, 5, 0, 0, 0, 0, 5, -10],
                                [-20, -10, -10, -10, -10, -10, -10, -20]],

                          "n": [[-50, -40, -30, -30, -30, -30, -40, -50],
                                [-40, -20, 0, 0, 0, 0, -20, -40],
                                [-30, 0, 10, 15, 15, 10, 0, -30],
                                [-30, 5, 15, 20, 20, 15, 5,-30],
                                [-30, 0, 15, 20, 20, 15, 0, -30],
                                [-30, 5, 10, 15, 15, 10, 5, -30],
                                [-40, -20, 0, 5, 5, 0, -20, -40],
                                [-50, -40, -30, -30, -30, -30, -40, -50]],

                          "r": [[0, 0, 0, 0, 0, 0, 0, 0],
                                [5, 10, 10, 10, 10, 10, 10, 5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [0, 0, 0, 5, 5, 0, 0, 0]],

                          "q": [[-20, -10, -10, -5, -5, -10, -10, -20],
                                [-10, 0, 0, 0, 0, 0, 0, -10],
                                [-10, 0, 5, 5, 5, 5, 0, -10],
                                [-5, 0, 5, 5, 5, 5, 0, -5],
                                [0, 0, 5, 5, 5, 5, 0, -5],
                                [-10, 5, 5, 5, 5, 5, 0, -10],
                                [-10, 0, 5, 0, 0, 0, 0, -10],
                                [-20, -10, -10, -5, -5, -10, -10, -20]],

                          "k": [[-30, -40, -40, -50, -50, -40, -40, -30],
                                [-30, -40, -40, -50, -50, -40, -40, -30],
                                [-30, -40, -40, -50, -50, -40, -40, -30],
                                [-30, -40, -40, -50, -50, -40, -40, -30],
                                [-20, -30, -30, -40, -40, -30, -30, -20],
                                [-10, -20, -20, -20, -20, -20, -20, -10],
                                [20, 20, 0, 0, 0, 0, 20, 20],
                                [20, 30, 10, 0, 0, 10, 30, 20]]
                          }  # pieces are more or less useful at certain positions

    black_piece_values = {x: list(reversed(y)) for x, y in white_piece_values.items()}

    white_values = []
    black_values = []

    for i, row in enumerate(board.array):
        for j, square in enumerate(row):
            if square:
                if square.colour == board_rep.Colour.WHITE:
                    white_values.append(square.value + white_piece_values[square.symbol][i][j])
                else:
                    black_values.append(square.value + black_piece_values[square.symbol][i][j])

    if board.side_to_move == board_rep.Colour.WHITE:
        value = sum(white_values) - sum(black_values)
        multiplier = 1  # opposite signs to distinguish between black and white
    else:
        value = sum(black_values) - sum(white_values)
        multiplier = -1

    value += len(board.check_possible_moves(test_board))
    value *= multiplier

    return value


def zobrist_generator():
    """Generates pseudo-random numbers for each piece type and colour for each square on the board."""
    random.seed(1)  # pseudo-random number generation for reproducibility
    array = [[] for x in range(8)]

    for row in range(8):
        for square in range(8):
            array[row].append([random.randint(1, 1000000) for x in range(1, 14)])

    array.append([random.randint(1, 1000000), random.randint(1, 100000)])
    return array


def zobrist_hash(board, array):
    """Hashes a board position to a unique number."""
    value = 0

    piece_values = {('p', board_rep.Colour.WHITE.value): 0,
                    ('b', board_rep.Colour.WHITE.value): 1,
                    ('n', board_rep.Colour.WHITE.value): 2,
                    ('r', board_rep.Colour.WHITE.value): 3,
                    ('q', board_rep.Colour.WHITE.value): 4,
                    ('k', board_rep.Colour.WHITE.value): 5,
                    ('p', board_rep.Colour.BLACK.value): 6,
                    ('b', board_rep.Colour.BLACK.value): 7,
                    ('n', board_rep.Colour.BLACK.value): 8,
                    ('r', board_rep.Colour.BLACK.value): 9,
                    ('q', board_rep.Colour.BLACK.value): 10,
                    ('k', board_rep.Colour.BLACK.value): 11
                    }

    for i, row in enumerate(board.array):
        for j, square in enumerate(row):
            if square:
                index = piece_values[(square.symbol, square.colour.value)]
            else:
                index = 12

            value = operator.xor(value, array[i][j][index])

    operator.xor(value, array[-1][board.side_to_move.value])

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


search_class = Searching()
