"Module providing functions to generate and validate moves."

from chess_engine import constants as cs, move


def get_piece_locs(bd, black):
    """Returns a list of all piece locations for a side.

    Args:
        bd (Board): The board to search.
        black (int): Whether the side is black.

    Returns:
        list: A list of all piece locations for the side.
    """
    pieces = cs.BLACK_PIECES if black else cs.WHITE_PIECES
    piece_locs = []

    for p in pieces:
        piece_locs.extend(bd.piece_list[p])

    return piece_locs


def square_under_threat(bd, pos):
    """Checks if a position can be attacked by the side to move.

    Args:
        bd (Board): The board to analyse.
        pos (int): The index of the position to check for attacks
            on. Must be either empty or occupied by an enemy piece.

    Returns:
        bool: True if a pseudo-legal attack on any of the squares exists,
            otherwise False.
    """
    piece_locs = get_piece_locs(bd, bd.black)

    for loc in piece_locs:
        piece = bd.array[loc]
        p_type = abs(piece)
        diff = pos - loc
        x88_diff = 0x77 + diff

        if p_type == cs.PAWN:
            can_move = (
                cs.MOVE_TABLE[x88_diff] & cs.MASKS[piece]
                and abs(diff) != cs.VECTORS["N"]
            )
        else:
            can_move = cs.MOVE_TABLE[x88_diff] & cs.MASKS[p_type]

        if can_move:
            if p_type in (cs.KING, cs.KNIGHT, cs.PAWN):
                return True

            dist = cs.CHEBYSHEV[x88_diff]
            vec = int(diff / dist)
            blocked = False

            for i in range(1, dist):
                if bd.array[loc + i * vec]:
                    blocked = True

            if not blocked:
                return True

    return False


def find_attack(bd, pos, black):
    """Checks if a position can be attacked by a side."""
    switch = False

    if bd.black != black:
        switch = True
        bd.switch_side()

    threat = square_under_threat(bd, pos)

    if switch:
        bd.switch_side()

    return threat


def in_check(bd):
    """Checks if the side to move's king is under attack."""
    return find_attack(bd, bd.find_king(bd.black), bd.black ^ 1)


def legal(mv, bd):
    """Checks if a pseudo-legal move does not leave the king in check.

    Args:
        mv (string): The move string.
        bd (Board): The board to analyse.

    Returns:
        bool: True if the move is legal, and False otherwise.
    """
    [start, dest, _] = move.get_info(mv)
    castling = move.castle_type(bd, start, dest)

    if castling:
        squares = [
            x + 2 * int(castling == cs.KINGSIDE) + 0x70 * bd.black for x in range(2, 5)
        ]

        for sqr in squares:
            if find_attack(bd, sqr, bd.black ^ 1):
                return False
        return True

    move.make_move(mv, bd)
    valid = not square_under_threat(bd, bd.find_king(bd.black ^ 1))
    move.unmake_move(mv, bd)

    return valid


def gen_pawn_moves(bd, pos, moves):
    """Appends all possible moves from a pawn at index pos to a list."""
    mul = 1 - 2 * bd.black
    pawn_vec = cs.VECTORS["N"] * mul

    if (
        (pos >> 4) == 1 + 5 * bd.black
        and not bd.array[pos + pawn_vec]
        and not bd.array[pos + 2 * pawn_vec]
    ):
        moves.append(move.to_string(pos, pos + 2 * pawn_vec))

    for v in cs.VALID_VECTORS[bd.array[pos]]:
        vec = cs.VECTORS[v]
        current = pos + vec
        square = bd.array[current]
        vertical = vec == pawn_vec

        capture = not vertical and (square or move.is_en_passant(bd, pos, current))

        if (
            square * mul > 0
            or (vertical and (square or capture))
            or not (vertical or capture)
        ):
            continue

        if (current >> 4) == 7 * (bd.black ^ 1):
            for p in (cs.BISHOP, cs.KNIGHT, cs.QUEEN, cs.ROOK):
                moves.append(move.to_string(pos, current, promotion=p))
        else:
            moves.append(move.to_string(pos, current))


def gen_moves(bd, pos, moves):
    """Appends all possible moves from a piece at index pos to a list.

    Args:
        bd (Board): The board to analyse.
        pos (int): The starting square to generate moves from.
        moves (list): A list of moves to append to.
    """
    mul = 1 - 2 * bd.black
    piece = bd.array[pos]

    if piece * mul <= 0:
        return

    p_type = abs(piece)

    if p_type == cs.PAWN:
        gen_pawn_moves(bd, pos, moves)
        return

    if p_type == cs.KING:
        for i, castle in enumerate(cs.CASTLES):
            if not bd.get_castling_rights(2 * int(bd.black ^ 1) + i):
                continue

            rank = 0x70 * bd.black
            if not any(bd.array[rank + (1 + 4 * (1 - i)) : rank + (4 + 3 * (1 - i))]):
                moves.append(move.to_string(pos, pos + cs.CASTLES[castle]))

    scale = p_type in (cs.BISHOP, cs.QUEEN, cs.ROOK)

    for v in cs.VALID_VECTORS[p_type]:
        current = pos
        vec = cs.VECTORS[v]

        while True:
            current += vec
            if current & 0x88:
                break

            square = bd.array[current]
            capture = square * mul < 0

            if square * mul > 0:
                break

            moves.append(move.to_string(pos, current))

            if not scale or capture:
                break


def all_pseudo_legal_moves(bd):
    """Finds all the pseudo-legal moves that the side to move can make.

    Args:
        bd (Board): The board to analyse.

    Returns:
        list: A list of all pseudo-legal moves from the board position.
    """
    moves = []
    piece_locs = get_piece_locs(bd, bd.black)

    for pos in piece_locs:
        gen_moves(bd, pos, moves)

    return moves


def all_legal_moves(bd):
    """Finds all the legal moves that the side to move can make."""
    return [mv for mv in all_pseudo_legal_moves(bd) if legal(mv, bd)]
