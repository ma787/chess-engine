import sys


class Piece:
    value = 0
    symbol = ""
    move_set = []
    scale = False
    move_count = 0
    icons = ()

    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.icon = self.icons[self.colour.value]


class Pawn(Piece):
    value = 1
    symbol = "p"
    move_set = [(1, 0), (2, 0), (1, 1)]
    icons = ("\u2659", "\u265f")


class Knight(Piece):
    value = 3
    symbol = "n"
    move_set = [(1, 2), (2, 1)]
    icons = ("\u2658", "\u265e")


class Bishop(Piece):
    value = 3
    symbol = "b"
    move_set = [(1, 1)]
    scale = True
    icons = ("\u2657", "\u265d")


class Rook(Piece):
    value = 5
    symbol = "r"
    move_set = [(0, 1), (1, 0)]
    scale = True
    icons = ("\u2656", "\u265c")


class Queen(Piece):
    value = 9
    symbol = "q"
    move_set = [(0, 1), (1, 0), (1, 1)]
    scale = True
    icons = ("\u2655", "\u265b")


class King(Piece):
    value = sys.maxsize - 206  # 206 is the total value of all other possible pieces, prevents overflow
    symbol = "k"
    move_set = [(0, 1), (1, 0), (1, 1)]
    icons = ("\u2654", "\u265a")
