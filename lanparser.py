import re
import string

from castling import Castling
from colour import Colour
from pieces import Bishop, King, Knight, Pawn, Queen, Rook


def convert_lan_to_move(move_string, colour):
    from move import Move

    """Validates and changes the move string entered by the user to a move class."""
    piece_check = re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string)
    pawn_check = re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string)
    castling_check = (move_string in ("0-0", "0-0-0"))

    # compares the format of the string to these expressions

    piece_type = None
    promotion = None
    castling = None
    capture = False

    if piece_check:
        for p in (Bishop, Knight, Rook, Queen, King):
            if p.symbol == move_string[0].lower():
                piece_type = p  # matches the first letter of the string to a type
                break

        if move_string[3] == "x":
            capture = True
        else:
            capture = False

        start_string = move_string[1:3]
        end_string = move_string[-2:]

    elif pawn_check:
        piece_type = Pawn

        for p in (Bishop, Knight, Rook, Queen, King):
            if p.symbol == move_string[-1].lower():
                promotion = p
                break

        if move_string[2] == "x":
            capture = True
        else:
            capture = False

        start_string = move_string[0:2]

        if promotion:
            end_string = move_string[-3:-1]
        else:
            end_string = move_string[-2:]

    elif castling_check:
        piece_type = King
        split_string = move_string.split("-")

        if len(split_string) == 3:
            castling = Castling.QUEEN_SIDE
            end_letter = "c"
        else:
            castling = Castling.KING_SIDE
            end_letter = "g"

        if colour == Colour.WHITE:
            start_string = "e1"
            end_string = end_letter + "1"

        else:
            start_string = "e8"
            end_string = end_letter + "8"
    else:
        return None

    start_coord = (int(start_string[1]) - 1, string.ascii_lowercase.index(start_string[0]))
    end_coord = (int(end_string[1]) - 1, string.ascii_lowercase.index(end_string[0]))

    move = Move(piece_type.symbol, piece_type, colour, start_coord, end_coord, castling=castling,
                is_capture=capture, promotion=promotion)

    return move


def convert_move_to_lan(move):
    """Converts a move class to LAN."""
    user_input = []

    if move.castling:
        if move.castling == Castling.QUEEN_SIDE:
            return "0-0-0"
        else:
            return "0-0"

    if move.piece_symbol != "p":
        user_input.append(move.piece_symbol.upper())

    user_input.append(string.ascii_letters[move.start[1]])
    user_input.append(str(move.start[0] + 1))

    if move.is_capture:
        user_input.append("x")
    else:
        user_input.append("-")

    user_input.append(string.ascii_letters[move.destination[1]])
    user_input.append(str(move.destination[0] + 1))

    if move.promotion:
        user_input.append(move.promotion.symbol.upper())

    user_input = "".join(user_input)

    return user_input
