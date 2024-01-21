import re
import string

from .castling import Castling
from .colour import Colour
from .move import Move
from .pieces import Bishop, King, Knight, Queen, Rook


def convert_lan_to_move(move_string, board):
    """Validates and changes the move string entered by the user to a move class."""
    piece_check = re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string)
    pawn_check = re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string)
    castling_check = (move_string in ("0-0", "0-0-0"))

    promotion = None
    castling = None
    capture = False

    if piece_check:
        if move_string[3] == "x":
            capture = True
        else:
            capture = False

        start_string = move_string[1:3]
        end_string = move_string[-2:]

    elif pawn_check:
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
        split_string = move_string.split("-")

        if len(split_string) == 3:
            castling = Castling.QUEEN_SIDE
            end_letter = "c"
        else:
            castling = Castling.KING_SIDE
            end_letter = "g"

        if board.side_to_move == Colour.WHITE:
            start_string = "e1"
            end_string = end_letter + "1"

        else:
            start_string = "e8"
            end_string = end_letter + "8"
    else:
        return None

    start_coord = (int(start_string[1]) - 1, string.ascii_lowercase.index(start_string[0]))
    end_coord = (int(end_string[1]) - 1, string.ascii_lowercase.index(end_string[0]))

    piece = board.array[start_coord[0]][start_coord[1]]

    if not piece:
        return None

    if pawn_check and piece.symbol != "p":
        return None
    elif piece_check and piece.symbol != move_string[0].lower():
        return None

    move = Move(piece, board, start_coord, end_coord, capture=capture, castling=castling, promotion=promotion)

    return move


def convert_move_to_lan(move):
    """Converts a move class to LAN."""
    user_input = []

    if move.castling:
        if move.castling == Castling.QUEEN_SIDE:
            return "0-0-0"
        else:
            return "0-0"

    if move.piece.symbol != "p":
        user_input.append(move.piece.symbol.upper())

    user_input.append(string.ascii_letters[move.start[1]])
    user_input.append(str(move.start[0] + 1))

    if move.capture:
        user_input.append("x")
    else:
        user_input.append("-")

    user_input.append(string.ascii_letters[move.destination[1]])
    user_input.append(str(move.destination[0] + 1))

    if move.promotion:
        user_input.append(move.promotion.symbol.upper())

    user_input = "".join(user_input)

    return user_input
