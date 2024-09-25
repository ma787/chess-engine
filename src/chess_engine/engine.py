"Module providing the chess engine implementation."

import math

from chess_engine import (
    hashing,
    lan_parser as lp,
    move_generation as mg,
)


class Engine:
    """The chess engine implementation.

    Attributes:
        black (bool): Whether the engine object is playing as black.
        hashing (Hashing)": The Hashing object to use for hashing board positions.
        t_table (dict): The transposition table, used to store previously
            evaluated positions and their scores:
                hashed position: (move_string, score)
    """

    def __init__(self, black):
        self.black = black
        self.hashing = hashing.Hashing()
        self.t_table = {}

    def alpha_beta_search(self, board, alpha, beta, depth):
        """Finds the highest score attainable from the current position.

        Args:
            board (Board): The board to analyse.
            alpha (int): The score below which any positions are discarded.
            beta (int): The score above which any positions are discarded.
            depth (int): The depth to reach in the search tree.

        Returns:
            int: The highest score found for the given position.
        """
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

                    self.t_table[board_hash] = (
                        lp.convert_move_to_lan(move, board),
                        value,
                    )
                    return beta  # fail-high node

                if value > alpha:
                    best_move = move
                    alpha = value

                move.unmake_move(board)

        selected_move = (
            lp.convert_move_to_lan(best_move, board)
            if best_move is not None
            else None  # either a terminal or a fail-low node
        )

        self.t_table[board_hash] = (selected_move, value)
        return alpha

    def find_move(self, board):
        """Performs a search and returns the move that led to the best score.

        Args:
            board (Board): The board to analyse.

        Returns:
            Move: A move object representing the best move found in the search.
        """
        board_hash = self.hashing.zobrist_hash(board)
        depth = 3

        for key, _ in self.t_table.items():
            if board_hash == key:
                return self.t_table[board_hash][0]

        self.alpha_beta_search(board, -math.inf, math.inf, depth)
        return self.t_table[board_hash][0]

    @staticmethod
    def evaluate(board):
        """Returns the value of a certain position.

        Args:
            board (Board): The board to analyse.

        Returns:
            int: The score evaluated for the given board position.
            Negative if the side to move is black.
        """
        # the utility of a piece varies with its position
        square_values = {
            1: [  # bishop
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20],
            ],
            2: [  # king
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20],
            ],
            3: [  # knight
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50],
            ],
            4: [  # pawn
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            5: [  # queen
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20],
            ],
            6: [  # rook
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0],
            ],
        }

        piece_values = {
            1: 3,
            2: 10000000,
            3: 3,
            4: 1,
            5: 9,
            6: 5,
        }

        material_values = [0, 0]
        mobility = 0

        for i in range(8):
            for j in range(8):
                square = board.array[i][j]

                if square:
                    rank = i if square > 0 else 7 - i
                    material_values[int(square < 0)] += (
                        piece_values[abs(square)] + square_values[abs(square)][rank][j]
                    )
                    mobility += len(mg.all_moves_from_position(board, (i, j)))

        if board.black:
            material = (material_values[1] - material_values[0]) * -1
            mobility *= -1
        else:
            material = material_values[0] - material_values[1]

        return material + mobility
