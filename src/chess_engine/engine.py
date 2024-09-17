"Module providing the chess engine implementation."

import math

from chess_engine import (
    attributes as attrs,
    hashing,
    lan_parser as lp,
    move_generation as mg,
)


class Engine:
    """The chess engine implementation.

    Attributes:
        colour (Colour): The side to move of the engine object.
        hashing (Hashing)": The Hashing object to use for hashing board positions.
        t_table (dict): The transposition table, used to store previously
            evaluated positions and their scores:
                hashed position: (move_string, score)
    """

    def __init__(self, colour):
        self.colour = colour
        self.hashing = hashing.Hashing()
        self.t_table = {}

    def alpha_beta_search(self, board, alpha, beta, depth):
        """Finds the highest score attainable from the current position."""
        if depth == 0:
            return Engine.evaluate(board)

        board_hash = self.hashing.zobrist_hash(board)

        for key, _ in self.t_table.items():
            if board_hash == key:
                return self.t_table[board_hash][1]

        value = -math.inf

        moves = mg.all_possible_moves(board)
        no_moves = len(moves) == 0
        best_move = None

        if no_moves:
            if not mg.in_check(board):
                value = 0

        else:
            for move in moves:
                move.make_move(board)
                value = max(
                    value, -self.alpha_beta_search(board, -beta, -alpha, depth - 1)
                )

                if value >= beta:
                    move.unmake_move(board)
                    self.t_table[board_hash] = (lp.convert_move_to_lan(move), value)
                    return beta  # fail-high node

                if value > alpha:
                    best_move = move
                    alpha = value

                move.unmake_move(board)

        if best_move is not None:
            best_move = lp.convert_move_to_lan(best_move)

        else:  # either a terminal or a fail-low node
            best_move = None if no_moves else moves[0]

        self.t_table[board_hash] = (best_move, value)
        return alpha

    def find_move(self, board):
        """Performs a search and returns the move that led to the best score."""
        board_hash = self.hashing.zobrist_hash(board)
        depth = 3

        if board_hash in self.t_table.keys():
            return self.t_table[board_hash][0]

        else:
            self.alpha_beta_search(board, -math.inf, math.inf, depth)
            return self.t_table[board_hash][0]

    @staticmethod
    def evaluate(board):
        """Returns the value of a certain position."""
        score = 0

        white_squares = {
            "p": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "b": [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20],
            ],
            "n": [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50],
            ],
            "r": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0],
            ],
            "q": [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20],
            ],
            "k": [
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20],
            ],
        }  # the utility of a piece varies with its position

        black_squares = {x: list(reversed(y)) for x, y in white_squares.items()}

        white_pieces = []
        black_pieces = []

        for i in range(8):
            for j in range(8):
                square = board.array[i][j]
                if square:
                    if square.colour == attrs.Colour.WHITE:
                        white_pieces.append(square)
                    else:
                        black_pieces.append(square)

        white_material = sum(
            [
                piece.value
                + white_squares[piece.symbol][piece.position[0]][piece.position[1]]
                for piece in white_pieces
            ]
        )

        black_material = sum(
            [
                piece.value
                + black_squares[piece.symbol][piece.position[0]][piece.position[1]]
                for piece in black_pieces
            ]
        )

        if board.side_to_move == attrs.Colour.WHITE:
            mobility = len(
                [
                    mg.all_moves_from_position(board, piece.position)
                    for piece in white_pieces
                ]
            )
            material = white_material - black_material
            score = material + mobility
        else:
            mobility = len(
                [
                    mg.all_moves_from_position(board, piece.position)
                    for piece in black_pieces
                ]
            )
            material = (black_material - white_material) * -1
            score = material - mobility

        return score
