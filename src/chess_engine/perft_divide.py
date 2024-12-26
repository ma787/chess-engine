"""Module providing perft and divide functions for testing."""

from chess_engine import constants as cs, move, move_gen as mg


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
        if move.make_move(m, bd) != -1:
            nodes += perft(bd, depth - 1)
            promoted = bd.prev_state[-1][-1]
            move.unmake_move(m, bd)

            if promoted:
                for pc in (cs.N, cs.B, cs.R):
                    if move.make_move(m, bd, pr_type=pc) != -1:
                        nodes += perft(bd, depth - 1)
                        move.unmake_move(m, bd)

    return nodes


def get_result(bd, mv, depth, total, pr_type=cs.Q):
    """Outputs the perft result after a move is made from the starting position."""
    if move.make_move(mv, bd, pr_type=pr_type) != -1:
        n = perft(bd, depth - 1)
        total += n
        move.unmake_move(mv, bd)
        return n, total

    return 0, total


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
        mstr = move.int_to_string(bd, m)
        n, total = get_result(bd, m, depth, total)
        if n:
            print(f"{mstr} {n}", file=stdout)

        if len(mstr) == 5:  # promotion
            for pc in (cs.N, cs.B, cs.R):
                mstr = mstr[:4] + cs.LETTERS[pc + cs.BVAL].lower()
                n, total = get_result(bd, m, depth, total, pr_type=pc)
                print(f"{mstr} {n}", file=stdout)

    print(f"\n{total}", file=stdout)
