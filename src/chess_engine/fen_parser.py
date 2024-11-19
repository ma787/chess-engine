"""Module providing functions to create a board object from a fen string."""

import re


from chess_engine import board, constants as cs, utils


def find_distant_checkers(bd, pos):
    """Finds all distant checkers of the king."""
    checkers = []

    for v in cs.VALID_VECS[cs.Q]:
        current = pos + v

        if current & 0x88:
            continue

        square = bd.array[current]
        if square and square >> 3 == bd.black:
            continue

        current += v
        while not current & 0x88:
            square = bd.array[current]
            if square:
                if (
                    square >> 3 != bd.black
                    and cs.MOVE_TABLE[utils.square_diff(current, pos)]
                    & cs.DISTANT_MASKS[square]
                ):
                    checkers.append(current)
                break
            current += v

    return checkers


def initialise_check(bd):
    """Sets the check status of the board, and if applicable, the position of the checker."""
    king_pos = bd.find_king(bd.black)
    dist_checkers = find_distant_checkers(bd, king_pos)
    contact = -1

    for v in cs.VALID_VECS[cs.N] + cs.VALID_VECS[cs.Q]:
        loc = king_pos + v
        if not loc & 0x88:
            if (
                bd.array[loc] >> 3 != bd.black
                and cs.MOVE_TABLE[utils.square_diff(loc, king_pos)]
                & cs.CONTACT_MASKS[bd.array[loc]]
            ):
                contact = loc

    # if checked by more than one piece, only king moves are legal
    # so it doesn't matter what the destination of the last move was
    if contact != -1 and dist_checkers or len(dist_checkers) > 1:
        bd.check = 3
        return

    if contact != -1:
        bd.checker = contact
        bd.check = 1
        return

    if dist_checkers:
        bd.checker = dist_checkers[0]
        bd.check = 2
        return

    bd.check = 0


def fen_to_board(fen_str):
    """Converts a FEN string to a board object."""
    reg = r"\s*^(((?:[rnbqkpRNBQKP1-8]+\/){7})[rnbqkpRNBQKP1-8]+)\s([b|w])\s(-|[K|Q|k|q]{1,4})\s(-|[a-h][1-8])\s(\d+\s\d+)$"
    if re.fullmatch(reg, fen_str) is None:
        raise ValueError

    # info[0]: the squares on the board
    # info[1]: the side to move
    # info[2]: the castling rights
    # info[3]: the en passant square
    # info[4]: the halfmove clock
    # info[5]: the full move number
    info = fen_str.split(" ")
    rows = "/".join(reversed(info[0].split("/")))
    arr = [0 for _ in range(128)]
    i = 0

    for sqr in rows:
        if sqr == "/":
            i += 8
        else:
            try:
                arr[i] = cs.LETTERS.index(sqr)
                i += 1
            except ValueError:
                i += int(sqr)

    c_rights = [c in info[2] for c in "KQkq"]
    ep = -1 if info[3] == "-" else utils.string_to_coord(info[3])

    bd = board.Board(
        arr, int(info[1] == "b"), c_rights, ep, int(info[4]), int(info[5]), -1
    )
    initialise_check(bd)
    return bd
