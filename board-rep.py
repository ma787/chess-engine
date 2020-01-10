board = [0 for x in range(120)]
illegal = 88

for x in range(20):
    board[x] = illegal

for y in range(100, 120):
    board[y] = illegal

n = 20
while n < 100:
    board[n] = illegal
    board[n + 9] = illegal
    n += 10

# 4 buffer rows and 2 buffer columns made to avoid off-board moves

pieces = {
    "pa": 1,
    "bi": 3,
    "kn": 3,
    "ro": 5,
    "qu": 9,
    "ki": 100000000
}  # piece values

U = 10
D = -10
R = 1
L = -1

moves = {
    "pa": (U, U + U, U + R, U + L ),
    "bi": (U + R, U + L, D + R, D + L),
    "kn": (U + U + R, U + U + L, D + D + R, D + D + L),
    "ro": (U, D, R, L),
    "qu": (U, D, R, L, U + R, U + L, D + R, D + L),
    "ki": (U, D, R, L, U + R, U + L, D + R, D + L)
}

# possible moves for all pieces

letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
digits = list(range(1, 9))
ranks = dict(zip(letters, digits))

tens = [20, 30, 40, 50, 60, 70, 80, 90]
digit_strings = [str(x) for x in digits]
files = dict(zip(tens, digit_strings))

# encodes standard chess position references (e.g. "e1") to the array index
