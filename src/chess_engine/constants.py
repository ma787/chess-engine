"Module containing project-wide constants."

WHITE = 0
BLACK = 1

BISHOP = 1
KING = 2
KNIGHT = 3
PAWN = 4
QUEEN = 5
ROOK = 6

KINGSIDE = 2
QUEENSIDE = 3

PIECES_BY_COLOUR = [{BISHOP, KING, KNIGHT, PAWN, QUEEN, ROOK}]
PIECES_BY_COLOUR.append({-p for p in PIECES_BY_COLOUR[0]})
ALL_PIECES = set.union(PIECES_BY_COLOUR[WHITE], PIECES_BY_COLOUR[BLACK])

SYM_FROM_PIECE = {
    0: "",
    BISHOP: "b",
    KING: "k",
    KNIGHT: "n",
    PAWN: "p",
    QUEEN: "q",
    ROOK: "r",
}
PIECE_FROM_SYM = {j: i for i, j in SYM_FROM_PIECE.items()}

CASTLES = {KINGSIDE: 2, QUEENSIDE: -2}

N, E, S, W = 16, 1, -16, -1
VECS = {N, E, S, W}

VALID_VECS = {
    BISHOP: (N + E, N + W, S + E, S + W),
    KING: (N, E, S, W, N + E, N + W, S + E, S + W),
    KNIGHT: (
        N + N + E,
        N + N + W,
        S + S + E,
        S + S + W,
        E + E + N,
        E + E + S,
        W + W + N,
        W + W + S,
    ),
    PAWN: (N, N + E, N + W),
    -PAWN: (S, S + E, S + W),
    QUEEN: (N, E, S, W, N + E, N + W, S + E, S + W),
    ROOK: (N, E, S, W),
}

MASKS = {p: 1 << (p - 1) for p in (BISHOP, KING, KNIGHT, PAWN, QUEEN, ROOK)}
MASKS[-PAWN] = 1 << max(ALL_PIECES)

MOVE_TABLE = [0 for _ in range(239)]
CHEBYSHEV = [0 for _ in range(239)]

for i in range(1, 8):
    # sliding vertical/horizontal moves
    for v in VECS:
        MOVE_TABLE[0x77 + i * v] = MASKS[QUEEN] | MASKS[ROOK]
        CHEBYSHEV[0x77 + i * v] = i

    # sliding diagonal moves
    for v in VALID_VECS[BISHOP]:
        MOVE_TABLE[0x77 + i * v] = MASKS[BISHOP] | MASKS[QUEEN]
        CHEBYSHEV[0x77 + i * v] = i

# king moves
for vec in VALID_VECS[KING]:
    MOVE_TABLE[0x77 + vec] |= MASKS[KING]

# knight moves
for vec in VALID_VECS[KNIGHT]:
    MOVE_TABLE[0x77 + vec] = MASKS[KNIGHT]

# pawn moves
for p in (PAWN, -PAWN):
    for vec in VALID_VECS[p]:
        MOVE_TABLE[0x77 + vec] |= MASKS[p]
