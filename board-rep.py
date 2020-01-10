board = [0 for x in range(120)]
illegal = 99

for x in range(20):
    board[x] = illegal

for y in range(100, 120):
    board[y] = illegal

n = 20
while n < 100:
    board[n] = illegal
    board[n + 9] = illegal
    n += 10

#  4 buffer rows and 2 buffer columns made to avoid off-board moves

n = 1
m = 0

while n <= 64:
    if board[m] == illegal:
        pass
    else:
        board[m] = n
        n += 1
    m += 1

#  squares on the board are numbered from 1-64
