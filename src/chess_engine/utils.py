"""Modules containing misc functions."""

import string


def string_to_coord(s):
    """Converts a square string to an array index."""
    return ((int(s[1]) - 1) << 4) + (string.ascii_letters.index(s[0]))


def coord_to_string(coord):
    """Converts an array index to a square string."""
    return string.ascii_letters[coord & 0x0F] + str((coord >> 4) + 1)
