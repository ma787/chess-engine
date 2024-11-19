"""Modules containing misc functions."""

from chess_engine import constants as cs


def string_to_coord(s):
    """Converts a square string to an array index."""
    return ((int(s[1]) - 1) << 4) + (cs.FILES.index(s[0]))


def coord_to_string(coord):
    """Converts an array index to a square string."""
    return cs.FILES[coord & 0x0F] + str((coord >> 4) + 1)


def square_diff(start, dest):
    """Returns the square difference between two coordinates."""
    return 0x77 + dest - start
