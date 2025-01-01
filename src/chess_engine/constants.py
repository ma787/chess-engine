"Module containing project-wide constants."

NAME = "Aether"
AUTHOR = "Mohamed Omar"

WHITE, BLACK = 0, 1
KINGSIDE, QUEENSIDE = 2, 3

P, p, N, B, R, Q, K = 1, 2, 3, 4, 5, 6, 7
PIECE_TYPES = (P, p, N, B, R, Q, K)
PAWNS = (P, p)

NL, GD, BVAL = 0, 2, 8  # empty square, border guard, colour code
WP, WN, WB, WR, WQ, WK = P, N, B, R, Q, K
BP, BN, BB, BR, BQ, BK = (
    (p + BVAL),
    (N + BVAL),
    (B + BVAL),
    (R + BVAL),
    (Q + BVAL),
    (K + BVAL),
)

# fmt: off
STARTING_ARRAY = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, 0, 0,
    0, 0, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, 0, 0,
    0, 0, GD, GD, WR, WN, WB, WQ, WK, WB, WN, WR, GD, GD, 0, 0,
    0, 0, GD, GD, WP, WP, WP, WP, WP, WP, WP, WP, GD, GD, 0, 0,
    0, 0, GD, GD, NL, NL, NL, NL, NL, NL, NL, NL, GD, GD, 0, 0,
    0, 0, GD, GD, NL, NL, NL, NL, NL, NL, NL, NL, GD, GD, 0, 0,
    0, 0, GD, GD, NL, NL, NL, NL, NL, NL, NL, NL, GD, GD, 0, 0,
    0, 0, GD, GD, NL, NL, NL, NL, NL, NL, NL, NL, GD, GD, 0, 0,
    0, 0, GD, GD, BP, BP, BP, BP, BP, BP, BP, BP, GD, GD, 0, 0,
    0, 0, GD, GD, BR, BN, BB, BQ, BK, BB, BN, BR, GD, GD, 0, 0,
    0, 0, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, 0, 0,
    0, 0, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, GD, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

STARTING_PIECE_LIST = [
    0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B,
    0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B,
    0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB,
    0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB,
]

for i, pos in enumerate(STARTING_PIECE_LIST):
    STARTING_ARRAY[pos] |= (i << 4)

SIDE_OFFSET = 16

A1 = 0x44
A8 = 0xB4

ICONS = ["\u2003", "\u2659", "\u2003", "\u2658", "\u2657", "\u2656", "\u2655",
         "\u2654", "\u2003", "\u2003", "\u265f", "\u265e", "\u265d", "\u265c", 
         "\u265b", "\u265a"]

# fmt: on

FILES = "abcdefgh"
LETTERS = " P.NBRQK..pnbrqk"

FW, LT, BW, RT = 16, 1, -16, -1

VALID_VECS = {
    P: (FW, FW + LT, FW + RT),
    p: (BW, BW + LT, BW + RT),
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
    Q: (FW, LT, BW, RT, FW + LT, FW + RT, BW + LT, BW + RT),
    R: (FW, LT, BW, RT),
}

MOVE_TABLE = [0 for _ in range(239)]
UNIT_VEC = [0 for _ in range(239)]

# check masks
CONTACT_MASKS = {pc: 1 << (pc - 1) for pc in PIECE_TYPES}
CONTACT_MASKS[0] = 0
DISTANT_MASKS = {pc: 1 << (K + pc - 1) for pc in PIECE_TYPES}

# setting contact masks
for p_type in (N, B, R, Q, K):
    for v in VALID_VECS[p_type]:
        MOVE_TABLE[0x77 + v] |= CONTACT_MASKS[p_type]
        UNIT_VEC[0x77 + v] = v

for pawn in (P, p):
    for v in VALID_VECS[pawn][1:]:
        MOVE_TABLE[0x77 + v] |= CONTACT_MASKS[pawn]

# setting distant masks
for i in range(2, 8):
    for v in VALID_VECS[R]:
        MOVE_TABLE[0x77 + i * v] = DISTANT_MASKS[Q] | DISTANT_MASKS[R]
        UNIT_VEC[0x77 + i * v] = v

    for v in VALID_VECS[B]:
        MOVE_TABLE[0x77 + i * v] = DISTANT_MASKS[B] | DISTANT_MASKS[Q]
        UNIT_VEC[0x77 + i * v] = v
