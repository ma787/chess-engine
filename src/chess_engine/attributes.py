"Module providing enum classes for castling and colour values."

from enum import Enum


class Castling(Enum):
    "Provides enums for castling values."
    QUEEN_SIDE = 1
    KING_SIDE = 2

    def __eq__(self, other):
        if other:
            return self.value == other.value
        return False


class Colour(Enum):
    "Provides enums for castling values."
    WHITE = 0
    BLACK = 1

    def __eq__(self, other):
        if other:
            return self.value == other.value
        return False
