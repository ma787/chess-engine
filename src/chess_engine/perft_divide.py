"""Module providing perft and divide functions for testing."""

from chess_engine import move, move_generation as mg


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

    moves = mg.all_moves(bd)
    nodes = 0

    for m in moves:
        move.make_move(m, bd)
        nodes += perft(bd, depth - 1)
        move.unmake_move(m, bd)

    return nodes


def divide(bd, depth, stdout=None):
    """Prints every initial move from a position and how many child nodes it has.

    Args:
        bd (Board): The board position to begin the traversal from.
        depth (int): The depth at which the search should be halted.
        stdout (SupportsWrite[str], optional): The file object the
            print function should write to. Defaults to None.
    """
    moves = mg.all_moves(bd)
    total = 0

    for m in moves:
        move.make_move(m, bd)
        n = perft(bd, depth - 1)
        total += n
        print(f"{m} {n}", file=stdout)
        move.unmake_move(m, bd)

    print(f"\n{total}", file=stdout)
