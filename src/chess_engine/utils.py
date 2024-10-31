"""Modules containing misc functions."""

FILE_TO_INDEX = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
INDEX_TO_FILE = {j: i for i, j in FILE_TO_INDEX.items()}


def string_to_coord(s):
    """Converts a square string to an array index."""
    return ((int(s[1]) - 1) << 4) + (FILE_TO_INDEX[s[0]])


def coord_to_string(coord):
    """Converts an array index to a square string."""
    return INDEX_TO_FILE[coord & 0x0F] + str((coord >> 4) + 1)
