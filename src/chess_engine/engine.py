"Module providing the chess engine implementation."

import math

from chess_engine import (
    constants as cs,
    hashing as hsh,
    lan_parser as lp,
    move,
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
        self.t_table = {}

    def alpha_beta_search(self, bd, alpha, beta, depth):
        """Finds the highest score attainable from the current position.

        Args:
            bd (Board): The board to analyse.
            alpha (int): The score below which any positions are discarded.
            beta (int): The score above which any positions are discarded.
            depth (int): The depth to reach in the search tree.

        Returns:
            int: The highest score found for the given position.
        """
        if depth == 0:
            return Engine.evaluate(bd)

        board_hash = hsh.zobrist_hash(bd)

        for key, _ in self.t_table.items():
            if board_hash == key:
                return self.t_table[board_hash][1]

        value = -math.inf

        moves = mg.all_legal_moves(bd)
        no_moves = len(moves) == 0
        best_move = 0

        if no_moves:
            if not mg.square_under_threat(bd, bd.find_king(bd.black), not bd.black):
                value = 0

        else:
            for mv in moves:
                move.make_move(mv, bd)
                value = max(
                    value, -self.alpha_beta_search(bd, -beta, -alpha, depth - 1)
                )

                if value >= beta:
                    move.unmake_move(mv, bd)

                    self.t_table[board_hash] = (
                        lp.convert_move_to_lan(mv, bd),
                        value,
                    )
                    return beta  # fail-high node

                if value > alpha:
                    best_move = mv
                    alpha = value

                move.unmake_move(mv, bd)

        self.t_table[board_hash] = (best_move, value)
        return alpha

    def find_move(self, bd):
        """Performs a search and returns the move that led to the best score.

        Args:
            bd (Board): The board to analyse.

        Returns:
            Move: A move object representing the best move found in the search.
        """
        board_hash = hsh.zobrist_hash(bd)
        depth = 3

        for key, _ in self.t_table.items():
            if board_hash == key:
                return self.t_table[board_hash][0]

        self.alpha_beta_search(bd, -math.inf, math.inf, depth)
        return self.t_table[board_hash][0]

    @staticmethod
    def evaluate(bd):
        """Returns the value of a certain position.

        Args:
            bd (Board): The board to analyse.

        Returns:
            int: The score evaluated for the given board position.
            Negative if the side to move is black.
        """
        material_values = [0, 0]
        mobility = 0

        for i in range(8):
            for j in range(8):
                square = bd.array[i][j]

                if square:
                    rank = i if square > 0 else 7 - i
                    material_values[int(square < 0)] += (
                        cs.PIECE_VALS[abs(square)]
                        + cs.SQUARE_VALS[abs(square)][rank][j]
                    )
                    mobility += len(mg.all_moves_from_position(bd, (i, j)))

        if bd.black:
            material = (material_values[1] - material_values[0]) * -1
            mobility *= -1
        else:
            material = material_values[0] - material_values[1]

        return material + mobility
