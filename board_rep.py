board = [0 for x in range(120)]
illegal = 88

for x in range(20):
    board[x] = illegal

for y in range(100, 120):
    board[y] = illegal

n = 20
while n < 100:
    board[n] = illegal
    board[n + 9] = illegal
    n += 10

# 4 buffer rows and 2 buffer columns made to avoid off-board moves

letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
digits = list(range(1, 9))

ranks = dict(zip(letters, digits))

digit_strings = [str(x) for x in digits]
tens = [20, 30, 40, 50, 60, 70, 80, 90]

files = dict(zip(digit_strings, tens))

# encodes standard chess position references (e.g. "e1") to the array index

U = 10
D = -10
R = 1
L = -1

# directions to move

initial_positions = {
    "wp": [x for x in range(31, 39)],
    "wb": [23, 26],
    "wn": [22, 27],
    "wr": [21, 28],
    "wq": [24],
    "wk": [25],
    "bp": [x for x in range(81, 89)],
    "bb": [93, 96],
    "bn": [92, 97],
    "br": [91, 98],
    "bq": [94],
    "bk": [95]
}

# the positions in the array of the pieces in the initial chess arrangement

for row in initial_positions.values():
    for item in row:
        board[item] = 1

# setting the initial board positions


class Piece:
    piece_list = []

    def __init__(self, piece_type, colour, moves, value, positions):
        self.piece_type = piece_type
        self.colour = colour
        self.moves = moves
        self.value = value
        self.positions = positions

        Piece.piece_list.append(self)

    def make_move(self, start_pos, end_pos):
        """Checks that the move is legal and carries it out."""


white_pawn = Piece(1, "white", (U, U + U, U + R, U + L), 1, initial_positions["wp"])
white_bishop = Piece(2, "white", (U + R, U + L, D + R, D + L), 3, initial_positions["wb"])
white_knight = Piece(3, "white", (U + U + R, U + U + L, D + D + R, D + D + L), 3, initial_positions["wn"])
white_rook = Piece(4, "white", (U, D, R, L), 5, initial_positions["wr"])
white_queen = Piece(5, "white", (U, D, R, L, U + R, U + L, D + R, D + L), 9, initial_positions["wq"])
white_king = Piece(6, "white", (U, D, R, L, U + R, U + L, D + R, D + L), 100000000, initial_positions["wk"])

black_pawn = Piece(1, "black", (U, U + U, U + R, U + L), 1, initial_positions["bp"])
black_bishop = Piece(2, "black", (U + R, U + L, D + R, D + L), 3, initial_positions["bb"])
black_knight = Piece(3, "black", (U + U + R, U + U + L, D + D + R, D + D + L), 3, initial_positions["bn"])
black_rook = Piece(4, "black", (U, D, R, L), 5, initial_positions["br"])
black_queen = Piece(5, "black", (U, D, R, L, U + R, U + L, D + R, D + L), 9, initial_positions["bq"])
black_king = Piece(6, "black", (U, D, R, L, U + R, U + L, D + R, D + L), 100000000, initial_positions["bk"])

# uses the piece class to give every piece their own attributes


def parse_string(check_string):
    """Validates the move string and converts to array indices."""

    if len(check_string) != 4:
        return []
    else:
        pos_refs = [check_string[:2], check_string[2:]]  # splits string into the two positions it points to
        locations = []

        for part in pos_refs:
            if (part[0] in letters) and (part[1] in digit_strings):
                locations.append(ranks[part[0]] + files[part[1]])  # the array indices of the positions
            else:
                return []  # returns an empty array if the format is invalid

        return locations


def check_location(loc_array):
    """Checks if the position on the board is occupied."""

    for piece in Piece.piece_list:
        if loc_array[0] in piece.positions:
            return piece

    return


def is_in_check(side):
    """Checks whether a side's king is in check."""
    return


def check_move_distance(piece, location):
    """Checks if a piece's move-set allows them to reach a square."""
    diff = abs(location[0] - location[1])


fifty_move_counter = 0
side_to_move = "white"

while 1:
    move_string = input("What move would you like to make: ")
    move_locations = parse_string(move_string)

    if not move_locations:
        print("Please enter your move in the correct format, e.g. 'a1b2'.")

    piece_to_move = check_location(move_locations)

    if not piece_to_move:
        print("There is no piece to move at this position.")

    else:
        piece_to_move.make_move(move_locations[0], move_locations[1])  # passes move to the piece class

    if side_to_move == "white":
        side_to_move = "black"
    else:
        side_to_move = "white"

    break
