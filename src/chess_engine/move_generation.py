"Module providing functions to generate and validate moves."

from chess_engine import constants as cs, move


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
    pieces = cs.PIECES_BY_COLOUR[bd.black]

    for piece in pieces:
        p_type = abs(piece)
        for loc in bd.piece_list[piece]:
            diff = pos - loc
            x88_diff = 0x77 + diff

            if p_type == cs.PAWN:
                can_move = (
                    cs.MOVE_TABLE[x88_diff] & cs.MASKS[piece] and abs(diff) != cs.N
                )
            else:
                can_move = cs.MOVE_TABLE[x88_diff] & cs.MASKS[p_type]

            if can_move:
                if p_type in (cs.KING, cs.KNIGHT, cs.PAWN):
                    return True

                dist = cs.CHEBYSHEV[x88_diff]
                v = int(diff / dist)
                blocked = False

                for i in range(1, dist):
                    if bd.array[loc + i * v]:
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
    start, dest, _ = move.get_info(mv)
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
    """Appends all pseudo-legal pawn moves from index pos to a list."""
    fwd = cs.N * bd.mul

    if (pos >> 4) == 1 + 5 * bd.black and not (
        bd.array[pos + fwd] or bd.array[pos + 2 * fwd]
    ):
        moves.append(move.to_string(pos, pos + 2 * fwd))

    for v in cs.VALID_VECS[bd.array[pos]]:
        current = pos + v
        square = bd.array[current]
        vertical = v == fwd

        capture = not vertical and (square or current == bd.ep_square)

        if (
            square * bd.mul > 0
            or (vertical and (square or capture))
            or not (vertical or capture)
        ):
            continue

        if (current >> 4) == 7 * (bd.black ^ 1):
            for p in (cs.BISHOP, cs.KNIGHT, cs.QUEEN, cs.ROOK):
                moves.append(move.to_string(pos, current, promotion=p))
        else:
            moves.append(move.to_string(pos, current))


def gen_moves(bd, p_type, pos, moves):
    """Appends all pseudo-legal moves from a piece at index pos to a list.

    Args:
        bd (Board): The board to analyse.
        p_type (int): The type of the piece to move.
        pos (int): The starting square to generate moves from.
        moves (list): A list of moves to append to.
    """
    if p_type == cs.KING:
        for i, castle in enumerate(cs.CASTLES):
            if not bd.get_castling_rights(2 * (bd.black ^ 1) + i):
                continue

            rank = 0x70 * bd.black
            if not any(bd.array[rank + (1 + 4 * (1 - i)) : rank + (4 + 3 * (1 - i))]):
                moves.append(move.to_string(pos, pos + cs.CASTLES[castle]))

    scale = p_type in (cs.BISHOP, cs.QUEEN, cs.ROOK)

    for v in cs.VALID_VECS[p_type]:
        current = pos

        while True:
            current += v
            if current & 0x88:
                break

            square = bd.array[current]
            capture = square * bd.mul < 0

            if square * bd.mul > 0:
                break

            moves.append(move.to_string(pos, current))

            if not scale or capture:
                break


def all_moves(bd):
    """Finds all the pseudo-legal moves that the side to move can make.

    Args:
        bd (Board): The board to analyse.

    Returns:
        list: A list of all pseudo-legal moves from the board position.
    """
    moves = []
    pieces = cs.PIECES_BY_COLOUR[bd.black]

    for piece in pieces:
        p_type = abs(piece)

        if p_type == cs.PAWN:
            for pos in bd.piece_list[piece]:
                gen_pawn_moves(bd, pos, moves)
        else:
            for pos in bd.piece_list[piece]:
                gen_moves(bd, p_type, pos, moves)

    return [mv for mv in moves if legal(mv, bd)]
