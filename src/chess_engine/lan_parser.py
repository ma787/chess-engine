"""This module provides functions that convert valid move strings in long 
algebraic notation to move objects and vice versa."""

import re
import string

from chess_engine import attributes as attrs, move


def to_index(square_str):
    """Converts a square string to a board array index.

    Args:
        square_str (string): The string representing the square, e.g. 'e8'.

    Returns:
        tuple: The indices of the square in the board array.
    """
    return (int(square_str[1]) - 1, string.ascii_lowercase.index(square_str[0]))


def to_string(coord):
    """Converts a board array index to a square string.

    Args:
        coord (tuple): The indices of the square in the board array.

    Returns:
        string: The string representing the square.
    """
    return string.ascii_letters[coord[1]] + str(coord[0] + 1)


def convert_lan_to_move(move_string, black):
    """Validates and changes the move string entered by the user to a move object.

    Args:
        move_string (string): The LAN representation of the requested move.
        black (int): Whether the current side to move on the board is black. Used
            to determine castle move coordinates.

    Returns:
        Move: The move object represented by the move string.
    """
    p_types = {"B": 1, "K": 2, "N": 3, "P": 4, "Q": 5, "R": 6}
    promotion = 0
    castling = None
    capture = False

    first_rank = 7 if black else 0

    if re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string) is not None:
        capture = move_string[3] == "x"
        start_coord = to_index(move_string[1:3])
        end_coord = to_index(move_string[-2:])

    elif re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string) is not None:
        for p, t in p_types.items():
            if move_string[-1] == p:
                promotion = t
                break

        capture = move_string[2] == "x"

        start_coord = to_index(move_string[0:2])
        end_coord = to_index(move_string[-2:] if not promotion else move_string[-3:-1])

        if end_coord[0] == 7 - first_rank and not promotion:
            return None

    elif move_string in ("0-0", "0-0-0"):
        castling = (
            attrs.Castling.QUEEN_SIDE
            if move_string == "0-0-0"
            else attrs.Castling.KING_SIDE
        )
        file = 2 if castling == attrs.Castling.QUEEN_SIDE else 4

        start_coord = (first_rank, 4)
        end_coord = (first_rank, file)
    else:
        return None

    return move.Move(
        start_coord,
        end_coord,
        capture=capture,
        castling=castling,
        promotion=promotion,
    )


def convert_move_to_lan(move_obj, board):
    """Converts a move object to a move string in LAN.

    Args:
        move_obj (Move): The move object to convert.
        board (Board): The board to perform the move object on.

    Returns:
        string: The string representing the move in LAN.
    """
    symbols = {0: "", 1: "B", 2: "K", 3: "N", 4: "P", 5: "Q", 6: "R"}

    user_input = ""

    if move_obj.castling:
        if move_obj.castling == attrs.Castling.QUEEN_SIDE:
            return "0-0-0"
        return "0-0"

    piece = board.array[move_obj.start[0]][move_obj.start[1]]

    if abs(piece) != 4:
        user_input += symbols[abs(piece)]

    user_input += to_string(move_obj.start)
    user_input += "x" if move_obj.capture else "-"
    user_input += to_string(move_obj.destination)
    user_input += symbols[abs(move_obj.promotion)]

    return user_input
