"Module providing move making, unmaking and checking utilities."

from chess_engine import constants as cs, utils


def to_string(start, dest, promotion=0):
    """Converts a move to a move string in LAN.

    Args:
        start (int): The position of the piece to move.
        dest (int): The destination square of the move.
        promotion (int, optional): The piece type to promote
            a pawn to, if applicable. Defaults to 0.

    Returns:
        string: A LAN string with this format:
            source|target|promotion
    """
    return (
        utils.coord_to_string(start)
        + utils.coord_to_string(dest)
        + cs.SYM_FROM_PIECE[abs(promotion)]
    )


def get_info(mv):
    """Extracts the move state from a move string.

    Args:
        mv (string): The move string.

    Returns:
        list: A list of values associated with the move:
            [start, dest, promotion]
    """
    info = [0 for _ in range(3)]

    info[0] = utils.string_to_coord(mv[0:2])
    info[1] = utils.string_to_coord(mv[2:4])

    if len(mv) == 5:
        info[2] = cs.PIECE_FROM_SYM[mv[-1]]

    return info


def castle_type(bd, start, dest):
    """Returns the castling type of a move."""
    if (
        start == 0x70 * bd.black + 4
        and abs(dest - start) == 2
        and abs(bd.array[start]) == cs.KING
    ):
        return cs.KINGSIDE if dest - start == 2 else cs.QUEENSIDE
    return 0


def is_en_passant(bd, start, dest):
    """Determines whether a move is an en passant capture."""
    piece = bd.array[start]

    return (
        abs(piece) == cs.PAWN
        and bd.ep_square
        and abs(bd.ep_square - start) == 1
        and abs(bd.ep_square - dest) == 16
    )


def get_rook_castle(bd, castling):
    """Returns the start and dest indices for a rook castle move."""
    r_start = 0x70 * bd.black + 0x7 * (3 - castling)
    return (r_start, r_start + 5 * castling - 12)


def move_piece(bd, start, dest):
    """Moves a piece to a square on the board."""
    piece = bd.array[start]
    bd.array[start] = 0
    bd.array[dest] = piece
    bd.piece_list[piece].remove(start)
    bd.piece_list[piece].add(dest)


def add_piece(bd, piece, pos):
    """Adds a piece to the board."""
    bd.array[pos] = piece
    bd.piece_list[piece].add(pos)


def remove_piece(bd, pos):
    """Removes a piece from the board."""
    piece = bd.array[pos]
    bd.array[pos] = 0
    bd.piece_list[piece].remove(pos)


def promote_piece(bd, start, dest, promotion):
    """Promotes a pawn."""
    mul = 1 - 2 * bd.black
    bd.array[start] = 0
    bd.array[dest] = promotion * mul
    bd.piece_list[cs.PAWN * mul].remove(start)
    bd.piece_list[promotion * mul].add(dest)


def make_move(mv, bd):
    """Carries out a pseudo-legal move and updates the board state.

    Args:
        mv (string): The move string.
        bd (Board): The board to update.
    """
    [start, dest, promotion] = get_info(mv)
    castling = castle_type(bd, start, dest)
    pawn_move = abs(bd.array[start]) == cs.PAWN
    cap_type = 0
    is_ep = 0

    if bd.array[dest]:
        cap_type = int(abs(bd.array[dest]))
        remove_piece(bd, dest)
    elif is_en_passant(bd, start, dest):
        is_ep = 1
        cap_type = cs.PAWN
        remove_piece(bd, bd.ep_square)

    if castling:
        r_move = get_rook_castle(bd, castling)
        move_piece(bd, r_move[0], r_move[1])

    bd.save_state(is_ep, cap_type)

    if promotion:
        promote_piece(bd, start, dest, promotion)
    else:
        move_piece(bd, start, dest)

    # update castling rights
    if not bd.array[0x04 + 0x70 * bd.black]:
        c_off = 2 * int(bd.black ^ 1)
        bd.remove_castling_rights(c_off)
        bd.remove_castling_rights(c_off + 1)

    for i, sqr in enumerate((0x77, 0x70, 0x07, 0x00)):
        at_sqr = bd.array[sqr]
        if abs(at_sqr) != cs.ROOK or at_sqr * (sqr - 0x10) > 0:
            bd.remove_castling_rights(i)

    # reset en passant square and mark new one if necessary
    bd.ep_square = 0
    if pawn_move and abs(dest - start) == 0x20:
        bd.ep_square = dest

    if pawn_move or cap_type:
        bd.halfmove_clock = 0
    else:
        bd.halfmove_clock += 1

    bd.fullmove_num += bd.black
    bd.switch_side()


def unmake_move(mv, bd):
    """Reverses a move and any changes to the board state.

    Args:
        mv (string): The move string.
        bd (Board): The board to update.
    """
    bd.switch_side()
    bd.fullmove_num -= bd.black

    [start, dest, promotion] = get_info(mv)
    mul = 1 - 2 * bd.black
    diff = dest - start

    if (
        abs(bd.array[dest]) == cs.KING
        and start == 0x70 * bd.black + 4
        and abs(diff) == 2
    ):
        r_move = get_rook_castle(bd, cs.KINGSIDE if diff == 2 else cs.QUEENSIDE)
        move_piece(bd, r_move[1], r_move[0])

    if promotion:
        remove_piece(bd, dest)
        add_piece(bd, cs.PAWN * mul, start)
    else:
        move_piece(bd, start=dest, dest=start)

    prev_info = bd.get_prev_state()
    cap_type = prev_info[1]

    if cap_type:
        cap_pos = dest - (cs.VECTORS["N"] * mul * prev_info[0])
        add_piece(bd, cap_type * -mul, cap_pos)

    bd.castling_rights = prev_info[2]
    bd.halfmove_clock = prev_info[4]
    bd.ep_square = (0x40 - (0x10 * bd.black) + (prev_info[3] & 7)) * (prev_info[3] >> 3)
