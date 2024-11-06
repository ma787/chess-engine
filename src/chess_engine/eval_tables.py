"""Module containing evaluation tables for engine."""

from chess_engine import constants as cs


WB_ARR = [0 for _ in range(128)]
WB_ARR[0:8] = [-20, -10, -10, -10, -10, -10, -10, -20]
WB_ARR[16:24] = [-10, 5, 0, 0, 0, 0, 5, -10]
WB_ARR[32:40] = [-10, 10, 10, 10, 10, 10, 10, -10]
WB_ARR[48:56] = [-10, 0, 10, 10, 10, 10, 0, -10]
WB_ARR[64:72] = [-10, 5, 5, 10, 10, 5, 5, -10]
WB_ARR[80:88] = [-10, 0, 5, 10, 10, 5, 0, -10]
WB_ARR[96:104] = [-10, 0, 0, 0, 0, 0, 0, -10]
WB_ARR[112:120] = [-20, -10, -10, -10, -10, -10, -10, -20]

WK_ARR = [0 for _ in range(128)]
WK_ARR[0:8] = [20, 30, 10, 0, 0, 10, 30, 20]
WK_ARR[16:24] = [20, 20, 0, 0, 0, 0, 20, 20]
WK_ARR[32:40] = [-10, -20, -20, -20, -20, -20, -20, -10]
WK_ARR[48:56] = [-20, -30, -30, -40, -40, -30, -30, -20]
WK_ARR[64:72] = [-30, -40, -40, -50, -50, -40, -40, -30]
WK_ARR[80:88] = list(WK_ARR[64:72])
WK_ARR[96:104] = list(WK_ARR[64:72])
WK_ARR[112:120] = list(WK_ARR[64:72])

WK_END_ARR = [0 for _ in range(128)]
WK_END_ARR[0:8] = [-50, -30, -30, -30, -30, -30, -30, -50]
WK_END_ARR[16:24] = [-30, -30, 0, 0, 0, 0, -30, -30]
WK_END_ARR[32:40] = [-30, -10, 20, 30, 30, 20, -10, -30]
WK_END_ARR[48:56] = [-30, -10, 30, 40, 40, 30, -10, -30]
WK_END_ARR[64:72] = list(WK_END_ARR[48:56])
WK_END_ARR[80:88] = list(WK_END_ARR[32:40])
WK_END_ARR[96:104] = [-30, -20, -10, 0, 0, -10, -20, -30]
WK_END_ARR[112:120] = [-50, -40, -30, -20, -20, -30, -40, -50]

WN_ARR = [0 for _ in range(128)]
WN_ARR[0:8] = [-50, -40, -30, -30, -30, -30, -40, -50]
WN_ARR[16:24] = [-40, -20, 0, 5, 5, 0, -20, -40]
WN_ARR[32:40] = [-30, 5, 10, 15, 15, 10, 5, -30]
WN_ARR[48:56] = [-30, 0, 15, 20, 20, 15, 0, -30]
WN_ARR[64:72] = [-30, 5, 15, 20, 20, 15, 5, -30]
WN_ARR[80:88] = [-30, 0, 10, 15, 15, 10, 0, -30]
WN_ARR[96:104] = [-40, -20, 0, 0, 0, 0, -20, -40]
WN_ARR[112:120] = [-50, -40, -30, -30, -30, -30, -40, -50]

WP_ARR = [0 for _ in range(128)]
WP_ARR[16:24] = [5, 10, 10, -20, -20, 10, 10, 5]
WP_ARR[32:40] = [5, -5, -10, 0, 0, -10, -5, 5]
WP_ARR[48:56] = [0, 0, 0, 20, 20, 0, 0, 0]
WP_ARR[64:72] = [5, 5, 10, 25, 25, 10, 5, 5]
WP_ARR[80:88] = [10, 10, 20, 30, 30, 20, 10, 10]
WP_ARR[96:104] = [50, 50, 50, 50, 50, 50, 50, 50]

WQ_ARR = [0 for _ in range(128)]
WQ_ARR[0:8] = [-20, -10, -10, -5, -5, -10, -10, -20]
WQ_ARR[16:24] = [-10, 0, 5, 0, 0, 0, 0, -10]
WQ_ARR[32:40] = [-10, 5, 5, 5, 5, 5, 0, -10]
WQ_ARR[48:56] = [0, 0, 5, 5, 5, 5, 0, -5]
WQ_ARR[64:72] = [-5, 0, 5, 5, 5, 5, 0, -5]
WQ_ARR[80:88] = [-10, 0, 5, 5, 5, 5, 0, -10]
WQ_ARR[96:104] = [-10, 0, 0, 0, 0, 0, 0, -10]
WQ_ARR[112:120] = [-20, -10, -10, -5, -5, -10, -10, -20]

WR_ARR = [0 for _ in range(128)]
WR_ARR[0:8] = [0, 0, 0, 5, 5, 0, 0, 0]
WR_ARR[16:24] = [-5, 0, 0, 0, 0, 0, 0, -5]
WR_ARR[32:40] = list(WR_ARR[16:24])
WR_ARR[48:56] = list(WR_ARR[16:24])
WR_ARR[64:72] = list(WR_ARR[16:24])
WR_ARR[80:88] = list(WR_ARR[16:24])
WR_ARR[96:104] = [5, 10, 10, 10, 10, 10, 10, 5]

BB_ARR = [0 for _ in range(128)]
BK_ARR = [0 for _ in range(128)]
BK_END_ARR = [0 for _ in range(128)]
BN_ARR = [0 for _ in range(128)]
BP_ARR = [0 for _ in range(128)]
BQ_ARR = [0 for _ in range(128)]
BR_ARR = [0 for _ in range(128)]

for i in range(0x10, 0x80, 0x10):
    for j in range(0, 8):
        BB_ARR[0x70 - i + j] = WB_ARR[i + j]
        BK_ARR[0x70 - i + j] = WK_ARR[i + j]
        BK_END_ARR[0x70 - i + j] = WK_END_ARR[i + j]
        BN_ARR[0x70 - i + j] = WN_ARR[i + j]
        BP_ARR[0x70 - i + j] = WP_ARR[i + j]
        BQ_ARR[0x70 - i + j] = WQ_ARR[i + j]
        BR_ARR[0x70 - i + j] = WR_ARR[i + j]

P_SQUARE_VALS = {
    cs.B: WB_ARR,
    cs.K: WK_ARR,
    cs.N: WN_ARR,
    cs.P: WP_ARR,
    cs.Q: WQ_ARR,
    cs.R: WR_ARR,
    cs.b: BB_ARR,
    cs.k: BK_ARR,
    cs.n: BN_ARR,
    cs.p: BP_ARR,
    cs.q: BQ_ARR,
    cs.r: BR_ARR,
}

END_VALS = (WK_END_ARR, BK_END_ARR)

PIECE_VALS = {
    cs.B: 330,
    cs.K: 20000,
    cs.N: 320,
    cs.P: 100,
    cs.Q: 900,
    cs.R: 500,
}
