"Module providing move making, unmaking and checking utilities."
from chess_engine import constants as cs


def encode_move(start, dest, capture=False, castling=0, promotion=cs.NULL_PIECE):
    """Encodes the state associated with a move to an integer.

    Args:
        start (int): The coordinates of the starting position.
        dest (int): The coordinates of the destination.
        capture (bool, optional): Indicates whether the move is a capture. Defaults
            to False.
        castling (int, optional): Indicates if the move is a castle and if so,
            which type: NONE = 0, KINGSIDE = 2, QUEENSIDE = 3. Defaults to 0.
        promotion (int, optional): The piece type to change the pawn to if the move
            is a promotion. Defaults to 0.

    Returns:
        int: A number encoding the move state.
    """
    mv = (start >> 4) << 13
    mv |= (start & 0x0F) << 10
    mv |= (dest >> 4) << 7
    mv |= (dest & 0x0F) << 4
    info = 0

    if castling:
        mv |= castling

    info |= int(capture) << 2

    if promotion:
        info |= 8  # valid bit
        info |= cs.PROM_FROM_PIECE[promotion]  # promotion type

    return mv | info


def get_info(mv):
    """Extracts the move state from the move integer.

    Args:
        mv (int): The move integer.

    Returns:
        list: A list of values associated with the move:
            [start, dest, capture, castling, promotion]
    """
    flags = mv & 0xF
    info = [0, 0, 0, 0, 0]

    info[0] = ((mv & 0xE000) >> 9) + ((mv & 0x1C00) >> 10)  # start
    info[1] = ((mv & 0x0380) >> 3) + ((mv & 0x0070) >> 4)  # dest
    info[2] = bool(flags & 4)  # capture
    info[3] = flags if flags in (2, 3) else 0  # castling
    info[4] = cs.PIECE_FROM_PROM[flags & 3] if flags & 8 else 0  # promotion

    return info


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
    return (r_start, r_start - 2 + 5 * (castling - 2))


def pseudo_legal(mv, bd):
    """Checks if a move with valid start/destination indices
        and no obstructions is pseudo-legal.

    Args:
        bd (Board): The board to analyse.

    Returns:
        bool: True if the move is pseudo-legal, and False otherwise.
    """
    [start, dest, capture, castling, promotion] = get_info(mv)

    piece = bd.array[start]
    final_rank = (dest >> 4) == 7 * (bd.black ^ 1)

    if piece * (1 - 2 * bd.black) <= 0 or (promotion and not final_rank):
        return False

    if castling:
        if not bd.get_castling_rights(2 * (bd.black ^ 1) + cs.C_INFO[castling][0]):
            return False

        rank = 0x70 * bd.black
        indices = (1, 4) if castling == cs.QUEENSIDE else (5, 7)
        c_squares = bd.array[rank + indices[0] : rank + indices[1]]

        return not any(c_squares)

    if capture:
        if is_en_passant(bd, start, dest):
            to_capture = bd.array[bd.ep_square]
        else:
            to_capture = bd.array[dest]

        return to_capture * piece < 0

    return not bd.array[dest]


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
        mv (int): The move integer.
        bd (Board): The board to update.

    Raises:
        ValueError: If the move is not pseudo-legal.
    """
    [start, dest, capture, castling, promotion] = get_info(mv)
    pawn_move = abs(bd.array[start]) == cs.PAWN
    cap_type = 0
    is_ep = 0

    if capture:
        if is_en_passant(bd, start, dest):
            is_ep = 1
            cap_type = cs.PAWN
            remove_piece(bd, bd.ep_square)
        else:
            cap_type = int(abs(bd.array[dest]))
            remove_piece(bd, dest)

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

    if pawn_move or capture:
        bd.halfmove_clock = 0
    else:
        bd.halfmove_clock += 1

    bd.fullmove_num += bd.black
    bd.switch_side()


def unmake_move(mv, bd):
    """Reverses a move and any changes to the board state.

    Args:
        mv (int): The move integer.
        bd (Board): The board to update.
    """
    bd.switch_side()
    bd.fullmove_num -= bd.black

    [start, dest, capture, castling, promotion] = get_info(mv)
    mul = 1 - 2 * bd.black

    if castling:
        r_move = get_rook_castle(bd, castling)
        move_piece(bd, r_move[1], r_move[0])

    if promotion:
        remove_piece(bd, dest)
        add_piece(bd, cs.PAWN * mul, start)
    else:
        move_piece(bd, start=dest, dest=start)

    prev_info = bd.get_prev_state()

    if capture:
        cap_piece = prev_info[1] * -mul
        cap_pos = dest - (cs.VECTORS["N"] * mul * prev_info[0])
        add_piece(bd, cap_piece, cap_pos)

    bd.castling_rights = prev_info[2]
    bd.halfmove_clock = prev_info[4]
    bd.ep_square = (0x40 - (0x10 * bd.black) + (prev_info[3] & 7)) * (prev_info[3] >> 3)
