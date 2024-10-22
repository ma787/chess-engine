"Module containing project-wide constants."
import numpy as np


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

VALID_PAWN_VECTORS = {0: "N", 1: "S"}

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

B_ARR = np.zeros(128)
B_ARR[0:8] = np.array([-20, -10, -10, -10, -10, -10, -10, -20])
B_ARR[16:24] = np.array([-10, 0, 0, 0, 0, 0, 0, -10])
B_ARR[32:40] = np.array([-10, 0, 5, 10, 10, 5, 0, -10])
B_ARR[48:56] = np.array([-10, 5, 5, 10, 10, 5, 5, -10])
B_ARR[64:72] = np.array([-10, 0, 10, 10, 10, 10, 0, -10])
B_ARR[80:88] = np.array([-10, 10, 10, 10, 10, 10, 10, -10])
B_ARR[96:104] = np.array([-10, 5, 0, 0, 0, 0, 5, -10])
B_ARR[112:120] = np.array([-20, -10, -10, -10, -10, -10, -10, -20])

K_ARR = np.zeros(128)
K_ARR[0:8] = np.array([-30, -40, -40, -50, -50, -40, -40, -30])
K_ARR[16:24] = K_ARR[0:8]
K_ARR[32:40] = K_ARR[0:8]
K_ARR[48:56] = K_ARR[0:8]
K_ARR[64:72] = np.array([-20, -30, -30, -40, -40, -30, -30, -20])
K_ARR[80:88] = np.array([-10, -20, -20, -20, -20, -20, -20, -10])
K_ARR[96:104] = np.array([20, 20, 0, 0, 0, 0, 20, 20])
K_ARR[112:120] = np.array([20, 30, 10, 0, 0, 10, 30, 20])

N_ARR = np.zeros(128)
N_ARR[0:8] = np.array([-50, -40, -30, -30, -30, -30, -40, -50])
N_ARR[16:24] = np.array([-40, -20, 0, 0, 0, 0, -20, -40])
N_ARR[32:40] = np.array([-30, 0, 10, 15, 15, 10, 0, -30])
N_ARR[48:56] = np.array([-30, 5, 15, 20, 20, 15, 5, -30])
N_ARR[64:72] = np.array([-30, 0, 15, 20, 20, 15, 0, -30])
N_ARR[80:88] = np.array([-30, 5, 10, 15, 15, 10, 5, -30])
N_ARR[96:104] = np.array([-40, -20, 0, 5, 5, 0, -20, -40])
N_ARR[112:120] = np.array([-50, -40, -30, -30, -30, -30, -40, -50])

P_ARR = np.zeros(128)
P_ARR[16:24] = np.array([50, 50, 50, 50, 50, 50, 50, 50])
P_ARR[32:40] = np.array([10, 10, 20, 30, 30, 20, 10, 10])
P_ARR[48:56] = np.array([5, 5, 10, 25, 25, 10, 5, 5])
P_ARR[64:72] = np.array([0, 0, 0, 20, 20, 0, 0, 0])
P_ARR[80:88] = np.array([5, -5, -10, 0, 0, -10, -5, 5])
P_ARR[96:104] = np.array([5, 10, 10, -20, -20, 10, 10, 5])

Q_ARR = np.zeros(128)
Q_ARR[0:8] = np.array([-20, -10, -10, -5, -5, -10, -10, -20])
Q_ARR[16:24] = np.array([-10, 0, 0, 0, 0, 0, 0, -10])
Q_ARR[32:40] = np.array([-10, 0, 5, 5, 5, 5, 0, -10])
Q_ARR[48:56] = np.array([-5, 0, 5, 5, 5, 5, 0, -5])
Q_ARR[64:72] = np.array([0, 0, 5, 5, 5, 5, 0, -5])
Q_ARR[80:88] = np.array([-10, 5, 5, 5, 5, 5, 0, -10])
Q_ARR[96:104] = np.array([-10, 0, 5, 0, 0, 0, 0, -10])
Q_ARR[112:120] = np.array([-20, -10, -10, -5, -5, -10, -10, -20])

R_ARR = np.zeros(128)
R_ARR[16:24] = np.array([5, 10, 10, 10, 10, 10, 10, 5])
R_ARR[32:40] = np.array([-5, 0, 0, 0, 0, 0, 0, -5])
R_ARR[48:56] = R_ARR[32:40]
R_ARR[64:72] = R_ARR[32:40]
R_ARR[80:88] = R_ARR[32:40]
R_ARR[96:104] = R_ARR[32:40]
R_ARR[112:120] = np.array([0, 0, 0, 5, 5, 0, 0, 0])

SQUARE_VALS = {
    BISHOP: B_ARR,
    KING: K_ARR,
    KNIGHT: N_ARR,
    PAWN: P_ARR,
    QUEEN: Q_ARR,
    ROOK: R_ARR,
}

PIECE_VALS = {
    1: 3,
    2: 10000000,
    3: 3,
    4: 1,
    5: 9,
    6: 5,
}
