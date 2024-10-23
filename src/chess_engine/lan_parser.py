"Module providing functions to convert between algebraic notation and move integers."

import string


from chess_engine import constants as cs, move


def to_coord(s):
    """Converts a square string to a board array index.

    Args:
        s (string): The string representing the square.

    Returns:
        int: The index of the square in the board array.
    """
    return ((int(s[1]) - 1) << 4) + (string.ascii_letters.index(s[0]))


def to_string(coord):
    """Converts a board array index to a square string.

    Args:
        coord (int): The index of the square in the board array.

    Returns:
        string: The string representing the square.
    """
    return string.ascii_letters[coord & 0x0F] + str((coord >> 4) + 1)


def convert_lan_to_move(mstr, bd):
    """Converts a lan string to a move integer.

    Args:
        mstr (str): The lan string to convert.
        bd (Board): The board to perform the move on.

    Returns:
        int: The integer representation of the move.
    """
    start = to_coord(mstr[0:2])
    dest = to_coord(mstr[2:4])
    capture = bd.array[dest] != cs.NULL_PIECE
    castling = 0
    promotion = cs.NULL_PIECE
    king_pos = ((7 * bd.black) << 4) + 4

    if (
        mstr[0] == "e"
        and mstr[2] in ("c", "g")
        and bd.array[king_pos] * (1 - 2 * bd.black) == cs.KING
    ):
        castling = cs.KINGSIDE if mstr[2] == "g" else cs.QUEENSIDE

    if len(mstr) == 5:
        promotion = cs.PIECE_FROM_SYM[mstr[-1]]

    if abs(bd.array[start]) == cs.PAWN and abs((start & 0x0F) - (dest & 0x0F)) == 1:
        capture = True

    return move.encode_move(
        start, dest, capture=capture, castling=castling, promotion=promotion
    )


def convert_move_to_lan(mv, bd):
    """Converts a move integer to a move string in LAN.

    Args:
        mv (int): The move integer to convert.
        bd (Board): The board to perform the move on.

    Returns:
        string: A LAN string with this format:
            source|target|promotion
    """
    [start, dest, _, castling, promotion] = move.get_info(mv)

    if castling:
        rank = str(1 + 7 * bd.black)
        file = "c" if castling == cs.QUEENSIDE else "g"
        return "e" + rank + file + rank

    return to_string(start) + to_string(dest) + cs.SYM_FROM_PIECE[abs(promotion)]
