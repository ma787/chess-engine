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
            castle_start = cs.A1 + (0x70 * (bd.black ^ 1)) + 4
            king_pos = dest
        else:
            castle_start = cs.A1 + (0x70 * bd.black) + 4
            king_pos = start

        if start == castle_start and bd.array[king_pos] & 7 == cs.K:
            diff = dest - start
            if abs(diff) == 2:
                castling = cs.KINGSIDE if diff == 2 else cs.QUEENSIDE

        return encode(start, dest, castling)

    except (IndexError, ValueError):
        return -1


def int_to_string(bd, mv):
    """Converts a move integer to a move string."""
    start, dest, _ = decode(mv)
    promotion = ""

    if bd.array[start] & 7 == cs.PAWNS[bd.black] and ((dest & 0xF0) >> 4) - 4 == 7 * (
        1 - bd.black
    ):
        promotion = "q"

    return (
        utils.coord_to_string(start) + utils.coord_to_string(dest) + promotion
    ).strip()


def is_square_attacked(bd, pos, black):
    """Checks if a square is attacked by a side."""
    vecs = set(cs.VALID_VECS[cs.Q])

    for v in cs.VALID_VECS[cs.N] + cs.VALID_VECS[cs.Q]:
        loc = pos + v
        square = bd.array[loc]

        if square != cs.GD and square:
            if (square >> 3) & 1 == black and cs.MOVE_TABLE[
                utils.square_diff(loc, pos)
            ] & cs.CONTACT_MASKS[square & 7]:
                return True
            if v in vecs:
                vecs.remove(v)

    for v in vecs:
        current = pos + v
        while True:
            current += v
            square = bd.array[current]

            if square:
                if (
                    square != cs.GD
                    and (square >> 3) & 1 == black
                    and cs.MOVE_TABLE[utils.square_diff(current, pos)]
                    & cs.DISTANT_MASKS[square & 7]
                ):
                    return True
                break

    return False


def update_check(bd, start, dest):
    """Updates the check status of the board after a move is made."""
    bd.check = 0
    p_type = bd.array[dest] & 7

    king_pos = bd.piece_list[cs.SIDE_OFFSET * bd.black + 4]
    dest_diff = utils.square_diff(dest, king_pos)
    direct = cs.MOVE_TABLE[dest_diff] & cs.CONTACT_MASKS[p_type]
    direct_vec = cs.UNIT_VEC[dest_diff]

    if not direct and cs.MOVE_TABLE[dest_diff] & cs.DISTANT_MASKS[p_type]:
        current = dest + direct_vec
        direct = 2

        while current != king_pos:
            if bd.array[current]:
                direct = 0
                break
            current += direct_vec

    # search for a discovered check
    start_diff = utils.square_diff(start, king_pos)
    discovered_vec = -cs.UNIT_VEC[start_diff]

    if (
        cs.MOVE_TABLE[start_diff] & (cs.DISTANT_MASKS[cs.Q] | cs.CONTACT_MASKS[cs.Q])
        and discovered_vec != -direct_vec
    ):
        current = king_pos

        while True:
            current += discovered_vec
            square = bd.array[current]

            if square:
                if (
                    square != cs.GD
                    and (square >> 3) & 1 != bd.black
                    and cs.MOVE_TABLE[utils.square_diff(current, king_pos)]
                    & cs.DISTANT_MASKS[square & 7]
                ):
                    bd.check = 2 + int(direct > 0)
                    bd.checker = current
                    return
                break

    bd.check = direct
    bd.checker = dest


def legal_king_move(bd, dest, castling):
    """Checks whether a king move is legal."""
    if castling:
        squares = [
            cs.A1 + (0x70 * (bd.black ^ 1)) + 2 * int(castling == cs.KINGSIDE) + x
            for x in range(2, 5)
        ]

        for sqr in squares:
            if is_square_attacked(bd, sqr, bd.black):
                return False

        return True

    return not is_square_attacked(bd, dest, bd.black)


def ep_pinned(bd, start, king_pos, ep_sqr):
    """Checks if an en passant capture would leave the king in check."""
    v = cs.UNIT_VEC[utils.square_diff(king_pos, start)]
    current = king_pos

    while True:
        current += v
        if current in (start, ep_sqr):
            continue

        square = bd.array[current]
        if square == cs.GD:
            return False

        if square:
            if (square >> 3) & 1 != bd.black and cs.MOVE_TABLE[
                utils.square_diff(current, king_pos)
            ] & cs.DISTANT_MASKS[square & 7]:
                return True
            return False


def unmake_move(mv, bd):
    """Reverses a move and any changes to the board state."""
    start, dest, castling = decode(mv)
    bd.switch_side()
    bd.fullmove_num -= bd.black

    if castling:
        r_start = cs.A1 + (0x70 * bd.black) + 0x7 * (3 - castling)
        r_dest = r_start + 5 * castling - 12
        rook = bd.array[r_dest]
        bd.array[r_dest] = 0
        bd.array[r_start] = rook
        bd.piece_list[rook >> 4] = r_start

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

    if promotion:  # change to pawn of same colour
        pawn = (cs.WP, cs.BP)[bd.black]
        bd.array[start] = (piece & 0x1F0) | (bd.black << 3) | pawn

    if captured:
        cap_pos = dest
        if dest == bd.ep_square:
            cap_pos += cs.BW * (1 - 2 * bd.black)
        bd.array[cap_pos] = captured
        bd.piece_list[captured >> 4] = cap_pos


def make_castle_move(mv, bd, dest, castling):
    """Completes a castle move."""
    r_start = cs.A1 + (0x70 * bd.black) + 0x7 * (3 - castling)
    r_dest = r_start + 5 * castling - 12

    rook = bd.array[r_start]
    bd.array[r_start] = 0
    bd.array[r_dest] = rook
    bd.piece_list[rook >> 4] = r_dest

    bd.castling_rights[2 * bd.black] = False
    bd.castling_rights[2 * bd.black + 1] = False

    bd.ep_square = -1
    bd.fullmove_num += bd.black
    bd.switch_side()

    if not legal_king_move(bd, dest, castling):
        unmake_move(mv, bd)
        return -1

    update_check(bd, r_start, r_dest)
    return 0


def make_pawn_move(bd, start, dest, piece, pr_type):
    "Completes a pawn move."
    promotion = dest >> 4 == 7 * (1 - bd.black) + 4
    victim_pawn_pos = dest + cs.BW * (1 - 2 * bd.black)
    cap_pos = dest
    captured = bd.array[cap_pos]
    override_check = 0

    # en passant capture
    if dest == bd.ep_square and not captured:
        king_off = cs.SIDE_OFFSET * bd.black
        king_pos = bd.piece_list[king_off + 4]

        if king_pos >> 4 == start >> 4 and ep_pinned(
            bd, start, king_pos, victim_pawn_pos
        ):
            return -1

        enemy_king_pos = bd.piece_list[16 - king_off + 4]
        ep_diff = utils.square_diff(enemy_king_pos, victim_pawn_pos)
        step = cs.UNIT_VEC[ep_diff]
        current = enemy_king_pos
        passed = False
        possible_pin = (
            step != cs.UNIT_VEC[utils.square_diff(enemy_king_pos, bd.ep_square)]
        )

        while possible_pin:
            current += step
            if current == victim_pawn_pos:
                passed = True
                continue

            square = bd.array[current]
            if square == cs.GD:
                break

            if square:
                if not passed:
                    break
                if (square >> 3) & 1 == bd.black and cs.MOVE_TABLE[
                    utils.square_diff(current, enemy_king_pos)
                ] & cs.DISTANT_MASKS[square & 7]:
                    override_check = current
                break

        cap_pos = victim_pawn_pos
        captured = bd.array[cap_pos]

    bd.save_state(captured, promotion)

    if captured:
        bd.piece_list[captured >> 4] = -1
        bd.array[cap_pos] = 0

    bd.array[start] = 0
    bd.array[dest] = piece
    bd.piece_list[piece >> 4] = dest

    bd.ep_square = -1
    bd.halfmove_clock = 0

    if dest - start in (2 * cs.FW, 2 * cs.BW):
        # ep square is one step back from the destination of a double pawn push
        bd.ep_square = victim_pawn_pos
    elif promotion:  # change to promoted type
        bd.array[dest] = (piece & 0x1F0) | (bd.black << 3) | pr_type

        if captured:
            off = 2 * (bd.black ^ 1)
            file = (dest & 0x0F) - 4
            bd.castling_rights[off] &= file != 7
            bd.castling_rights[off + 1] &= file != 0

    bd.fullmove_num += bd.black
    bd.switch_side()

    update_check(bd, start, dest)
    if override_check:
        bd.check |= 2
        bd.checker = override_check

    return 0


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

    if piece & 7 in (cs.P, cs.p):
        return make_pawn_move(bd, start, dest, piece, pr_type)

    captured = bd.array[dest]
    bd.save_state(captured, False)
    bd.halfmove_clock += 1

    if captured:
        bd.piece_list[captured >> 4] = -1
        bd.halfmove_clock = 0

    bd.array[start] = 0
    bd.array[dest] = piece
    bd.piece_list[piece >> 4] = dest

    if castling:
        return make_castle_move(mv, bd, dest, castling)

    # update castling rights
    first_rank = cs.A1 + 0x70 * bd.black
    last_rank = cs.A8 - 0x70 * bd.black
    off = 2 * bd.black
    bd.castling_rights[off] &= start != first_rank + 7
    bd.castling_rights[off + 1] &= start != first_rank
    bd.castling_rights[(2 - off)] &= dest != last_rank + 7
    bd.castling_rights[(2 - off) + 1] &= dest != last_rank

    bd.ep_square = -1  # reset en passant square
    bd.fullmove_num += bd.black
    bd.switch_side()

    if piece & 7 == cs.K:
        bd.castling_rights[off] = False
        bd.castling_rights[off + 1] = False

        if not legal_king_move(bd, dest, castling):
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

        return make_move(mv, bd, pr_type=promotion)

    return -1


def unmake_move_from_string(mstr, bd):
    """Parses a move string and calls the unmake function."""
    mv = string_to_int(bd, mstr, unmake=True)
    if mv != -1:
        unmake_move(mv, bd)
