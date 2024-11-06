"Module containing project-wide constants."

WHITE, BLACK = 0, 1
KINGSIDE, QUEENSIDE = 2, 3

P, N, B, R, Q, K = 1, 2, 3, 4, 5, 6
p, n, b, r, q, k = 9, 10, 11, 12, 13, 14

# fmt: off
STARTING_ARRAY = [
    R, N, B, Q, K, B, N, R, 0, 0, 0, 0, 0, 0, 0, 0,
    P, P, P, P, P, P, P, P, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    p, p, p, p, p, p, p, p, 0, 0, 0, 0, 0, 0, 0, 0,
    r, n, b, q, k, b, n, r, 0, 0, 0, 0, 0, 0, 0, 0
]

ICONS = ["\u2003", "\u2659", "\u2658", "\u2657", "\u2656", "\u2655", "\u2654",
         "", "", "\u265f", "\u265e", "\u265d", "\u265c", "\u265b", "\u265a"]

# fmt: on

FILES = "abcdefgh"
LETTERS = " PNBRQK..pnbrqk"

ALL_PIECES = (0, P, N, B, R, Q, K, p, n, b, r, q, k)
PIECES_BY_COLOUR = [{B, K, N, P, Q, R}, {b, k, n, p, q, r}]

FW, LT, BW, RT = 16, 1, -16, -1

VALID_VECS = {
    B: (FW + LT, FW + RT, BW + LT, BW + RT),
    K: (FW, LT, BW, RT, FW + LT, FW + RT, BW + LT, BW + RT),
    N: (
        FW + FW + LT,
        FW + FW + RT,
        BW + BW + LT,
        BW + BW + RT,
        LT + LT + FW,
        LT + LT + BW,
        RT + RT + FW,
        RT + RT + BW,
    ),
    P: (FW, FW + LT, FW + RT),
    p: (BW, BW + LT, BW + RT),
    Q: (FW, LT, BW, RT, FW + LT, FW + RT, BW + LT, BW + RT),
    R: (FW, LT, BW, RT),
}

MASKS = {piece: 1 << (piece - 1) for piece in (P, N, B, R, Q, K, p)}

MOVE_TABLE = [0 for _ in range(239)]
CHEBYSHEV = [0 for _ in range(239)]

for i in range(1, 8):
    # sliding vertical/horizontal moves
    for v in VALID_VECS[R]:
        MOVE_TABLE[0x77 + i * v] = MASKS[Q] | MASKS[R]
        CHEBYSHEV[0x77 + i * v] = i

    # sliding diagonal moves
    for v in VALID_VECS[B]:
        MOVE_TABLE[0x77 + i * v] = MASKS[B] | MASKS[Q]
        CHEBYSHEV[0x77 + i * v] = i

for piece in (K, N, P, p):
    for v in VALID_VECS[piece]:
        MOVE_TABLE[0x77 + v] |= MASKS[piece]
