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
        if square and (square >> 3) & 1 == bd.black:
            continue

        current += v
        while not current & 0x88:
            square = bd.array[current]
            if square:
                if (square >> 3) & 1 != bd.black and cs.MOVE_TABLE[
                    utils.square_diff(current, pos)
                ] & cs.DISTANT_MASKS[square & 7]:
                    checkers.append(current)
                break
            current += v

    return checkers


def get_board_array(bstr):
    """Converts a board string to an array and piece dictionary."""
    rows = "/".join(reversed(bstr.split("/")))

    # fmt: off
    pieces = (
        cs.P, cs.N, cs.B, cs.R, cs.Q, cs.K,
        cs.bp, cs.n, cs.b, cs.r, cs.q, cs.k
    )
    # fmt: on

    piece_dict = {p: set() for p in pieces}
    arr = [0 for _ in range(128)]
    i = 0

    for sqr in rows:
        if sqr == "/":
            i += 8
        else:
            try:
                piece = cs.LETTERS.index(sqr)
                arr[i] = piece
                piece_dict[piece].add(i)
                i += 1
            except ValueError:
                i += int(sqr)

    return arr, piece_dict


def get_piece_list(arr, piece_dict, black, c_rights, ep):
    """Converts a board string to an array and a piece list.

    Args:
        arr (list): The board array.
        piece_dict (dict): A dictionary associating each piece
            type/colour with its positions on the board.
        black (int): Whether the side to move is black.
        c_rights (list): The castling rights.
        ep (int): The en passant square.

    Returns:
        list: A list containing the current positions of all 32 pieces
            in the starting position.
    """

    def update_piece(piece, position, offset, p_list):
        p_list[offset] = position
        piece_dict[piece].remove(position)
        arr[position] |= offset << 4

    def find_pieces(p_type, side, row_offs, p_list):
        off = cs.SIDE_OFFSET * side
        for i in row_offs:
            if piece_list[off + i] == -1:
                piece = p_type | (side << 3)
                if piece_dict[piece]:
                    update_piece(piece, min(piece_dict[piece]), off + i, p_list)

    piece_list = [-1 for _ in range(32)]

    for side in (cs.WHITE, cs.BLACK):
        off = cs.SIDE_OFFSET * side

        # identify rooks required for castling rights
        for i in range(2):
            if c_rights[2 * side + i]:
                rook = cs.R | (side << 3)
                pos = 0x70 * side + 7 * (1 - i)
                update_piece(rook, pos, off + 7 * i, piece_list)

        # find kings
        king = cs.K | (side << 3)
        update_piece(king, min(piece_dict[king]), off + 4, piece_list)

    # identify enemy pawn that has just moved two steps from starting position
    if ep != -1:
        side = black ^ 1
        pawns = (cs.P, cs.p | (side << 3))
        pawn_pos = ep + cs.BW * (1 - 2 * black)
        piece_off = cs.SIDE_OFFSET * side + 8 + (pawn_pos >> 4)
        update_piece(pawns[side], pawn_pos, piece_off, piece_list)

    # search for any other pieces still in their original positions
    for i, loc in enumerate(cs.STARTING_PIECE_LIST):
        if arr[loc] == cs.STARTING_ARRAY[loc] and piece_list[i] == -1:
            update_piece(arr[loc], loc, i, piece_list)

    # find the remaining pieces
    pawn_offsets = list(range(8, 16))
    find_pieces(cs.P, cs.WHITE, pawn_offsets, piece_list)
    find_pieces(cs.p, cs.BLACK, pawn_offsets, piece_list)

    for side in (cs.WHITE, cs.BLACK):
        find_pieces(cs.N, side, (1, 6), piece_list)
        find_pieces(cs.B, side, (2, 5), piece_list)
        find_pieces(cs.R, side, (0, 7), piece_list)
        find_pieces(cs.Q, side, (3,), piece_list)

    # if we have more queens/bishops/knights/rooks than in the starting position
    # these are promoted pawns
    for side in (cs.WHITE, cs.BLACK):
        off = cs.SIDE_OFFSET * side
        pieces = [pc | (side << 3) for pc in (cs.Q, cs.N, cs.R, cs.B)]

        for i in range(8, 16):
            if piece_list[off + i] == -1:
                for piece in pieces:
                    if piece_dict[piece]:
                        update_piece(piece, min(piece_dict[piece]), off + i, piece_list)

    return piece_list


def initialise_check(bd):
    """Sets the check status of the board, and if applicable, the position of the checker."""
    king_pos = bd.piece_list[cs.SIDE_OFFSET * bd.black + 4]
    dist_checkers = find_distant_checkers(bd, king_pos)
    contact = -1

    for v in cs.VALID_VECS[cs.N] + cs.VALID_VECS[cs.Q]:
        loc = king_pos + v
        if not loc & 0x88:
            if (bd.array[loc] >> 3) & 1 != bd.black and cs.MOVE_TABLE[
                utils.square_diff(loc, king_pos)
            ] & cs.CONTACT_MASKS[bd.array[loc] & 7]:
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
    side = info[1] == "b"
    c_rights = [c in info[2] for c in "KQkq"]
    ep = -1 if info[3] == "-" else utils.string_to_coord(info[3])
    arr, piece_dict = get_board_array(info[0])
    piece_list = get_piece_list(arr, piece_dict, side, c_rights, ep)

    bd = board.Board(
        arr, side, c_rights, ep, int(info[4]), int(info[5]), -1, piece_list
    )
    initialise_check(bd)
    return bd
