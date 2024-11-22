"Module providing move making, unmaking and checking utilities."

from chess_engine import constants as cs, utils


def encode(start, dest, castling=0):
    """Encodes move information into an integer."""
    return start | (dest << 8) | (castling << 16)


def decode(mv):
    """Extracts move information from an integer."""
    return (mv & 0xFF, (mv >> 8) & 0xFF, (mv >> 16) & 0xF)


def string_to_int(bd, mstr, unmake=False):
    """Converts a move string to an integer."""
    try:
        start = utils.string_to_coord(mstr[0:2])
        dest = utils.string_to_coord(mstr[2:4])

        castling = 0

        if unmake:
            castle_start = 0x70 * (bd.black ^ 1) + 4
            king_pos = dest
        else:
            castle_start = 0x70 * bd.black + 4
            king_pos = start

        if start == castle_start and bd.array[king_pos] & 7 == cs.K:
            diff = dest - start
            if abs(diff) == 2:
                castling = cs.KINGSIDE if diff == 2 else cs.QUEENSIDE

        return encode(start, dest, castling)

    except (IndexError, ValueError):
        return -1


def add_piece(bd, piece, pos):
    """Adds a piece to the board."""
    bd.array[pos] = piece
    bd.piece_list[piece].add(pos)


def remove_piece(bd, pos):
    """Removes a piece from the board."""
    piece = bd.array[pos]
    bd.array[pos] = 0
    bd.piece_list[piece].remove(pos)


def is_square_attacked(bd, pos, black):
    """Checks if a square is attacked by a side."""
    vecs = set(cs.VALID_VECS[cs.Q])

    for v in cs.VALID_VECS[cs.N] + cs.VALID_VECS[cs.Q]:
        loc = pos + v
        if not loc & 0x88:
            square = bd.array[loc]
            if square:
                if (square >> 3) & 1 == black and cs.MOVE_TABLE[
                    utils.square_diff(loc, pos)
                ] & cs.CONTACT_MASKS[square & 7]:
                    return True
                if v in vecs:
                    vecs.remove(v)

    for v in vecs:
        current = pos + 2 * v
        while not current & 0x88:
            square = bd.array[current]
            if square:
                if (square >> 3) & 1 == black and cs.MOVE_TABLE[
                    utils.square_diff(current, pos)
                ] & cs.DISTANT_MASKS[square & 7]:
                    return True
                break

            current += v

    return False


def update_check(bd, start, dest):
    """Updates the check status of the board after a move is made."""
    bd.check = 0

    p_type = bd.array[dest] & 7

    king_pos = bd.piece_list[cs.SIDE_OFFSET * bd.black + 4]
    dest_diff = utils.square_diff(dest, king_pos)
    direct = cs.MOVE_TABLE[dest_diff] & cs.CONTACT_MASKS[p_type]

    if not direct and cs.MOVE_TABLE[dest_diff] & cs.DISTANT_MASKS[p_type]:
        v = cs.UNIT_VEC[dest_diff]
        current = dest + v
        direct = 2

        while current != king_pos:
            if bd.array[current]:
                direct = 0
                break
            current += v

    # search for a discovered check
    start_diff = utils.square_diff(start, king_pos)

    if cs.MOVE_TABLE[start_diff] & cs.DISTANT_MASKS[cs.Q]:
        v = -cs.UNIT_VEC[start_diff]
        current = king_pos + v

        while not current & 0x88:
            square = bd.array[current]
            if square:
                if (square >> 3) & 1 != bd.black and cs.MOVE_TABLE[
                    utils.square_diff(current, king_pos)
                ] & cs.DISTANT_MASKS[square & 7]:
                    bd.check = 2 + int(direct > 0)
                    bd.checker = current
                    return
                break
            current += v

    bd.check = direct
    bd.checker = dest


def legal_king_move(bd, dest, castling):
    """Checks whether a king move is legal."""
    if castling:
        squares = [
            x + 2 * int(castling == cs.KINGSIDE) + 0x70 * (bd.black ^ 1)
            for x in range(2, 5)
        ]

        for sqr in squares:
            if is_square_attacked(bd, sqr, bd.black):
                return False

        return True

    return not is_square_attacked(bd, dest, bd.black)


def ep_pinned(bd, start):
    """Checks if an en passant capture would leave the king in check."""
    king_pos = bd.piece_list[cs.SIDE_OFFSET * bd.black + 4]

    if king_pos >> 4 != start >> 4:
        return False

    v = cs.UNIT_VEC[utils.square_diff(king_pos, start)]
    current = king_pos + v
    piece_count = 0

    while current != start:
        square = bd.array[current]
        if square:
            if (square >> 3) & 1 == bd.black or square & 7 != cs.P:
                return False
            piece_count += 1
        current += v

    if piece_count > 1:
        return False

    current = start + v
    while not current & 0x88:
        square = bd.array[current]
        if square:
            if (square >> 3) & 1 != bd.black and cs.MOVE_TABLE[
                utils.square_diff(current, king_pos)
            ] & cs.DISTANT_MASKS[square & 7]:
                return True
            return False
        current += v

    return False


def unmake_move(mv, bd):
    """Reverses a move and any changes to the board state."""
    start, dest, castling = decode(mv)
    bd.switch_side()
    bd.fullmove_num -= bd.black

    if castling:
        r_dest = 0x70 * bd.black + 0x7 * (3 - castling)
        r_start = r_dest + 5 * castling - 12
        rook = bd.array[r_start]
        bd.array[r_start] = 0
        bd.array[r_dest] = rook
        bd.piece_list[rook >> 4] = r_dest

    piece = bd.array[dest]
    bd.array[dest] = 0
    bd.array[start] = piece
    bd.piece_list[piece >> 4] = start

    (
        bd.halfmove_clock,
        bd.ep_square,
        bd.castling_rights,
        bd.check,
        bd.checker,
        captured,
        promotion,
    ) = bd.get_prev_state()

    if promotion:
        pawn = cs.p | 8 if bd.black else cs.P
        bd.array[start] = pawn | (piece & 0x1F0)  # change to pawn of same colour

    if captured:
        cap_pos = dest
        if dest == bd.ep_square:
            cap_pos += cs.BW * (1 - 2 * bd.black)
        bd.array[cap_pos] = captured
        bd.piece_list[captured >> 4] = cap_pos


def make_move(mv, bd, pr_type=cs.Q):
    """Carries out a move and updates the board state.

    Args:
        mv (int): An integer encoding the move information.
        bd (Board): The board to update.

    Returns:
        int: 0, if the move is legal and the board is updated,
            or -1, if the move is illegal (causing the move to be
            reversed).
    """
    start, dest, castling = decode(mv)
    piece = bd.array[start]
    pawn_move = piece & 7 in (cs.P, cs.p)
    captured = bd.array[dest]
    clock = bd.halfmove_clock + 1
    promotion = False

    if captured:
        clock = 0
        bd.piece_list[captured >> 4] = -1

    if pawn_move:
        promotion = dest >> 4 == 7 * (1 - bd.black)
        if dest == bd.ep_square and not bd.array[dest]:
            if ep_pinned(bd, start):
                return -1

            cap_pos = dest + cs.BW * (1 - 2 * bd.black)
            captured = bd.array[cap_pos]
            bd.piece_list[captured >> 4] = -1
            bd.array[cap_pos] = 0
            clock = 0

    bd.save_state(captured, promotion)
    bd.halfmove_clock = clock

    bd.array[start] = 0
    bd.array[dest] = piece
    bd.piece_list[piece >> 4] = dest

    if castling:
        r_start = 0x70 * bd.black + 0x7 * (3 - castling)
        r_dest = r_start + 5 * castling - 12
        rook = bd.array[r_start]
        bd.array[r_start] = 0
        bd.array[r_dest] = rook
        bd.piece_list[rook >> 4] = r_dest

    # update castling rights
    for side in (cs.WHITE, cs.BLACK):
        rank = 0x70 * side
        off = 2 * side
        king = cs.K | (side << 3)

        if bd.array[rank + 4] & 15 != king:
            bd.castling_rights[off] = False
            bd.castling_rights[off + 1] = False
            continue

        rook = cs.R | (side << 3)

        if bd.array[rank] & 15 != rook:
            bd.castling_rights[off + cs.QUEENSIDE - 2] = False

        if bd.array[rank + 7] & 15 != rook:
            bd.castling_rights[off + cs.KINGSIDE - 2] = False

    bd.ep_square = -1  # reset en passant square

    if pawn_move:
        bd.halfmove_clock = 0
        if dest - start in (2 * cs.FW, 2 * cs.BW):
            bd.ep_square = dest - (cs.FW * (1 - 2 * bd.black))
        elif promotion:
            bd.array[dest] = (piece & 0x1F8) | pr_type  # change to promoted type

    bd.fullmove_num += bd.black
    bd.switch_side()

    if piece & 7 == cs.K and not legal_king_move(bd, dest, castling):
        unmake_move(mv, bd)
        return -1

    update_check(bd, start, dest)

    return 0


def make_move_from_string(mstr, bd):
    """Converts a move string to an integer and calls the make function."""
    mv = string_to_int(bd, mstr)

    if mv != -1:
        promotion = cs.Q
        if len(mstr) == 5:
            promotion = cs.LETTERS.index(mstr[-1]) & ~(1 << 3)

        make_move(mv, bd, pr_type=promotion)


def unmake_move_from_string(mstr, bd):
    """Parses a move string and calls the unmake function."""
    mv = string_to_int(bd, mstr, unmake=True)
    if mv != -1:
        unmake_move(mv, bd)
