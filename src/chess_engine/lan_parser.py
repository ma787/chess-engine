"""This module provides functions that convert valid move strings in long 
algebraic notation to move objects and vice versa."""

import re
import string

from chess_engine import attributes as attrs, move, pieces


def convert_lan_to_move(move_string, colour):
    """Validates and changes the move string entered by the user to a move object.

    Args:
        move_string (string): The LAN representation of the requested move.
        colour (Colour): The current side to move on the board. Used to
        determine castle move coordinates.

    Returns:
        Move: The move object represented by the move string.
    """

    def to_index(square):
        return (int(square[1]) - 1, string.ascii_lowercase.index(square[0]))

    piece_types = {
        "B": pieces.Bishop,
        "K": pieces.King,
        "N": pieces.Knight,
        "Q": pieces.Queen,
        "R": pieces.Rook,
    }

    promotion = None
    castling = None
    capture = False

    if re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string) is not None:
        p_type = piece_types[move_string[0]]
        capture = move_string[3] == "x"

        start_coord = to_index(move_string[1:3])
        end_coord = to_index(move_string[-2:])

    elif re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string) is not None:
        for p, t in piece_types.items():
            if move_string[-1] == p:
                promotion = t
                break

        p_type = pieces.Pawn
        capture = move_string[2] == "x"

        start_coord = to_index(move_string[0:2])
        end_coord = (
            to_index(move_string[-3:-1])
            if promotion is not None
            else to_index(move_string[-2:])
        )

    elif move_string in ("0-0", "0-0-0"):
        p_type = pieces.King
        castling = (
            attrs.Castling.QUEEN_SIDE
            if move_string == "0-0-0"
            else attrs.Castling.KING_SIDE
        )
        rank = 0 if colour == attrs.Colour.WHITE else 7
        file = 2 if castling == attrs.Castling.QUEEN_SIDE else 4

        start_coord = (rank, 4)
        end_coord = (rank, file)
    else:
        return None

    return move.Move(
        start_coord,
        end_coord,
        piece_type=p_type,
        capture=capture,
        castling=castling,
        promotion=promotion,
    )


def convert_move_to_lan(move_obj):
    """Converts a move object to a move string in LAN.

    Args:
        move_obj (Move): The move object to convert.

    Returns:
        string: The string representing the move in LAN.
    """

    def to_string(coord):
        return string.ascii_letters[coord[1]] + str(coord[0] + 1)

    user_input = ""

    if move_obj.castling:
        if move_obj.castling == attrs.Castling.QUEEN_SIDE:
            return "0-0-0"
        return "0-0"

    if move_obj.piece_type != pieces.Pawn:
        user_input += move_obj.piece_type.symbol.upper()

    user_input += to_string(move_obj.start)
    user_input += "x" if move_obj.capture else "-"
    user_input += to_string(move_obj.destination)

    if move_obj.promotion:
        user_input += move_obj.promotion.symbol.upper()

    return user_input
