"Module providing a piece class and subclasses for each piece type."


class Piece:
    """A class representing a chess piece. Not meant to be instantiated.

    Attributes:
        value (int): Signifies the relative importance of the piece and is added
        to the score of the side that captures it.
        symbol (string): A letter associated with each piece type.
        move_set (list): A list of tuples indicating the directions in which pieces
        can move.
        scale (bool): Indicates whether the piece can move any number of squares.
        move_count (int): The number of times the piece has been moved.
        icons (tuple): Two unicode symbols for the piece type, one for each colour.
    """

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
    value = 10000
    symbol = "k"
    move_set = [(0, 1), (1, 0), (1, 1)]
    icons = ("\u2654", "\u265a")
