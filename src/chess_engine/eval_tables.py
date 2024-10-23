"""Module containing evaluation tables for engine."""

import numpy as np

from chess_engine import constants as cs


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
    cs.BISHOP: B_ARR,
    cs.KING: K_ARR,
    cs.KNIGHT: N_ARR,
    cs.PAWN: P_ARR,
    cs.QUEEN: Q_ARR,
    cs.ROOK: R_ARR,
}

PIECE_VALS = {
    cs.BISHOP: 3,
    cs.KING: 10000000,
    cs.KNIGHT: 3,
    cs.PAWN: 1,
    cs.QUEEN: 9,
    cs.ROOK: 5,
}
