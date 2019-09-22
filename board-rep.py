board = [[0 for x in range(8)] for x in range(8)]

empty = 0

# white pieces
w_pawn = 1
w_knight = 3
w_bishop = 3
w_rook = 5
w_queen = 9
w_king = 1000000

# black pieces
b_pawn = -1
b_knight = -3
b_bishop = -3
b_rook = -5
b_queen = -9
b_king = -1000000

board[0] = [w_rook, w_knight, w_bishop, w_queen, w_king, w_bishop, w_knight,
            w_rook]

board[1] = [w_pawn for x in range(8)]

board[-1] = [b_rook, b_knight, b_bishop, b_queen, b_king, b_bishop, b_knight,
             b_rook]

board[-2] = [b_pawn for x in range(8)]
