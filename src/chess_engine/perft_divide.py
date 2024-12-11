"""Module providing perft and divide functions for testing."""

from chess_engine import constants as cs, move, move_gen as mg, utils


def int_to_string(mv, promoted=False):
    """Converts a move integer to a move string."""
    start, dest, _ = move.decode(mv)
    promotion = "q" if promoted else ""

    return (
        utils.coord_to_string(start) + utils.coord_to_string(dest) + promotion
    ).strip()


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
        result = move.make_move(m, bd)
        if result != -1:
            nodes += perft(bd, depth - 1)
            promoted = bd.prev_state[-1][-1]
            move.unmake_move(m, bd)

            if promoted:
                for pc in (cs.N, cs.B, cs.R):
                    result = move.make_move(m, bd, pr_type=pc)
                    if result != -1:
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
        result = move.make_move(m, bd)
        if result != -1:
            n = perft(bd, depth - 1)
            total += n
            promoted = bd.prev_state[-1][-1]

            mstr = int_to_string(m, promoted)
            print(f"{mstr} {n}", file=stdout)
            move.unmake_move(m, bd)

            if promoted:
                for pc in (cs.N, cs.B, cs.R):
                    mstr = mstr[:4] + cs.LETTERS[pc + cs.BVAL].lower()
                    result = move.make_move(m, bd, pr_type=pc)
                    if result != -1:
                        n = perft(bd, depth - 1)
                        total += n

                        print(f"{mstr} {n}", file=stdout)
                        move.unmake_move(m, bd)

    print(f"\n{total}", file=stdout)
