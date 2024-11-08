"Module providing move making, unmaking and checking utilities."

from chess_engine import constants as cs, utils


def encode(start, dest, castling, promotion):
    """Encodes move information into an integer."""
    return start | (dest << 8) | (promotion << 16) | (castling << 20)


def decode(mv):
    """Extracts move information from an integer."""
    return (mv & 0xFF, (mv >> 8) & 0xFF, (mv >> 16) & 0xF, (mv >> 20) & 3)


def string_to_int(bd, mstr, unmake=False):
    """Converts a move string to an integer."""
    try:
        start = utils.string_to_coord(mstr[0:2])
        dest = utils.string_to_coord(mstr[2:4])
        promotion = 0

        if len(mstr) == 5:
            promotion = cs.LETTERS.index(mstr[-1])

        castling = 0

        if unmake:
            castle_start = 0x70 * (bd.black ^ 1) + 4
            king_pos = dest
        else:
            castle_start = 0x70 * bd.black + 4
            king_pos = start

        if start == castle_start and utils.is_type(bd.array[king_pos], cs.K):
            diff = dest - start
            if abs(diff) == 2:
                castling = cs.KINGSIDE if diff == 2 else cs.QUEENSIDE

        return encode(start, dest, castling, promotion)

    except (IndexError, ValueError):
        return -1


def int_to_string(mv):
    """Converts a move integer to a string."""
    start, dest, promotion, _ = decode(mv)
    return (
        utils.coord_to_string(start)
        + utils.coord_to_string(dest)
        + cs.LETTERS[promotion].lower()
    ).strip()


def get_rook_castle(bd, castling):
    """Returns the start and dest indices for a rook castle move."""
    r_start = 0x70 * bd.black + 0x7 * (3 - castling)
    return (r_start, r_start + 5 * castling - 12)


def remove_rook_rights(bd, pos, black):
    """Removes castling rights for rook, if applicable."""
    for castle in (cs.KINGSIDE, cs.QUEENSIDE):
        if pos == 0x70 * black + 7 * (3 - castle) and utils.is_piece(
            bd.array[pos], cs.R, black
        ):
            bd.remove_castling_rights(black, castle)


def move_piece(bd, start, dest, promotion=0):
    """Moves a piece to a square on the board."""
    piece = bd.array[start]
    bd.array[start] = 0
    bd.piece_list[piece].remove(start)

    if promotion:
        piece = utils.change_colour(promotion, bd.black)

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


def make_move(mv, bd):
    """Carries out a pseudo-legal move and updates the board state."""
    start, dest, promotion, castling = decode(mv)
    pawn = utils.is_type(bd.array[start], cs.P)
    cap_type = utils.get_piece_type(bd.array[dest])
    clock = bd.halfmove_clock + 1

    if cap_type:
        bd.save_state(cap_type)
        remove_rook_rights(bd, dest, bd.black ^ 1)
        remove_piece(bd, dest)
        clock = 0
    elif pawn and dest == bd.ep_square:
        bd.save_state(cs.P)
        remove_piece(bd, bd.ep_square - (cs.FW * (1 - 2 * bd.black)))
        clock = 0
    else:
        bd.save_state(0)

    # update castling rights
    if utils.is_type(bd.array[start], cs.K):
        bd.remove_castling_rights(bd.black, cs.KINGSIDE)
        bd.remove_castling_rights(bd.black, cs.QUEENSIDE)

    remove_rook_rights(bd, start, bd.black)

    if castling:
        r_move = get_rook_castle(bd, castling)
        move_piece(bd, r_move[0], r_move[1])

    move_piece(bd, start, dest, promotion)

    # reset en passant square and mark new one if necessary
    bd.ep_square = 0x88

    if pawn and abs(dest - start) == 2 * cs.FW:
        bd.ep_square = dest - (cs.FW * (1 - 2 * bd.black))
        clock = 0

    bd.halfmove_clock = clock
    bd.fullmove_num += bd.black
    bd.switch_side()


def unmake_move(mv, bd):
    """Reverses a move and any changes to the board state."""
    start, dest, promotion, castling = decode(mv)
    bd.switch_side()
    bd.fullmove_num -= bd.black

    if castling:
        r_move = get_rook_castle(bd, castling)
        move_piece(bd, r_move[1], r_move[0])

    if promotion:
        remove_piece(bd, dest)
        add_piece(bd, utils.get_piece(cs.P, bd.black), start)
    else:
        move_piece(bd, start=dest, dest=start)

    prev_info = bd.get_prev_state()

    bd.halfmove_clock = prev_info[0]
    bd.ep_square = prev_info[1]
    bd.castling_rights = prev_info[2]

    cap_type = prev_info[3]

    if cap_type:
        cap_pos = dest + (
            cs.BW * (1 - 2 * bd.black) * int(dest > 0 and dest == bd.ep_square)
        )
        add_piece(bd, utils.get_piece(cap_type, (bd.black ^ 1)), cap_pos)


def make_move_from_string(mstr, bd):
    """Converts a move string to an integer and calls the make function."""
    mv = string_to_int(bd, mstr)
    if mv != -1:
        make_move(mv, bd)


def unmake_move_from_string(mstr, bd):
    """Parses a move string and calls the unmake function."""
    mv = string_to_int(bd, mstr, unmake=True)
    if mv != -1:
        unmake_move(mv, bd)
