"Module providing the chess engine implementation."

import math

from chess_engine import (
    constants as cs,
    eval_tables as et,
    hashing as hsh,
    move,
    move_generation as mg,
    utils,
)


class Engine:
    """The chess engine implementation.

    Attributes:
        black (int): Whether the engine object is playing as black.
        t_table (dict): The transposition table, used to store previously
            evaluated positions and their scores:
                hashed position: (move, score)
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

        moves = mg.all_moves(bd)
        no_moves = len(moves) == 0
        best_move = 0

        if no_moves:
            if not mg.in_check(bd):
                value = 0

        else:
            for mv in moves:
                move.make_move(mv, bd)
                value = max(
                    value, -self.alpha_beta_search(bd, -beta, -alpha, depth - 1)
                )

                if value >= beta:
                    move.unmake_move(mv, bd)
                    self.t_table[board_hash] = (mv, value)
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
        depth = 4

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
        i = 0

        while i < 128:
            square = bd.array[i]

            if square:
                if (
                    utils.is_type(square, cs.K)
                    and len(bd.piece_list[cs.Q]) == 0
                    and len(bd.piece_list[utils.get_piece(cs.Q, cs.BLACK)]) == 0
                ):
                    square_val = et.END_VALS[bd.black][i]
                else:
                    square_val = et.P_SQUARE_VALS[square][i]

                material_values[bd.black] += square_val

            i += 1

            if i & 0x88:
                i += 8

        if bd.black:
            material = (material_values[1] - material_values[0]) * -1
        else:
            material = material_values[0] - material_values[1]

        return material
