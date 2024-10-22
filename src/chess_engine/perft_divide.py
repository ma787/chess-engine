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

    def convert_move_string(mstr, bd):
        promotion = ""

        if mstr[0:3] == "0-0":
            rank = str(1 + 7 * int(bd.black))
            file = "g" if len(mstr) == 3 else "c"
            return "e" + rank + file + rank

        if len(mstr) == 6:
            if mstr[-1].isupper():
                promotion = mstr[-1].lower()
                mstr = mstr[:-1]
            else:
                mstr = mstr[1:]

        return mstr[0:2] + mstr[3:5] + promotion

    moves = mg.all_legal_moves(bd)
    total = 0

    for m in moves:
        mstr = lp.convert_move_to_lan(m, bd)
        mstr_conv = convert_move_string(mstr, bd)
        move.make_move(m, bd)
        n = perft(bd, depth - 1)
        total += n
        print(f"{mstr_conv} {n}")
        move.unmake_move(m, bd)

    print(f"\n{total}")
