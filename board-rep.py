board = [0 for x in range(120)]
illegal = 88
fifty_move_counter = 0
side_to_move = "white"

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
    "bk": [95],
}

# the positions in the array of the pieces in the initial chess arrangement

for row in initial_positions.values():
    for item in row:
        board[item] = 1

# setting the initial board positions


class Piece:
    def __init__(self, piece_type, colour, moves, value, positions):
        self.piece_type = piece_type
        self.colour = colour
        self.moves = moves
        self.value = value
        self.positions = positions


white_pawn = Piece(1, "white", (U, U + U, U + R, U + L), 1, initial_positions["wp"])
white_bishop = Piece(2, "white", (U + R, U + L, D + R, D + L), 3, initial_positions["wb"])
white_knight = Piece(3, "white", (U + U + R, U + U + L, D + D + R, D + D + L), 3, initial_positions["wn"])
white_rook = Piece(4, "white", (U, D, R, L), 5, initial_positions["wr"])
white_queen = Piece(5, "white", (U, D, R, L, U + R, U + L, D + R, D + L), 9, initial_positions["wq"])
white_king = Piece(6, "white", (U, D, R, L, U + R, U + L, D + R, D + L), 100000000, initial_positions["wk"])

black_pawn = Piece(1, "black", (U, U + U, U + R, U + L ), 1, initial_positions["bp"])
black_bishop = Piece(2, "black", (U + R, U + L, D + R, D + L), 3, initial_positions["bb"])
black_knight = Piece(3, "black", (U + U + R, U + U + L, D + D + R, D + D + L), 3, initial_positions["bn"])
black_rook = Piece(4, "black", (U, D, R, L), 5, initial_positions["br"])
black_queen = Piece(5, "black", (U, D, R, L, U + R, U + L, D + R, D + L), 9, initial_positions["bq"])
black_king = Piece(6, "black", (U, D, R, L, U + R, U + L, D + R, D + L), 100000000, initial_positions["bk"])

# uses the piece class to give every piece their own attributes
