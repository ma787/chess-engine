"Module providing functions to generate and validate moves."

from chess_engine import attributes as attrs, move, lan_parser as lp


def in_check(bd):
    """Searches for a pseudo-legal capture of the side to move's king.

    Args:
        bd (Board): The board object to inspect.

    Returns:
        bool: True if a pseudo-legal move to capture the king exists,
        and False otherwise.
    """
    king_pos = bd.find_king(bd.black)

    for i in range(8):
        for j in range(8):
            if move.Move.find_threat(bd, (i, j), not bd.black, king_pos, capture=True):
                return True

    return False


def all_moves_from_position(bd, pos):
    """Finds all the possible legal moves that can be made by a piece at a given position.

    Args:
        bd (Board): The board to analyse.
        pos (tuple): The indices of the position to start from on the board
        array.

    Returns:
        list: A list of move objects consisting of every legal move
        starting from the given position on the board array.
    """
    all_moves = []
    piece = bd.array[pos[0]][pos[1]]

    if not piece or piece > 0 and bd.black or piece < 0 and not bd.black:
        return all_moves

    for i, row in enumerate(bd.array):
        final_rank = 0 if bd.black else 7

        for j, dest_square in enumerate(row):
            castling = None
            capture = dest_square * piece < 0
            capture |= move.Move.is_en_passant(bd, pos, (i, j))

            pr_types = (1, 3, 5, 6) if abs(piece) == 4 and i == final_rank else (0,)

            if (
                abs(piece) == 2
                and pos == (7 - final_rank, 4)
                and (i, j) in ((pos[0], 2), (pos[0], 6))
            ):
                castling = (
                    attrs.Castling.QUEEN_SIDE if j == 2 else attrs.Castling.KING_SIDE
                )

            if dest_square == 0 or capture:
                for p in pr_types:
                    move_obj = move.Move(
                        pos,
                        (i, j),
                        capture=capture,
                        promotion=p,
                        castling=castling,
                    )

                    if move_obj.legal(bd):
                        all_moves.append(move_obj)

    return all_moves


def all_possible_moves(bd):
    """Finds all the possible legal moves that the side to move can make.

    Args:
        bd (Board): The board to analyse.

    Returns:
        list: A list of move objects consisting of every legal move
        that the side to move can make.
    """
    all_moves = []

    for i in range(8):
        for j in range(8):
            all_moves.extend(all_moves_from_position(bd, (i, j)))

    return all_moves


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

    moves = all_possible_moves(bd)
    nodes = 0

    for m in moves:
        m.make_move(bd)
        nodes += perft(bd, depth - 1)
        m.unmake_move(bd)

    return nodes


def divide(bd, depth):
    """Prints every initial move from a position and how many child nodes it has.

    Args:
        bd (Board): The board position to begin the traversal from.
        depth (int): The depth at which the search should be halted.
    """
    moves = all_possible_moves(bd)

    for i, m in enumerate(moves):
        mstr = lp.convert_move_to_lan(m, bd)
        m.make_move(bd)
        n = perft(bd, depth - 1)
        print(f"({i+1}) {mstr} : {n}")
        m.unmake_move(bd)
