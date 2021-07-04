from enum import Enum


class NodeType(Enum):
    PV = 1
    CUT = 2
    ALL = 3

    def __eq__(self, other):
        if other:
            return self.value == other.value
        else:
            return False
