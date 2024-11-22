"""Module providing move generation functions."""

from chess_engine import constants as cs, move, utils


def can_block(dest, king_pos, checker_pos, v):
    """Determines whether a move to a square can block an checking slider."""
    if cs.UNIT_VEC[utils.square_diff(king_pos, dest)] == v:
        pos = king_pos + v
        while pos != checker_pos:
            if pos == dest:
                return True
            pos += v

    return False


def gen_blocking_move(bd, p_type, pos, king_pos, v, moves):
    """Appends any move which block a checking slider to a list."""
    valid_vecs = cs.VALID_VECS[p_type]

    if p_type in (cs.P, cs.p):
        fw = valid_vecs[0]
        current = pos + fw

        if not bd.array[current]:
            if can_block(current, king_pos, bd.checker, v):
                moves.append(move.encode(pos, current))

        if pos >> 4 == 1 + 5 * bd.black:
            if not bd.array[current + fw] and can_block(
                current + fw, king_pos, bd.checker, v
            ):
                moves.append(move.encode(pos, current + fw))

        # ep captures to block check are only possible in unreachable positions
        for vec in valid_vecs[1:]:
            if pos + vec == bd.ep_square and can_block(
                pos + vec, king_pos, bd.checker, v
            ):
                moves.append(move.encode(pos, pos + vec))
                break

        return

    single = p_type == cs.N

    for vec in valid_vecs:
        current = pos + vec

        while not current & 0x88:
            if bd.array[current]:
                break

            if can_block(current, king_pos, bd.checker, v):
                moves.append(move.encode(pos, current))
                break

            current += vec

            if single:
                break


def gen_moves_in_check(bd, indices, moves):
    """Appends all legal non-king moves in check to a list."""
    if bd.check == 3:  # only king moves are legal in double check
        return

    king_pos = bd.piece_list[cs.SIDE_OFFSET * bd.black + 4]
    step = cs.UNIT_VEC[utils.square_diff(king_pos, bd.checker)]

    # attempt to capture the checker
    for i in indices:
        loc = bd.piece_list[i]
        p_type = bd.array[loc] & 7
        diff = utils.square_diff(loc, bd.checker)

        if cs.MOVE_TABLE[diff] & cs.CONTACT_MASKS[p_type]:
            moves.append(move.encode(loc, bd.checker))

        if (
            p_type in (cs.B, cs.R, cs.Q)
            and cs.MOVE_TABLE[diff] & cs.DISTANT_MASKS[p_type]
        ):
            v = cs.UNIT_VEC[diff]
            current = loc + v
            valid = True

            while current != bd.checker:
                if bd.array[current]:
                    valid = False
                    break

                current += v

            if valid:
                moves.append(move.encode(loc, bd.checker))

        # attempt to block the checker's piece ray, if a distant check
        if bd.check == 2:
            gen_blocking_move(bd, p_type, loc, king_pos, step, moves)


def gen_pinned_pieces(bd, indices, king_pos, moves):
    """Generates moves for pinned pieces."""

    def gen_ray(bd, start, vec):
        current = start + vec

        while True:
            square = bd.array[current]

            if square:
                if (square >> 3) & 1 != bd.black:
                    moves.append(move.encode(start, current))
                break

            moves.append(move.encode(start, current))
            current += vec

    for v in cs.VALID_VECS[cs.K]:
        pinned = 0
        loc = -1
        attacker = -1
        current = king_pos + v

        while not current & 0x88:
            square = bd.array[current]

            if square:
                if (square >> 3) & 1 != bd.black:
                    if (
                        cs.MOVE_TABLE[utils.square_diff(current, king_pos)]
                        & cs.DISTANT_MASKS[square & 7]
                    ):
                        attacker = current
                    break
                if pinned == 1:  # two pieces blocking this ray
                    pinned = 0
                    break

                pinned += 1
                loc = current

            current += v

        if pinned and attacker != -1:
            piece = bd.array[loc]
            p_type = piece & 7
            indices.remove(piece >> 4)
            vec = v

            if vec not in cs.VALID_VECS[p_type]:
                continue

            if p_type in (cs.B, cs.R, cs.Q):
                gen_ray(bd, loc, vec)
                gen_ray(bd, loc, -vec)
                continue

            if (
                cs.MOVE_TABLE[utils.square_diff(loc, attacker)]
                & cs.CONTACT_MASKS[p_type]
            ):
                moves.append(move.encode(loc, attacker))

            if p_type in (cs.P, cs.p) and vec == cs.VALID_VECS[p_type][0]:
                if not bd.array[loc + vec]:
                    moves.append(move.encode(loc, loc + vec))

                if loc >> 4 == 1 + 5 * bd.black:
                    if not bd.array[loc + 2 * vec]:
                        moves.append(move.encode(loc, loc + 2 * vec))

    return indices


def gen_pawn_moves(bd, p_type, pos, moves):
    """Appends all pawn moves from index pos to a list."""
    valid_vecs = cs.VALID_VECS[p_type]

    current = pos + valid_vecs[0]
    if not current & 0x88:
        if not bd.array[current]:
            moves.append(move.encode(pos, current))

            if pos >> 4 == 1 + 5 * bd.black and not bd.array[pos + 2 * valid_vecs[0]]:
                moves.append(move.encode(pos, pos + 2 * valid_vecs[0]))

    for v in valid_vecs[1:]:
        current = pos + v

        if not current & 0x88:
            square = bd.array[current]

            if (square and (square >> 3) & 1 == bd.black) or (
                not square and current != bd.ep_square
            ):
                continue

            moves.append(move.encode(pos, current))


def gen_step(bd, p_type, pos, moves):
    """Appends all pseudo-legal single-step moves for a piece at index pos to a list."""
    for v in cs.VALID_VECS[p_type]:
        loc = pos + v
        if loc & 0x88:
            continue

        square = bd.array[loc]
        if square and (square >> 3) & 1 == bd.black:
            continue

        moves.append(move.encode(pos, loc))


def gen_sliders(bd, p_type, pos, moves):
    """Appends all pseudo-legal moves for a sliding piece at index pos to a list."""
    for v in cs.VALID_VECS[p_type]:
        current = pos

        while True:
            current += v
            if current & 0x88:
                break

            square = bd.array[current]

            if square:
                if (square >> 3) & 1 != bd.black:
                    moves.append(move.encode(pos, current))
                break

            moves.append(move.encode(pos, current))


SELECT = {
    cs.P: gen_pawn_moves,
    cs.p: gen_pawn_moves,
    cs.B: gen_sliders,
    cs.N: gen_step,
    cs.R: gen_sliders,
    cs.Q: gen_sliders,
}


def all_moves(bd):
    """Generates all moves for the side to move."""
    moves = []
    piece_list_offset = cs.SIDE_OFFSET * bd.black

    indices = {
        piece_list_offset + i
        for i in range(16)
        if bd.piece_list[piece_list_offset + i] != -1
    }

    # must always generate king moves
    king_pos = bd.piece_list[piece_list_offset + 4]
    gen_step(bd, cs.K, king_pos, moves)
    indices.remove(piece_list_offset + 4)

    if bd.check:
        gen_moves_in_check(bd, indices, moves)
        return moves

    # generate castle moves if possible
    off = 2 * bd.black
    rank = 0x70 * bd.black

    for castle in (cs.KINGSIDE, cs.QUEENSIDE):
        if not bd.castling_rights[off + castle - 2]:
            continue

        is_kingside = 3 - castle
        if not any(
            bd.array[rank + (1 + 4 * is_kingside) : rank + (4 + 3 * is_kingside)]
        ):
            moves.append(
                move.encode(king_pos, king_pos - 2 + 4 * is_kingside, castling=castle)
            )

    indices = gen_pinned_pieces(bd, indices, king_pos, moves)

    for i in indices:
        loc = bd.piece_list[i]
        p_type = bd.array[loc] & 7
        SELECT[p_type](bd, p_type, loc, moves)

    return moves
