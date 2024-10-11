"Module providing functions to generate and validate moves."
import numpy as np


from chess_engine import constants as cs, move


def x88_diff(a, b):
    """Returns the 0x88 difference between indices a and b."""
    return 0x77 + a - b


def find_vector_from_diff(diff):
    """Returns the direction of movement from a square difference."""
    if abs(diff) < 8:
        return "E" if diff > 0 else "W"

    if diff % 16 == 0:
        return "S" if diff > 0 else "N"

    if diff % 17 == 0:
        return "SE" if diff > 0 else "NW"

    return "SW" if diff > 0 else "NE"


def square_under_threat(bd, pos, black):
    """Checks if a position can be attacked by a side.

    Args:
        bd (Board): The board to analyse.
        pos (int): The index of the position to check for attacks
            on. Must be either empty or occupied by the opposing side.
        black (bool): Whether the attacking side is black.

    Returns:
        bool: True if a pseudo-legal attack on any of the squares exists,
            otherwise False.
    """
    switch = bd.black != black

    if black:
        piece_locs = np.where(bd.array > 0)
    else:
        piece_locs = np.where(bd.array < 0)

    if switch:
        bd.switch_side()

    piece_list = bd[piece_locs]
    threat = False

    for piece, loc in np.c_[piece_list, piece_locs]:
        diff = x88_diff(pos, loc)
        p_type = abs(piece)

        if p_type == cs.PAWN:
            valid = diff in np.array([15, 17]) * (-1 + 2 * int(black))

        elif cs.MOVE_TABLE[diff] & (1 << p_type):
            valid = True

            if p_type not in (cs.KING, cs.KNIGHT):
                valid = True
                v = cs.VECTORS[find_vector_from_diff(diff)]
                current += v
                while current != pos:
                    if bd.array[current]:
                        valid = False
                        break
                    current += v

        if valid:
            capture = bd.array[pos] == 0
            if move.pseudo_legal(move.encode_move(loc, pos, capture=capture), bd):
                threat = True
                break

    if switch:
        bd.switch_side()

    return threat


def legal(mv, board):
    """Checks if a pseudo-legal move does not leave the king in check.

    Args:
        mv (int): The move integer.
        board (Board): The board to analyse.

    Returns:
        bool: True if the move is legal, and False otherwise.
    """
    [_, _, _, castling, _] = move.get_info(mv)

    if castling:
        squares = (
            np.array([2, 3, 4]) if castling == cs.KINGSIDE else np.array([4, 5, 6])
        )
        squares += 0x70 * board.black
        for sqr in squares:
            if square_under_threat(board, sqr, not board.black):
                return False
        return True

    try:
        move.make_move(mv, board)
    except ValueError:
        return False

    valid = square_under_threat(board, board.find_king(not board.black), board.black)
    move.unmake_move(mv, board)

    return valid


def gen_pawn_moves(bd, pos):
    """Finds all pseudo-legal pawn moves from a position."""
    moves = []

    step = 16 * (1 - 2 * int(bd.black))
    final_rank = 7 * int(bd.black)
    single = pos + step
    promotion = single >> 4 & final_rank

    if not single & 0x88:
        if not bd.array[single]:
            mv = move.encode_move(pos, single, promotion=promotion)
            if move.pseudo_legal(mv, bd):
                moves.append(mv)

        for d in (single - 1, single + 1):
            if not d & 0x88 and bd.array[d]:
                mv = move.encode_move(pos, d, capture=True, promotion=promotion)
                if move.pseudo_legal(mv, bd):
                    moves.append(mv)

        double = single + step
        if double >> 4 == 7 - final_rank and not bd.array[double]:
            promotion = double >> 4 & final_rank
            mv = move.encode_move(pos, double)
            if move.pseudo_legal(mv, bd):
                moves.append(mv)

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

    def check_and_append(bd, start, dest, moves, castling=0):
        capture = bd.array[dest] != 0
        mv = move.encode_move(start, dest, capture=capture, castling=castling)
        if move.pseudo_legal(mv, bd):
            moves.append(mv)

    moves = []
    piece = bd.array[pos]
    p_type = abs(piece)

    if p_type == cs.KNIGHT:
        for v in (0x19, 0x21, -0x19, -0x21):
            dest = pos + v
            if dest & 0x88:
                continue

            check_and_append(bd, pos, dest, moves)

    elif p_type == cs.KING:
        c_off = int(not bd.black)
        for c, info in cs.C_INFO.items():
            if bd.get_castling_rights(c_off + info[0]):
                check_and_append(bd, pos, pos + info[1], moves, castling=c)
        for v in cs.VALID_VECTORS[p_type]:
            check_and_append(bd, pos, pos + cs.VECTORS[v], moves)

    elif abs(piece) == cs.PAWN:
        return gen_pawn_moves(bd, pos)
    else:
        for v in cs.VALID_VECTORS[abs(piece)]:
            vec = cs.VECTORS[v]
            dest = pos + vec

            while not dest & 0x88:
                check_and_append(bd, pos, dest, moves)
                if bd.array[dest]:
                    break

                dest += vec

    return moves


def all_pseudo_legal_moves(bd):
    """Finds all the pseudo-legal moves that the side to move can make."""
    moves = []

    if bd.black:
        piece_locs = np.where(bd.array > 0)
    else:
        piece_locs = np.where(bd.array < 0)

    for pos in piece_locs:
        moves.extend(all_moves_from_position(bd, pos))

    return moves


def all_legal_moves(bd):
    """Finds all the legal moves that the side to move can make."""
    return [mv for mv in all_pseudo_legal_moves(bd) if legal(mv, bd)]
