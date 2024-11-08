"Module providing functions to generate and validate moves."

from chess_engine import constants as cs, move, utils


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
        p_type = utils.get_piece_type(piece)
        for loc in bd.piece_list[piece]:
            diff = pos - loc
            x88_diff = 0x77 + diff

            if p_type == cs.P:
                can_move = (
                    cs.MOVE_TABLE[x88_diff] & cs.MASKS[piece] and abs(diff) != cs.FW
                )
            else:
                can_move = cs.MOVE_TABLE[x88_diff] & cs.MASKS[p_type]

            if can_move:
                if p_type in (cs.K, cs.N, cs.P):
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


def check_move(bd, moves, start, dest, castling=0, promotion=0):
    """Appends a pseudo-legal move to a list if it is legal.

    Args:
        bd (Board): The board to analyse.
        moves (list): A list of encoded moves.
        start (int): The starting position of the move.
        dest (int): The destination square of the move.
        castling (int, optional): The type of castle move (if applicable).
            Defaults to 0.
        promotion (int, optional): The piece type to promote a pawn to
            (if applicable). Defaults to 0.
    """
    mv = move.encode(start, dest, castling, promotion)

    if castling:
        squares = [
            x + 2 * int(castling == cs.KINGSIDE) + 0x70 * bd.black for x in range(2, 5)
        ]

        for sqr in squares:
            if find_attack(bd, sqr, bd.black ^ 1):
                return

        moves.append(mv)
        return

    move.make_move(mv, bd)

    if not square_under_threat(bd, bd.find_king(bd.black ^ 1)):
        moves.append(mv)

    move.unmake_move(mv, bd)


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
                check_move(bd, moves, pos, current + v)
        else:
            valid = (square and utils.is_colour(square, bd.black ^ 1)) or (
                not square and current == bd.ep_square
            )

        if not valid:
            continue

        if utils.is_rank(current, 7 * (bd.black ^ 1)):
            for p in (cs.B, cs.N, cs.Q, cs.R):
                check_move(bd, moves, pos, current, promotion=p)
        else:
            check_move(bd, moves, pos, current)


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
                check_move(bd, moves, pos, pos - 2 + 4 * is_kingside, castling=castle)

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

            check_move(bd, moves, pos, current)

            if not scale or square:
                break


def all_moves(bd):
    """Finds all the legal moves that the side to move can make.

    Args:
        bd (Board): The board to analyse.

    Returns:
        list: A list of all pseudo-legal moves from the board position.
    """
    moves = []
    pieces = cs.PIECES_BY_COLOUR[bd.black]

    for piece in pieces:
        p_type = utils.get_piece_type(piece)

        if p_type == cs.P:
            for pos in list(bd.piece_list[piece]):
                gen_pawn_moves(bd, pos, moves)
        else:
            for pos in list(bd.piece_list[piece]):
                gen_moves(bd, p_type, pos, moves)

    return moves
