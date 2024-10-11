"Module containing project-wide constants."
NULL_PIECE = 0
BISHOP = 1
KING = 2
KNIGHT = 3
PAWN = 4
QUEEN = 5
ROOK = 6

SYM_FROM_PIECE = {
    NULL_PIECE: "",
    BISHOP: "b",
    KING: "k",
    KNIGHT: "n",
    PAWN: "p",
    QUEEN: "q",
    ROOK: "r",
}
PIECE_FROM_SYM = {j: i for i, j in SYM_FROM_PIECE.items()}

PIECE_FROM_PROM = {0: KNIGHT, 1: BISHOP, 2: ROOK, 3: QUEEN}
PROM_FROM_PIECE = {j: i for i, j in PIECE_FROM_PROM.items()}

KINGSIDE = 2
QUEENSIDE = 3
C_INFO = {KINGSIDE: (0, 2), QUEENSIDE: (1, -2)}

MOVE_TABLE = [0 for _ in range(239)]

# diagonal moves
for i in range(0x22, 0x88, 0x11):
    MOVE_TABLE[0x77 + i] = 0b010001
    MOVE_TABLE[0x77 - i] = 0b010001

for i in range(0x18, 0x72, 0x09):
    MOVE_TABLE[0x77 + i] = 0b010001
    MOVE_TABLE[0x77 - i] = 0b010001

# vertical moves
for i in range(0x20, 0x80, 0x10):
    MOVE_TABLE[0x77 + i] = 0b110000
    MOVE_TABLE[0x77 - i] = 0b110000

# horizontal moves
for i in range(2, 8):
    MOVE_TABLE[0x77 + i] = 0b110000
    MOVE_TABLE[0x77 - i] = 0b110000

# knight moves
MOVE_TABLE[0x77 + 0x19] = 0b001000
MOVE_TABLE[0x77 + 0x21] = 0b001000
MOVE_TABLE[0x77 - 0x19] = 0b001000
MOVE_TABLE[0x77 - 0x21] = 0b001000

# single step moves
MOVE_TABLE[0x77 + 1] = 0b110010
MOVE_TABLE[0x77 - 1] = 0b110010
MOVE_TABLE[0x77 + 0x09] = 0b010011
MOVE_TABLE[0x77 - 0x09] = 0b010011
MOVE_TABLE[0x77 + 0x10] = 0b110010
MOVE_TABLE[0x77 - 0x10] = 0b110010
MOVE_TABLE[0x77 + 0x11] = 0b010011
MOVE_TABLE[0x77 - 0x11] = 0b010011

VECTORS = {"N": -16, "NE": -15, "E": 1, "SE": 17, "S": 16, "SW": 15, "W": -1, "NW": -17}

VALID_VECTORS = {
    BISHOP: {"NW", "NE", "SW", "SE"},
    KING: {"NW", "N", "NE", "E", "SE", "S", "SW", "W"},
    QUEEN: {"NW", "N", "NE", "E", "SE", "S", "SW", "W"},
    ROOK: {"N", "E", "S", "W"},
}

SQUARE_VALS = {
    BISHOP: [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    KING: [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20],
    ],
    KNIGHT: [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    PAWN: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    QUEEN: [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ],
    ROOK: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0],
    ],
}

PIECE_VALS = {
    1: 3,
    2: 10000000,
    3: 3,
    4: 1,
    5: 9,
    6: 5,
}
