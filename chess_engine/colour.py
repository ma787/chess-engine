from enum import Enum


class Colour(Enum):
    WHITE = 0
    BLACK = 1

    def __eq__(self, other):
        if other:
            return self.value == other.value
        else:
            return False
