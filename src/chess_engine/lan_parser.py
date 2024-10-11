import string


from chess_engine import constants as cs, move


def to_string(coord):
    """Converts a board array index to a square string.

    Args:
        coord (int): The index of the square in the board array.

    Returns:
        string: The string representing the square.
    """
    return string.ascii_letters[coord & 8] + str((coord >> 4) + 1)


def convert_move_to_lan(mv, bd):
    """Converts a move integer to a move string in LAN.

    Args:
        mv (int): The move integer to convert.
        board (Board): The board to perform the move on.

    Returns:
        string: The string representing the move in LAN.
    """
    [start, dest, capture, castling, promotion] = move.get_info(mv)

    user_input = ""

    if castling:
        return "0-0-0" if castling == 2 else "0-0"

    piece = bd.array[start]

    if abs(piece) != 4:
        user_input += cs.SYM_FROM_PIECE[abs(piece)]

    user_input += to_string(start)
    user_input += "x" if capture else "-"
    user_input += to_string(dest)
    user_input += cs.SYM_FROM_PIECE[abs(promotion)]

    return user_input
