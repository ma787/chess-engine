"Module providing board hashing utilities."

import random

from chess_engine import constants as cs, move


random.seed(1)  # set seed for reproducibility
MAX_VAL = 2**64 - 1

# 1 number for each piece at each square (= 768)
# 8 numbers to indicate valid en passant files, if there are any
# 4 numbers to indicate castling rights
# 1 number to indicate that it's black's turn
ARR_LEN = 782
ARRAY = [random.randint(0, MAX_VAL) for _ in range(ARR_LEN - 1)]

# offsets of special board info in the array
OFFS = {"en_passant": -13, "castling": -5, "black": -1}


def get_hash(pos, piece):
    """Gets the number assigned to a piece with a given position and colour.

    Args:
        pos (int): The coordinates of the piece on the board.
        piece (int): The piece type and colour.

    Returns:
        int: The entry in the number array associated with this piece.
    """
    square_off = ((pos & 0xF0) - 0x40) * 6 + ((pos & 0x0F) - 4) * 12

    if (piece >> 3) & 1:
        piece_off = (piece & 0x0F) - 3
    elif piece & 7 == cs.P:
        piece_off = piece & 0x0F
    else:
        piece_off = (piece & 0x0F) - 1

    return ARRAY[square_off + piece_off - 1]


def zobrist_hash(bd):
    """Hashes a board position to a unique number."""
    value = 0
    i = 0

    for i in range(0x44, 0xC4, 0x10):
        for j in range(8):
            square = bd.array[i + j]
            if square:
                value ^= get_hash(i + j, square)

    if bd.black:
        value ^= ARRAY[OFFS["black"]]

    if bd.ep_square != -1:
        value ^= ARRAY[OFFS["en_passant"] + (bd.ep_square & 0x0F) - 4]

    for i in range(4):
        if bd.castling_rights[i]:
            value ^= ARRAY[OFFS["castling"] + i]

    return value


def update_hash(b_hash, mv, bd, pr_type=cs.Q):
    """Updates a board hash for a move to be made.

    Args:
        current_hash (int): The board hash to update.
        mv (int): A move integer.
        bd (Board): The board state before the move is made.
        pr_type (int, optional): The type of piece to promote a pawn to.
            Defaults to Queen.

    Returns:
        int: The hash of the board position after the move is made.
    """
    start, dest, castling = move.decode(mv)
    piece = bd.array[start]

    # moving piece
    b_hash ^= get_hash(start, piece)
    b_hash ^= get_hash(dest, piece)

    cap_pos = -1
    ep_file = -1

    if piece & 7 == cs.PAWNS[bd.black]:
        if (dest >> 4) - 4 == 7 * (1 - bd.black):
            b_hash ^= get_hash(dest, piece)
            b_hash ^= get_hash(dest, pr_type | (bd.black << 3))

        if dest == bd.ep_square and not bd.array[dest]:
            cap_pos = bd.ep_square + (cs.BW * (1 - 2 * bd.black))

        if dest - start in (2 * cs.FW, 2 * cs.BW):
            ep_file = (dest & 0x0F) - 4

    if bd.array[dest]:
        cap_pos = dest

    # removing captured piece
    if cap_pos != -1:
        b_hash ^= get_hash(cap_pos, bd.array[cap_pos])

    if castling:
        # move rook
        r_start = cs.A1 + (0x70 * bd.black) + 7 * (3 - castling)
        rook = cs.R | (bd.black << 3)
        b_hash ^= get_hash(r_start, rook)
        b_hash ^= get_hash(r_start + 5 * castling - 12, rook)

        # remove castling rights
        c_off = 2 * bd.black
        b_hash ^= ARRAY[OFFS["castling"] + c_off]
        b_hash ^= ARRAY[OFFS["castling"] + c_off + 1]

    else:
        moved = (start, dest)
        for side in (cs.WHITE, cs.BLACK):
            c_off = 2 * side
            rank = cs.A1 + (0x70 * side)

            if rank + 4 in moved:
                if bd.castling_rights[c_off]:
                    b_hash ^= ARRAY[OFFS["castling"] + c_off]
                if bd.castling_rights[c_off + 1]:
                    b_hash ^= ARRAY[OFFS["castling"] + c_off + 1]
                break

            if rank in moved and bd.castling_rights[c_off + cs.QUEENSIDE - 2]:
                b_hash ^= ARRAY[OFFS["castling"] + c_off + cs.QUEENSIDE - 2]

            if rank + 7 in moved and bd.castling_rights[c_off + cs.KINGSIDE - 2]:
                b_hash ^= ARRAY[OFFS["castling"] + c_off + cs.KINGSIDE - 2]

    # removing previous en passant file, if any
    if bd.ep_square != -1:
        b_hash ^= ARRAY[OFFS["en_passant"] + (bd.ep_square & 0x0F) - 4]

    # set new en passant file if necessary
    if ep_file != -1:
        b_hash ^= ARRAY[OFFS["en_passant"] + ep_file]

    # switching side to move
    b_hash ^= ARRAY[OFFS["black"]]

    return b_hash
