"Module providing the chess engine implementation."

import math
import time

from chess_engine import (
    constants as cs,
    eval_tables as et,
    hashing as hsh,
    move,
    move_gen as mg,
)


def evaluate(bd):
    """Returns the value of a certain position.

    Args:
        bd (Board): The board to analyse.

    Returns:
        int: The relative score evaluated for the given board position.
    """
    material_values = [0, 0]
    i = 0x44

    while i < 0xBC:
        square = bd.array[i]

        if square == cs.GD:
            i += 8
            continue

        if square:
            square_val = et.P_SQUARE_VALS[square & 15][i]
            material_values[bd.black] += square_val

        i += 1

    if bd.black:
        material = (material_values[1] - material_values[0]) * -1
    else:
        material = material_values[0] - material_values[1]

    return material


def search(bd, alpha, beta, depth, t_table=None):
    """Searches the game tree to a given depth to find the highest attainable score.

    Args:
        bd (Board): The board to analyse.
        alpha (int): The score below which any positions are discarded.
        beta (int): The score above which any positions are discarded.
        depth (int): The depth to reach in the search tree.
        t_table (dict, optional): A table that stores information about visited
            positions in the following format:
            board hash: (best move, score)

    Returns:
        int: The highest score found for the given position.
    """
    if t_table is None:
        t_table = {}

    if depth == 0:
        return evaluate(bd)

    b_hash = hsh.zobrist_hash(bd)

    for key, _ in t_table.items():
        if b_hash == key:
            return t_table[b_hash][1]

    value = -math.inf

    moves = mg.all_moves(bd)
    best_move = 0
    found_move = False

    for mv in moves:
        result = move.make_move(mv, bd)
        if result == -1:
            continue
        found_move = True

        value = max(value, -search(bd, -beta, -alpha, depth - 1, t_table=t_table))

        if value >= beta:
            move.unmake_move(mv, bd)
            t_table[b_hash] = (mv, value)
            return beta  # fail-high node

        if value > alpha:
            best_move = mv
            alpha = value

        move.unmake_move(mv, bd)

    if not (found_move or bd.check):
        value = 0

    t_table[b_hash] = (best_move, value)
    return alpha


def find_move(bd, remaining_time, t_table=None):
    """Performs a search and returns the move that led to the best score.

    Args:
        bd (Board): The board to analyse.
        remaining_time (int): The remaining time in the game.
        t_table (dict, optional): A table that stores information about visited
            positions in the following format:
            board hash: (best move, score)

    Returns:
        string: The move string of the best move found in the search.
    """
    start = time.time()

    if t_table is None:
        t_table = {}

    board_hash = hsh.zobrist_hash(bd)

    search_time = remaining_time / 20  # estimate of number of moves in a game
    i = 0

    while time.time() - start < search_time:
        search(bd, -math.inf, math.inf, i, t_table=t_table)
        i += 1

    return move.int_to_string(bd, t_table[board_hash][0])
