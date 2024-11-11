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

MOVE_TABLE = [0 for _ in range(239)]
UNIT_VEC = [0 for _ in range(239)]


# contact check masks
CONTACT_MASKS = {piece: 1 << (piece - 1) for piece in ALL_PIECES[1:]}

for v in VALID_VECS[R]:
    MOVE_TABLE[0x77 + v] = (
        CONTACT_MASKS[R]
        | CONTACT_MASKS[Q]
        | CONTACT_MASKS[K]
        | CONTACT_MASKS[r]
        | CONTACT_MASKS[q]
        | CONTACT_MASKS[k]
    )
    UNIT_VEC[0x77 + v] = v

for v in VALID_VECS[B]:
    MOVE_TABLE[0x77 + v] = (
        CONTACT_MASKS[B]
        | CONTACT_MASKS[Q]
        | CONTACT_MASKS[K]
        | CONTACT_MASKS[b]
        | CONTACT_MASKS[q]
        | CONTACT_MASKS[k]
    )
    UNIT_VEC[0x77 + v] = v

for v in VALID_VECS[N]:
    MOVE_TABLE[0x77 + v] |= CONTACT_MASKS[N] | CONTACT_MASKS[n]
    UNIT_VEC[0x77 + v] = v

for pawn in (P, p):
    for v in VALID_VECS[pawn][1:]:
        MOVE_TABLE[0x77 + v] |= CONTACT_MASKS[pawn]

# distant check masks
DISTANT_MASKS = {piece: 1 << (max(ALL_PIECES) + piece - 1) for piece in ALL_PIECES[1:]}

for i in range(2, 8):
    for v in VALID_VECS[R]:
        MOVE_TABLE[0x77 + i * v] = (
            DISTANT_MASKS[Q] | DISTANT_MASKS[R] | DISTANT_MASKS[q] | DISTANT_MASKS[r]
        )
        UNIT_VEC[0x77 + i * v] = v

    for v in VALID_VECS[B]:
        MOVE_TABLE[0x77 + i * v] = (
            DISTANT_MASKS[B] | DISTANT_MASKS[Q] | DISTANT_MASKS[b] | DISTANT_MASKS[q]
        )
        UNIT_VEC[0x77 + i * v] = v
