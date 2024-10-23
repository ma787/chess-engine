"Module providing functions to generate and validate moves."
import numpy as np


from chess_engine import constants as cs, move


def x88_diff(a, b):
    """Returns the 0x88 difference between indices a and b."""
    return 0x77 + a - b


def square_under_threat(bd, pos, black):
    """Checks if a position can be attacked by a side.

    Args:
        bd (Board): The board to analyse.
        pos (int): The index of the position to check for attacks
            on. Must be either empty or occupied by the opposing side.
        black (int): Whether the attacking side is black.

    Returns:
        bool: True if a pseudo-legal attack on any of the squares exists,
            otherwise False.
    """
    switch = bd.black != black

    if black:
        piece_locs = np.where(bd.array < 0)[0]
    else:
        piece_locs = np.where(bd.array > 0)[0]

    if switch:
        bd.switch_side()

    threat = False

    for loc in piece_locs:
        diff = pos - loc
        x88 = x88_diff(pos, loc)
        p_type = int(abs(bd.array[loc]))
        valid = False

        if p_type == cs.PAWN:
            vec = cs.VECTORS[cs.VALID_PAWN_VECTORS[black]]
            valid = diff in (vec + cs.VECTORS["E"], vec + cs.VECTORS["W"])

        elif cs.MOVE_TABLE[x88] & (1 << (p_type - 1)):
            valid = True

            if p_type not in (cs.KING, cs.KNIGHT):
                v = int(diff / cs.CHEBYSHEV[x88])
                current = loc + v

                while current != pos:
                    if bd.array[current]:
                        valid = False
                        break
                    current += v

        if valid:
            capture = bd.array[loc] * bd.array[pos] < 0
            if move.pseudo_legal(move.encode_move(loc, pos, capture=capture), bd):
                threat = True
                break

    if switch:
        bd.switch_side()

    return threat


def in_check(bd):
    """Checks if the side to move's king is under attack."""
    return square_under_threat(bd, bd.find_king(bd.black), bd.black ^ 1)


def legal(mv, bd):
    """Checks if a pseudo-legal move does not leave the king in check.

    Args:
        mv (int): The move integer.
        bd (Board): The board to analyse.

    Returns:
        bool: True if the move is legal, and False otherwise.
    """
    [_, _, _, castling, _] = move.get_info(mv)

    if castling:
        squares = (
            np.array([2, 3, 4]) if castling == cs.QUEENSIDE else np.array([4, 5, 6])
        )
        squares += 0x70 * bd.black
        for sqr in squares:
            if square_under_threat(bd, sqr, bd.black ^ 1):
                return False
        return True

    try:
        move.make_move(mv, bd)
    except ValueError:
        return False

    valid = not square_under_threat(bd, bd.find_king(bd.black ^ 1), bd.black)
    move.unmake_move(mv, bd)

    return valid


def check_and_append(bd, info, moves):
    """Checks if a move is pseudo-legal and appends it to a list if so."""
    mv = move.encode_move(
        info[0], info[1], capture=info[2], castling=info[3], promotion=info[4]
    )
    if move.pseudo_legal(mv, bd):
        moves.append(mv)


def gen_pawn_moves(bd, pos):
    """Finds all pseudo-legal pawn moves from a position."""

    def check_pawn_move(bd, dest, moves, capture=False):
        if not dest & 0x88:
            if (dest >> 4) == (7 * (bd.black ^ 1)):
                for p_type in (cs.BISHOP, cs.KNIGHT, cs.QUEEN, cs.ROOK):
                    check_and_append(bd, [pos, dest, capture, 0, p_type], moves)
            else:
                check_and_append(bd, [pos, dest, capture, 0, cs.NULL_PIECE], moves)

    moves = []
    v = cs.VALID_PAWN_VECTORS[bd.black]
    vec = cs.VECTORS[v]

    check_pawn_move(bd, pos + vec, moves)

    # check for double pawn push
    if (pos >> 4) == 1 + 5 * bd.black and not bd.array[pos + vec]:
        check_pawn_move(bd, pos + 2 * vec, moves)

    for d in ("E", "W"):
        cap_vec = cs.VECTORS[v + d]
        cap_pos = pos + cap_vec

        if (
            not cap_pos & 0x88
            and bd.array[cap_pos] != cs.NULL_PIECE
            or (cap_pos - vec) == bd.ep_square
        ):
            check_pawn_move(bd, cap_pos, moves, capture=True)

    return moves


def all_moves_from_position(bd, pos):
    """Finds all pseudo-legal moves from a position.

    Args:
        bd (Board): The board to analyse.
        pos (int): The index of the position to start from on the board
        array.

    Returns:
        list: A list of integers consisting of every legal move
        starting from the given position on the board array.
    """

    def check_piece_move(bd, start, dest, moves):
        if not dest & 0x88:
            product = bd.array[start] * bd.array[dest]
            if product <= 0:
                check_and_append(
                    bd, [start, dest, product < 0, 0, cs.NULL_PIECE], moves
                )

    moves = []
    sqr = bd.array[pos]

    if not sqr or sqr * (1 - 2 * bd.black) < 0:
        return moves

    p_type = int(abs(bd.array[pos]))

    if p_type == cs.KNIGHT:
        for v in cs.KNIGHT_VECTORS:
            check_piece_move(bd, pos, pos + v, moves)
    elif p_type == cs.KING:
        c_off = 2 * int(bd.black ^ 1)

        for c, info in cs.C_INFO.items():
            if bd.get_castling_rights(c_off + info[0]):
                rook = bd.array[move.get_rook_castle(bd, c)[0]]
                dest = pos + info[1]

                if (
                    abs(rook) == cs.ROOK
                    and rook * bd.array[pos] > 0
                    and not bd.array[dest]
                ):
                    check_and_append(bd, [pos, dest, False, c, cs.NULL_PIECE], moves)

        for v in cs.VALID_VECTORS[p_type]:
            check_piece_move(bd, pos, pos + cs.VECTORS[v], moves)

    elif p_type == cs.PAWN:
        return gen_pawn_moves(bd, pos)
    else:
        for v in cs.VALID_VECTORS[p_type]:
            vec = cs.VECTORS[v]
            dest = pos + vec

            while (not dest & 0x88) and not bd.array[dest]:
                check_piece_move(bd, pos, dest, moves)
                dest += vec

            check_piece_move(bd, pos, dest, moves)

    return moves


def all_pseudo_legal_moves(bd):
    """Finds all the pseudo-legal moves that the side to move can make."""
    moves = []

    if bd.black:
        piece_locs = np.where(bd.array < 0)[0]
    else:
        piece_locs = np.where(bd.array > 0)[0]

    for pos in piece_locs:
        moves.extend(all_moves_from_position(bd, pos))

    return moves


def all_legal_moves(bd):
    """Finds all the legal moves that the side to move can make."""
    return [mv for mv in all_pseudo_legal_moves(bd) if legal(mv, bd)]
