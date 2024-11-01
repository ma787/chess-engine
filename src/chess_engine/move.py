"Module providing move making, unmaking and checking utilities."

from chess_engine import constants as cs, utils


def to_string(start, dest, promotion=0):
    """Converts the move's source and target to a move string.

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
        tuple: Contains values associated with the move:
            start, dest, promotion
    """
    promotion = 0

    start = utils.string_to_coord(mv[0:2])
    dest = utils.string_to_coord(mv[2:4])

    if len(mv) == 5:
        promotion = cs.PIECE_FROM_SYM[mv[-1]]

    return start, dest, promotion


def castle_type(bd, start, dest):
    """Returns the castling type of a move."""
    if (
        start == 0x70 * bd.black + 4
        and abs(dest - start) == 2
        and abs(bd.array[start]) == cs.KING
    ):
        return cs.KINGSIDE if dest - start == 2 else cs.QUEENSIDE
    return 0


def get_rook_castle(bd, castling):
    """Returns the start and dest indices for a rook castle move."""
    r_start = 0x70 * bd.black + 0x7 * (3 - castling)
    return (r_start, r_start + 5 * castling - 12)


def move_piece(bd, start, dest, promotion=0):
    """Moves a piece to a square on the board."""
    piece = bd.array[start]
    bd.array[start] = 0
    bd.piece_list[piece].remove(start)

    if promotion:
        piece = promotion * bd.mul

    bd.array[dest] = piece
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


def make_move_from_info(bd, start, dest, promotion):
    """Carries out a pseudo-legal move and updates the board state."""
    castling = castle_type(bd, start, dest)
    pawn = abs(bd.array[start]) == cs.PAWN
    cap_type = abs(bd.array[dest])
    clock = bd.halfmove_clock + 1

    if cap_type:
        remove_piece(bd, dest)
        clock = 0
    elif pawn and dest == bd.ep_square:
        cap_type = cs.PAWN
        remove_piece(bd, bd.ep_square - (cs.N * bd.mul))
        clock = 0

    bd.save_state(cap_type)

    if castling:
        r_move = get_rook_castle(bd, castling)
        move_piece(bd, r_move[0], r_move[1])

    move_piece(bd, start, dest, promotion)

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

    if pawn and abs(dest - start) == 2 * cs.N:
        bd.ep_square = dest - (cs.N * bd.mul)
        clock = 0

    bd.halfmove_clock = clock
    bd.fullmove_num += bd.black
    bd.switch_side()


def unmake_move_from_info(bd, start, dest, promotion):
    """Reverses a move and any changes to the board state."""
    bd.switch_side()
    bd.fullmove_num -= bd.black
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
        add_piece(bd, cs.PAWN * bd.mul, start)
    else:
        move_piece(bd, start=dest, dest=start)

    prev_info = bd.get_prev_state()

    bd.halfmove_clock = prev_info[0]
    bd.ep_square = prev_info[1]
    bd.castling_rights = prev_info[2]

    cap_type = prev_info[3]

    if cap_type:
        cap_pos = dest + (cs.S * bd.mul * int(dest == bd.ep_square))
        add_piece(bd, cap_type * -bd.mul, cap_pos)


def make_move(mv, bd):
    """Parses a move string and calls the move-making function.

    Args:
        mv (string): The move string.
        bd (Board): The board to update.
    """
    start, dest, promotion = get_info(mv)
    make_move_from_info(bd, start, dest, promotion)


def unmake_move(mv, bd):
    """Parses a move string and calls the unmake function.

    Args:
        mv (string): The move string.
        bd (Board): The board to update.
    """
    start, dest, promotion = get_info(mv)
    unmake_move_from_info(bd, start, dest, promotion)
