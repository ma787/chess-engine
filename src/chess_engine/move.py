"Module providing move making, unmaking and checking utilities."

from chess_engine import constants as cs, utils


def encode(start, dest, castling=0, promotion=0):
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


def can_attack(bd, piece, loc, pos):
    """Checks if a piece at a location can attack a square."""
    x88_diff = 0x77 + pos - loc

    if cs.MOVE_TABLE[x88_diff] & cs.CONTACT_MASKS[piece]:
        return True

    if cs.MOVE_TABLE[x88_diff] & cs.DISTANT_MASKS[piece]:
        v = cs.UNIT_VEC[x88_diff]
        current = loc + v

        while current != pos:
            if bd.array[current]:
                return False
            current += v

        return True

    return False


def is_square_attacked(bd, pos, black):
    """Checks if a position can be attacked by a side."""
    for v in cs.VALID_VECS[cs.N]:
        loc = pos + v
        if not loc & 0x88 and bd.array[loc] == utils.get_piece(cs.N, black):
            return True

    for v in cs.VALID_VECS[cs.Q]:
        current = pos + v

        while not current & 0x88:
            square = bd.array[current]
            if square:
                if utils.is_colour(square, black) and can_attack(
                    bd, square, current, pos
                ):
                    return True
                break
            current += v

    return False


def check_discovered(bd, start, king_pos):
    """Determines whether a move has discovered a check on a king."""
    if can_attack(bd, cs.Q, start, king_pos):
        v = cs.UNIT_VEC[0x77 - king_pos + start]
        current = king_pos + v

        while not current & 0x88:
            square = bd.array[current]
            if square:
                if (
                    not utils.same_colour(square, bd.array[king_pos])
                    and cs.MOVE_TABLE[0x77 + king_pos - current]
                    & cs.DISTANT_MASKS[square]
                ):
                    return True

                return False
            current += v

    return False


def update_check(bd, start, dest):
    """Updates the check status of the board after a move is made."""
    king_pos = bd.find_king(bd.black)

    if can_attack(bd, bd.array[dest], dest, king_pos):
        bd.check = 1
    elif check_discovered(bd, start, king_pos):
        bd.check = 1
    else:
        bd.check = 0


def legality_test(bd, mv):
    """Checks whether a position is legal after a move is made."""
    if bd.check:
        return not is_square_attacked(bd, bd.find_king(bd.black ^ 1), bd.black)

    start, dest, _, castling = decode(mv)

    if castling:
        squares = [
            x + 2 * int(castling == cs.KINGSIDE) + 0x70 * (bd.black ^ 1)
            for x in range(2, 5)
        ]

        for sqr in squares:
            if is_square_attacked(bd, sqr, bd.black):
                return False

        return True

    king_pos = bd.find_king(bd.black ^ 1)

    if king_pos == dest and is_square_attacked(bd, dest, bd.black):
        return False

    return not check_discovered(bd, start, king_pos)


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
    bd.check = prev_info[3]

    cap_type = prev_info[4]

    if cap_type:
        cap_pos = dest + (
            cs.BW * (1 - 2 * bd.black) * int(dest > 0 and dest == bd.ep_square)
        )
        add_piece(bd, utils.get_piece(cap_type, (bd.black ^ 1)), cap_pos)


def make_move(mv, bd):
    """Carries out a move and updates the board state.

    Args:
        mv (int): An integer encoding the move information.
        bd (Board): The board to update.

    Returns:
        int: 0, if the move is legal and the board is updated,
            or -1, if the move is illegal (causing the move to be
            reversed).
    """
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

    if not legality_test(bd, mv):
        unmake_move(mv, bd)
        return -1

    update_check(bd, start, dest)
    return 0


def gen_pawn_moves(bd, pos, moves):
    """Appends all pseudo-legal pawn moves from index pos to a list."""
    for v in cs.VALID_VECS[bd.array[pos]]:
        current = pos + v
        square = bd.array[current]
        valid = True

        if v in (cs.FW, cs.BW):
            valid = not square

            if (
                utils.is_rank(pos, 1 + 5 * bd.black)
                and valid
                and not bd.array[current + v]
            ):
                moves.append(encode(pos, current + v))
        else:
            valid = (square and utils.is_colour(square, bd.black ^ 1)) or (
                not square and current == bd.ep_square
            )

        if not valid:
            continue

        if utils.is_rank(current, 7 * (bd.black ^ 1)):
            for p in (cs.B, cs.N, cs.Q, cs.R):
                moves.append(encode(pos, current, promotion=p))
        else:
            moves.append(encode(pos, current))


def gen_moves(bd, p_type, pos, moves):
    """Appends all pseudo-legal moves from a piece at index pos to a list.

    Args:
        bd (Board): The board to analyse.
        p_type (int): The type of the piece to move.
        pos (int): The starting square to generate moves from.
        moves (list): A list of moves to append to.
    """
    if p_type == cs.K:
        for castle in (cs.KINGSIDE, cs.QUEENSIDE):
            if not bd.can_castle(bd.black, castle):
                continue

            rank = 0x70 * bd.black
            is_kingside = 3 - castle
            if not any(
                bd.array[rank + (1 + 4 * is_kingside) : rank + (4 + 3 * is_kingside)]
            ):
                moves.append(encode(pos, pos - 2 + 4 * is_kingside, castling=castle))

    scale = p_type in (cs.B, cs.Q, cs.R)

    for v in cs.VALID_VECS[p_type]:
        current = pos

        while True:
            current += v
            if current & 0x88:
                break

            square = bd.array[current]

            if square and utils.is_colour(square, bd.black):
                break

            moves.append(encode(pos, current))

            if not scale or square:
                break


def all_moves(bd):
    """Returns a list of all pseudo-legal moves from this position."""
    moves = []
    pieces = cs.PIECES_BY_COLOUR[bd.black]

    if bd.check == -1:
        bd.check = int(is_square_attacked(bd, bd.find_king(bd.black), bd.black ^ 1))

    for piece in pieces:
        p_type = utils.get_piece_type(piece)

        if p_type == cs.P:
            for pos in list(bd.piece_list[piece]):
                gen_pawn_moves(bd, pos, moves)
        else:
            for pos in list(bd.piece_list[piece]):
                gen_moves(bd, p_type, pos, moves)

    return moves


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
