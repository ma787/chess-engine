from enum import Enum


class Castling(Enum):
    QUEEN_SIDE = 1
    KING_SIDE = 2

    def __eq__(self, other):
        if other:
            return self.value == other.value
        else:
            return False
