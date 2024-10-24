"Module containing project-wide constants."

WHITE = 0
BLACK = 1

NULL_PIECE = 0
BISHOP = 1
KING = 2
KNIGHT = 3
PAWN = 4
QUEEN = 5
ROOK = 6

WHITE_PIECES = {BISHOP, KING, KNIGHT, PAWN, QUEEN, ROOK}
BLACK_PIECES = {-p for p in WHITE_PIECES}
ALL_PIECES = set.union(WHITE_PIECES, BLACK_PIECES)

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

SYM_FROM_CASTLE = {0: "Q", 1: "K", 2: "q", 3: "k"}

KINGSIDE = 2
QUEENSIDE = 3
C_INFO = {KINGSIDE: (0, 2), QUEENSIDE: (1, -2)}

VECTORS = {"N": 16, "NW": 15, "NE": 17, "S": -16, "SW": -17, "SE": -15, "E": 1, "W": -1}

KNIGHT_VECTORS = (
    2 * VECTORS["N"] + VECTORS["E"],
    2 * VECTORS["N"] + VECTORS["W"],
    2 * VECTORS["S"] + VECTORS["E"],
    2 * VECTORS["S"] + VECTORS["W"],
    2 * VECTORS["E"] + VECTORS["N"],
    2 * VECTORS["E"] + VECTORS["S"],
    2 * VECTORS["W"] + VECTORS["N"],
    2 * VECTORS["W"] + VECTORS["S"],
)

VALID_VECTORS = {
    BISHOP: {"NW", "NE", "SW", "SE"},
    KING: {"NW", "N", "NE", "E", "SE", "S", "SW", "W"},
    QUEEN: {"NW", "N", "NE", "E", "SE", "S", "SW", "W"},
    ROOK: {"N", "E", "S", "W"},
}

VALID_PAWN_VECTORS = {WHITE: "N", BLACK: "S"}

MASKS = {p: 1 << (p - 1) for p in (BISHOP, KING, KNIGHT, PAWN, QUEEN, ROOK)}
MOVE_TABLE = [0 for _ in range(239)]
CHEBYSHEV = [0 for _ in range(239)]


for i in range(1, 8):
    # sliding diagonal moves
    for v in ("N", "E", "S", "W"):
        MOVE_TABLE[0x77 + i * VECTORS[v]] = MASKS[QUEEN] | MASKS[ROOK]
        CHEBYSHEV[0x77 + i * VECTORS[v]] = i

    # sliding vertical/horizontal moves
    for v in ("NE", "SE", "SW", "NW"):
        MOVE_TABLE[0x77 + i * VECTORS[v]] = MASKS[BISHOP] | MASKS[QUEEN]
        CHEBYSHEV[0x77 + i * VECTORS[v]] = i

# king moves
for _, vec in VECTORS.items():
    MOVE_TABLE[0x77 + vec] |= MASKS[KING]

# knight moves
for vec in KNIGHT_VECTORS:
    MOVE_TABLE[0x77 + vec] = MASKS[KNIGHT]
