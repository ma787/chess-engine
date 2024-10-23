"Module providing board hashing utilities."

import operator
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


def to_array_index(coord):
    """Converts board array coordinates to a number array index."""
    return coord * 6 + (coord & 8) * 12


def get_hash(position, piece):
    """Gets the number assigned to a piece with a given position and colour.

    Args:
        position (int): The coordinates of the piece on the board.
        piece (int): The piece type and colour.

    Returns:
        int: The entry in the number array associated with this piece.
    """
    return ARRAY[int(to_array_index(position) + abs(piece) - 1 + 6 * int(piece < 0))]


def zobrist_hash(bd):
    """Hashes a board position to a unique number."""
    value = 0
    i = 0

    while i < 0x78:
        square = bd.array[i]
        if square:
            piece_val = get_hash(i, square)
            value = operator.xor(value, piece_val)
        i += 1
        if i & 0x88:
            i += 8

    if bd.black:
        value = operator.xor(value, ARRAY[OFFS["black"]])

    if bd.ep_square:
        value = operator.xor(value, ARRAY[OFFS["en_passant"] + (bd.ep_square & 0x0F)])

    for i in range(4):
        if bd.get_castling_rights(i):
            value = operator.xor(value, ARRAY[OFFS["castling"] + i])

    return value


def remove_castling_rights(current_hash, pos, bd):
    """Removes castling values from the hash after a move/capture.

    Args:
        current_hash (int): The board hash to update.
        pos (int): The position of the piece to move.
        bd (Board): The board to analyse.

    Returns:
        int: The hash updated with any changes to castling rights.
    """
    piece = bd.array[pos]
    p_type = abs(piece)

    if p_type not in (cs.KING, cs.ROOK):
        return current_hash

    if abs(piece) == cs.KING:
        c_off = 2 * (bd.black ^ 1)
        for i in range(0, 2):
            if bd.get_castling_rights(c_off + i):
                current_hash = operator.xor(
                    current_hash, ARRAY[OFFS["castling"] + c_off + i]
                )

    for i, sqr in enumerate((0x77, 0x70, 0x07, 0x00)):
        if pos == sqr and bd.get_castling_rights(i):
            current_hash = operator.xor(current_hash, ARRAY[OFFS["castling"] + i])

    return current_hash


def update_hash(current_hash, mv, bd):
    """Updates a board hash for a move to be made.

    Args:
        current_hash (int): The board hash to update.
        mv (int): The move to be made.
        bd (Board): The board state before the move is made.

    Returns:
        int: The hash of the board position after the move is made.
    """
    [start, dest, capture, castling, promotion] = move.get_info(mv)
    piece = bd.array[start]
    mul = 1 - 2 * bd.black

    # moving piece
    current_hash = operator.xor(current_hash, get_hash(start, piece))
    current_hash = operator.xor(
        current_hash, get_hash(dest, promotion * mul if promotion else piece)
    )

    ep_file = -1

    if capture:
        cap_pos = bd.ep_square if not bd.array[dest] else dest

        # removing captured piece
        current_hash = operator.xor(current_hash, get_hash(cap_pos, bd.array[cap_pos]))

        # removing castling rights after rook capture
        current_hash = remove_castling_rights(current_hash, cap_pos, bd)

    elif castling:
        r_move = move.get_rook_castle(bd, castling)
        current_hash = operator.xor(current_hash, get_hash(r_move[0], cs.ROOK * mul))
        current_hash = operator.xor(current_hash, get_hash(r_move[1], cs.ROOK * mul))

    # updating en passant file after a double pawn push
    elif abs(piece) == cs.PAWN and abs(dest - start) == 0x20:
        ep_file = dest & 0x0F

    # removing castling rights after king/rook move
    current_hash = remove_castling_rights(current_hash, start, bd)

    # removing previous en passant file, if any
    if bd.ep_square:
        current_hash = operator.xor(
            current_hash, ARRAY[OFFS["en_passant"] + (bd.ep_square & 0x0F)]
        )

    # set new en passant file if necessary
    if ep_file != -1:
        current_hash = operator.xor(current_hash, ARRAY[OFFS["en_passant"] + ep_file])

    # switching side to move
    current_hash = operator.xor(current_hash, ARRAY[OFFS["black"]])

    return current_hash
