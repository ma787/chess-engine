board = [[0 for x in range(12)] for x in range(12)]
boundary = (0, 1, 10, 11)

for i, row in enumerate(board):
    if i in boundary:
        board[i] = ["-" for n in range(12)]
    else:
        for point in boundary:
            row[point] = "-"

for x in board:
    print(x)

