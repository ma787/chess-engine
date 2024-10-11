"""Module providing perft and divide functions for testing."""

from chess_engine import lan_parser as lp, move, move_generation as mg


def perft(bd, depth):
    """Returns the number of nodes at a given depth beginning from a position.

    Args:
        bd (Board): The board position to begin the traversal from.
        depth (int): The depth at which the search should be halted.

    Returns:
        int: The number of nodes encountered at the search depth.
    """
    if depth == 0:
        return 1

    moves = mg.all_legal_moves(bd)
    nodes = 0

    for m in moves:
        move.make_move(m, bd)
        nodes += perft(bd, depth - 1)
        move.unmake_move(m, bd)

    return nodes


def divide(bd, depth):
    """Prints every initial move from a position and how many child nodes it has.

    Args:
        bd (Board): The board position to begin the traversal from.
        depth (int): The depth at which the search should be halted.
    """
    moves = mg.all_legal_moves(bd)

    for i, m in enumerate(moves):
        mstr = lp.convert_move_to_lan(m, bd)
        move.make_move(m, bd)
        n = perft(bd, depth - 1)
        print(f"({i+1}) {mstr} : {n}")
        move.unmake_move(m, bd)
