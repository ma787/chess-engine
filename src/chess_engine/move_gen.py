"""Module providing move generation functions."""

from chess_engine import constants as cs, move, utils


def gen_pawn_moves(bd, vecs, pos, moves):
    """Appends all pawn moves from index pos to a list."""
    straight = cs.FW * (1 - 2 * bd.black)

    for v in vecs:
        if v == straight:
            current = pos + straight
            if not bd.array[current]:
                moves.append(move.encode(pos, current))

                if (pos >> 4) - 4 == 1 + 5 * bd.black and not bd.array[
                    pos + 2 * straight
                ]:
                    moves.append(move.encode(pos, pos + 2 * straight))
            continue

        current = pos + v
        square = bd.array[current]

        if (
            square == cs.GD
            or (square and (square >> 3) & 1 == bd.black)
            or (not square and current != bd.ep_square)
        ):
            continue

        moves.append(move.encode(pos, current))


def gen_step(bd, vecs, pos, moves):
    """Appends all pseudo-legal single-step moves for a piece at index pos to a list."""
    for v in vecs:
        square = bd.array[pos + v]

        if square == cs.GD or square and (square >> 3) & 1 == bd.black:
            continue

        moves.append(move.encode(pos, pos + v))


def gen_sliders(bd, vecs, pos, moves):
    """Appends any piece moves along the provided set of vectors to a list."""
    for v in vecs:
        current = pos

        while True:
            current += v
            square = bd.array[current]

            if square:
                if square != cs.GD and (square >> 3) & 1 != bd.black:
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


def gen_move_in_check(bd, king_pos, step, vecs, loc, moves):
    """Appends any moves that the current piece can make to escape check to a list."""
    p_type = bd.array[loc] & 7
    diff = utils.square_diff(loc, bd.checker)
    v = cs.UNIT_VEC[diff]

    if cs.MOVE_TABLE[diff] & cs.CONTACT_MASKS[p_type] and v in vecs:
        moves.append(move.encode(loc, bd.checker))

    if (
        p_type in (cs.B, cs.R, cs.Q)
        and cs.MOVE_TABLE[diff] & cs.DISTANT_MASKS[p_type]
        and v in vecs
    ):
        current = loc + v
        valid = True

        while current != bd.checker:
            if bd.array[current]:
                valid = False
                break

            current += v

        if valid:
            moves.append(move.encode(loc, bd.checker))

    # attempt ep capture
    if p_type == cs.PAWNS[bd.black] and bd.checker == (
        bd.ep_square + cs.BW * (1 - 2 * bd.black)
    ):
        ep_diff = utils.square_diff(loc, bd.ep_square)
        if (
            cs.MOVE_TABLE[ep_diff] & cs.CONTACT_MASKS[p_type]
            and cs.UNIT_VEC[ep_diff] in vecs
        ):
            moves.append(move.encode(loc, bd.ep_square))

    # attempt to block checker
    if bd.check == 2:
        blocking_moves = []
        SELECT[p_type](bd, vecs, loc, blocking_moves)

        for mv in blocking_moves:
            _, dest, _ = move.decode(mv)

            if cs.UNIT_VEC[utils.square_diff(king_pos, dest)] == step:
                pos = king_pos + step
                while pos != bd.checker:
                    if pos == dest:
                        moves.append(mv)
                    pos += step


def gen_pinned_pieces(bd, indices, king_pos, step, moves):
    """Generates moves for pinned pieces."""
    for v in cs.VALID_VECS[cs.K]:
        pinned = 0
        loc = -1
        attacker = -1
        current = king_pos

        while True:
            current += v
            square = bd.array[current]

            if square:
                if square == cs.GD:
                    break

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

        if pinned and attacker != -1:
            piece = bd.array[loc]
            p_type = piece & 7
            indices.remove(piece >> 4)
            vecs = ()

            if v not in cs.VALID_VECS[p_type]:
                if p_type in cs.PAWNS and -v in cs.VALID_VECS[p_type]:
                    vecs = (-v,)
                else:
                    continue
            elif p_type == cs.PAWNS[bd.black]:
                vecs = (v,)
            elif p_type in (cs.B, cs.R, cs.Q):
                vecs = (v, -v)

            if bd.check:
                gen_move_in_check(bd, king_pos, step, vecs, loc, moves)
            else:
                SELECT[p_type](bd, vecs, loc, moves)

    return indices


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
    gen_step(bd, cs.VALID_VECS[cs.K], king_pos, moves)
    indices.remove(piece_list_offset + 4)

    # generate moves for pinned pieces and in check
    step = cs.UNIT_VEC[utils.square_diff(king_pos, bd.checker)]
    indices = gen_pinned_pieces(bd, indices, king_pos, step, moves)

    if bd.check:
        if bd.check != 3:
            for i in indices:
                loc = bd.piece_list[i]
                vecs = cs.VALID_VECS[bd.array[loc] & 7]
                gen_move_in_check(bd, king_pos, step, vecs, loc, moves)
        return moves

    # generate castle moves if possible
    off = 2 * bd.black
    rank = cs.A1 + (0x70 * bd.black)

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

    for i in indices:
        loc = bd.piece_list[i]
        p_type = bd.array[loc] & 7
        SELECT[p_type](bd, cs.VALID_VECS[p_type], loc, moves)

    return moves
