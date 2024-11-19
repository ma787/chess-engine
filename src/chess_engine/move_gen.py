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


def gen_pawn_blocking_move(bd, pos, king_pos, v, moves):
    """Appends any pawn moves which block a checking slider to a list."""
    valid_vecs = cs.VALID_VECS[cs.P | (bd.black << 3)]
    current = pos + valid_vecs[0]

    if not bd.array[current]:
        if can_block(current, king_pos, bd.checker, v):
            if current >> 4 == 7 * (1 - bd.black):
                for p_type in (cs.N, cs.B, cs.R, cs.Q):
                    moves.append(move.encode(pos, current, promotion=p_type))
            else:
                moves.append(move.encode(pos, current))

        if pos >> 4 == 1 + 5 * bd.black:
            double_push = pos + 2 * valid_vecs[0]

            if not bd.array[double_push] and can_block(
                double_push, king_pos, bd.checker, v
            ):
                moves.append(move.encode(pos, double_push))

    # ep captures to block check are only possible in unreachable positions
    for vec in valid_vecs[1:]:
        current = pos + vec
        if current == bd.ep_square and can_block(current, king_pos, bd.checker, v):
            moves.append(move.encode(pos, current))
            return


def gen_knight_blocking_move(bd, pos, king_pos, v, moves):
    """Appends any knight moves which block a checking slider to a list."""
    for vec in cs.VALID_VECS[cs.N | (bd.black << 3)]:
        current = pos + vec

        if (
            not current & 0x88
            and not bd.array[current]
            and can_block(current, king_pos, bd.checker, v)
        ):
            moves.append(move.encode(pos, current))


def gen_slider_blocking_move(bd, pos, king_pos, v, moves):
    """Appends any sliding piece moves which block a checking slider to a list."""
    for vec in cs.VALID_VECS[bd.array[pos]]:
        current = pos + vec

        while not current & 0x88:
            if bd.array[current]:
                break

            if can_block(current, king_pos, bd.checker, v):
                moves.append(move.encode(pos, current))
                break

            current += vec


def gen_pawn_moves(bd, p_type, pos, moves):
    """Appends all pawn moves from index pos to a list."""
    valid_vecs = cs.VALID_VECS[p_type | (bd.black << 3)]

    current = pos + valid_vecs[0]
    if not current & 0x88:
        if not bd.array[current]:
            if current >> 4 == 7 * (1 - bd.black):
                for pc in (cs.N, cs.B, cs.R, cs.Q):
                    moves.append(move.encode(pos, current, promotion=pc))
            else:
                moves.append(move.encode(pos, current))

            if pos >> 4 == 1 + 5 * bd.black and not bd.array[pos + 2 * valid_vecs[0]]:
                moves.append(move.encode(pos, pos + 2 * valid_vecs[0]))

    for v in valid_vecs[1:]:
        current = pos + v

        if not current & 0x88:
            square = bd.array[current]

            if (square and square >> 3 == bd.black) or (
                not square and current != bd.ep_square
            ):
                continue

            if current >> 4 == 7 * (1 - bd.black):
                for pc in (cs.N, cs.B, cs.R, cs.Q):
                    moves.append(move.encode(pos, current, promotion=pc))
            else:
                moves.append(move.encode(pos, current))


def gen_step(bd, p_type, pos, moves):
    """Appends all pseudo-legal single-step moves for a piece at index pos to a list."""
    for v in cs.VALID_VECS[p_type]:
        loc = pos + v
        if loc & 0x88:
            continue

        square = bd.array[loc]
        if square and square >> 3 == bd.black:
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
                if square >> 3 != bd.black:
                    moves.append(move.encode(pos, current))
                break

            moves.append(move.encode(pos, current))


CHECK_SELECT = {
    cs.P: gen_pawn_blocking_move,
    cs.B: gen_slider_blocking_move,
    cs.N: gen_knight_blocking_move,
    cs.R: gen_slider_blocking_move,
    cs.Q: gen_slider_blocking_move,
}


def gen_moves_in_check(bd, pieces, moves):
    """Appends all legal non-king moves in check to a list."""
    if bd.check == 3:  # only king moves are legal in double check
        return

    # attempt to capture the checker
    for piece in pieces:
        p_type = piece & 7

        for loc in bd.piece_list[piece]:
            diff = utils.square_diff(loc, bd.checker)

            if cs.MOVE_TABLE[diff] & cs.CONTACT_MASKS[piece]:
                if p_type == cs.P and bd.checker >> 4 == 7 * (1 - bd.black):
                    for pc in (cs.N, cs.B, cs.R, cs.Q):
                        moves.append(move.encode(loc, bd.checker, promotion=pc))
                else:
                    moves.append(move.encode(loc, bd.checker))

            if p_type > cs.N and cs.MOVE_TABLE[diff] & cs.DISTANT_MASKS[piece]:
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
    king_pos = bd.find_king(bd.black)

    if bd.check == 2:
        step = cs.UNIT_VEC[utils.square_diff(king_pos, bd.checker)]

        for piece in pieces:
            for loc in bd.piece_list[piece]:
                CHECK_SELECT[piece & 7](bd, loc, king_pos, step, moves)


def gen_pinned_pieces(bd, king_pos, moves):
    """Generates moves for pinned pieces."""
    skipped = []

    def gen_ray(bd, start, vec):
        current = start + vec

        while True:
            square = bd.array[current]

            if square:
                if square >> 3 != bd.black:
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
                if square >> 3 != bd.black:
                    if (
                        cs.MOVE_TABLE[utils.square_diff(current, king_pos)]
                        & cs.DISTANT_MASKS[square]
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
            skipped.append(loc)
            vec = v

            if vec not in cs.VALID_VECS[piece]:
                if p_type == cs.P and -v in cs.VALID_VECS[piece]:
                    vec = -v
                else:
                    continue

            if p_type in (cs.B, cs.R, cs.Q):
                gen_ray(bd, loc, vec)
                gen_ray(bd, loc, -vec)
                continue

            if (
                cs.MOVE_TABLE[utils.square_diff(loc, attacker)]
                & cs.CONTACT_MASKS[piece]
            ):
                moves.append(move.encode(loc, attacker))

            if p_type == cs.P and vec == cs.VALID_VECS[piece][0]:
                if not bd.array[loc + vec]:
                    moves.append(move.encode(loc, loc + vec))

                if loc >> 4 == 1 + 5 * bd.black:
                    if not bd.array[loc + 2 * vec]:
                        moves.append(move.encode(loc, loc + 2 * vec))

    return skipped


SELECT = {
    cs.P: gen_pawn_moves,
    cs.B: gen_sliders,
    cs.N: gen_step,
    cs.R: gen_sliders,
    cs.Q: gen_sliders,
}


def all_moves(bd):
    """Generates all moves for the side to move."""
    moves = []
    pieces = set(cs.PIECES_BY_COLOUR[bd.black])

    # must always generate king moves
    king_pos = bd.find_king(bd.black)
    gen_step(bd, cs.K, king_pos, moves)
    pieces.remove(cs.K | (bd.black << 3))

    if bd.check:
        gen_moves_in_check(bd, pieces, moves)
        return moves

    for castle in (cs.KINGSIDE, cs.QUEENSIDE):
        if not bd.can_castle(bd.black, castle):
            continue

        rank = 0x70 * bd.black
        is_kingside = 3 - castle
        if not any(
            bd.array[rank + (1 + 4 * is_kingside) : rank + (4 + 3 * is_kingside)]
        ):
            moves.append(
                move.encode(king_pos, king_pos - 2 + 4 * is_kingside, castling=castle)
            )

    skipped = gen_pinned_pieces(bd, king_pos, moves)
    skipped.append(king_pos)

    for piece in pieces:
        p_type = piece & 7

        for loc in bd.piece_list[piece]:
            if loc not in skipped:
                SELECT[p_type](bd, p_type, loc, moves)

    return moves
