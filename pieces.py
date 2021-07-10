import sys

from colour import Colour


class Piece:
    value = 0
    symbol = ""
    icons = ("", "")

    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.has_moved = False
        self.icon = self.icons[self.colour.value]

    def can_move_to_square(self, destination):
        """Checks if the piece's move set allows it to move to the destination square."""
        distance = (destination[0] - self.position[0], destination[1] - self.position[1])  # the change in coordinates

        conditions = ((abs(distance[0]) == abs(distance[1])), ((distance[0] == 0) or (distance[1] == 0)),
                      (abs(distance[0]) > 1) or (abs(distance[1]) > 1))

        # this tuple contains checks to see if the move is diagonal, a straight line or of a magnitude greater than 1

        if self.symbol == "b":
            return conditions[0]

        elif self.symbol == "r":
            return conditions[1]

        elif self.symbol == "q":
            return conditions[0] or conditions[1]

        elif self.symbol == "k":
            return not conditions[2]


class Pawn(Piece):
    value = 1
    symbol = "p"
    icons = ("\u2659", "\u265f")

    def can_move_to_square(self, destination, capture=False):
        distance = (destination[0] - self.position[0], destination[1] - self.position[1])

        if (self.colour == Colour.WHITE) and (distance[0] <= 0):
            return False

        elif (self.colour == Colour.BLACK) and (distance[0] >= 0):
            return False

        if capture:
            if (abs(distance[0]), abs(distance[1])) != (1, 1):
                return False

        elif abs(distance[1]) != 0:
            return False

        if abs(distance[0]) > 1:
            if self.has_moved or (abs(distance[0]) != 2):
                return False

        return True


class Knight(Piece):
    value = 3
    symbol = "n"
    icons = ("\u2658", "\u265e")

    def can_move_to_square(self, destination):
        distance = (destination[0] - self.position[0], destination[1] - self.position[1])

        if (abs(distance[0]) == 2) and (abs(distance[1]) == 1):
            return True

        elif (abs(distance[0]) == 1) and (abs(distance[1]) == 2):
            return True
        else:
            return False


class Bishop(Piece):
    value = 3
    symbol = "b"
    icons = ("\u2657", "\u265d")


class Rook(Piece):
    value = 5
    symbol = "r"
    icons = ("\u2656", "\u265c")


class Queen(Piece):
    value = 9
    symbol = "q"
    icons = ("\u2655", "\u265b")


class King(Piece):
    value = sys.maxsize - 206  # 206 is the total value of all other possible pieces, prevents overflow
    symbol = "k"
    icons = ("\u2654", "\u265a")
