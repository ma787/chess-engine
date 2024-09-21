"Module providing a piece class and subclasses for each piece type."


class Piece:
    """A class representing a chess piece. Not meant to be instantiated.

    Attributes:
        value (int): Signifies the relative importance of the piece and is added
        to the score of the side that captures it.
        p_type (int): An integer associated with each piece type. Used to encode move
        state.
        symbol (string): A letter associated with each piece type.
        move_set (list): A list of tuples indicating the directions in which pieces
        can move.
        scale (bool): Indicates whether the piece can move any number of squares.
        icons (tuple): Two unicode symbols for the piece type, one for each colour.
    """

    p_type = 0
    symbol = ""
    move_set = []
    scale = False
    icons = ()

    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.icon = self.icons[self.colour.value]

    @staticmethod
    def from_type(p_type):
        """Matches an integer to a piece class.

        Args:
            p_type (int): The type of required piece class.

        Returns:
            Piece: The piece class corresponding to p_type,
            if the value of p_type is between 1 and 6, and None
            otherwise.
        """
        match p_type:
            case 1:
                piece = Bishop
            case 2:
                piece = King
            case 3:
                piece = Knight
            case 4:
                piece = Pawn
            case 5:
                piece = Queen
            case 6:
                piece = Rook
            case _:
                piece = None

        return piece


class Bishop(Piece):
    p_type = 1
    symbol = "b"
    move_set = [(1, 1)]
    scale = True
    icons = ("\u2657", "\u265d")


class King(Piece):
    p_type = 2
    symbol = "k"
    move_set = [(0, 1), (1, 0), (1, 1)]
    icons = ("\u2654", "\u265a")


class Knight(Piece):
    p_type = 3
    symbol = "n"
    move_set = [(1, 2), (2, 1)]
    icons = ("\u2658", "\u265e")


class Pawn(Piece):
    p_type = 4
    symbol = "p"
    move_set = [(1, 0), (2, 0), (1, 1)]
    icons = ("\u2659", "\u265f")


class Queen(Piece):
    p_type = 5
    symbol = "q"
    move_set = [(0, 1), (1, 0), (1, 1)]
    scale = True
    icons = ("\u2655", "\u265b")


class Rook(Piece):
    p_type = 6
    symbol = "r"
    move_set = [(0, 1), (1, 0)]
    scale = True
    icons = ("\u2656", "\u265c")
