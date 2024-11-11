"""Modules containing misc functions."""

from chess_engine import constants as cs


def string_to_coord(s):
    """Converts a square string to an array index."""
    return ((int(s[1]) - 1) << 4) + (cs.FILES.index(s[0]))


def coord_to_string(coord):
    """Converts an array index to a square string."""
    return cs.FILES[coord & 0x0F] + str((coord >> 4) + 1)


def is_rank(coord, rank):
    """Checks if a coordinate is at a certain rank."""
    return (coord >> 4) == rank


def is_file(coord, file):
    """Checks if a coordinate is at a certain file."""
    return (coord & 0x0F) == file


def get_piece_type(piece):
    """Returns the piece type of a piece."""
    return piece & 7


def get_piece(p_type, black):
    """Returns a piece of the provided type and colour."""
    return p_type | (black << 3)


def change_colour(piece, black):
    """Change a piece's colour."""
    return (piece & 7) | (black << 3)


def is_type(piece, p_type):
    """Determines whether a piece is of the provided type."""
    return get_piece_type(piece) == p_type


def is_colour(piece, black):
    """Determines whether a piece is a given colour."""
    return (piece >> 3) == black


def same_colour(piece_1, piece_2):
    """Determines whether two pieces are the same colour."""
    return (piece_1 >> 3) == (piece_2 >> 3)


def is_piece(piece, p_type, black):
    """Determines whether a piece has a given type and colour."""
    return is_type(piece, p_type) and is_colour(piece, black)
