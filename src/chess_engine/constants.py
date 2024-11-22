"Module containing project-wide constants."

WHITE, BLACK = 0, 1
KINGSIDE, QUEENSIDE = 2, 3

P, p, N, B, R, Q, K = 1, 2, 3, 4, 5, 6, 7
bp, n, b, r, q, k = 10, 11, 12, 13, 14, 15

PIECE_TYPES = (P, p, N, B, R, Q, K)

# fmt: off
STARTING_ARRAY = [
    R, N, B, Q, K, B, N, R, 0, 0, 0, 0, 0, 0, 0, 0,
    P, P, P, P, P, P, P, P, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    bp, bp, bp, bp, bp, bp, bp, bp, 0, 0, 0, 0, 0, 0, 0, 0,
    r, n, b, q, k, b, n, r, 0, 0, 0, 0, 0, 0, 0, 0
]

for i in range(8):
    STARTING_ARRAY[0x60 + i] = p | (BLACK << 3)

STARTING_PIECE_LIST = [
    0, 1, 2, 3, 4, 5, 6, 7,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77,
    0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67,
]

for i, pos in enumerate(STARTING_PIECE_LIST):
    STARTING_ARRAY[pos] |= (i << 4)

SIDE_OFFSET = 16

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
