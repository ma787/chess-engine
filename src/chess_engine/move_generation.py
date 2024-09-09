from chess_engine import attributes as attrs, move, pieces


def in_check(board):
    """Searches for a pseudo-legal move that allows the opposition to take the king of the side to move."""
    original_side = board.side_to_move
    index_1 = 0 if board.side_to_move == attrs.Colour.WHITE else 7
    index_2 = 7 - index_1
    step = 1 if index_2 > index_1 else -1

    for i in range(index_1, index_2 + step, step):
        for piece in board.array[i]:
            if piece:
                if piece.symbol == "k" and piece.colour == board.side_to_move:
                    king = piece
                    break

    for i in range(index_2, index_1 - step, -step):
        for j in range(0, 8):
            enemy_piece = board.array[i][j]

            if enemy_piece:
                if enemy_piece.colour != board.side_to_move:
                    threat = move.Move(
                        enemy_piece,
                        board,
                        enemy_piece.position,
                        king.position,
                        capture=True,
                    )
                    board.side_to_move = enemy_piece.colour

                    if threat.pseudo_legal():
                        board.side_to_move = original_side
                        return True
                    else:
                        board.side_to_move = original_side

    return False


def all_moves_from_position(board, position):
    """Finds all the possible legal moves that can be made by a piece at a given position."""
    all_moves = []
    piece = board.array[position[0]][position[1]]

    if not piece:
        return all_moves

    if piece.colour != board.side_to_move:
        return all_moves

    for i, row in enumerate(board.array):
        for j, _ in enumerate(row):
            dest_square = board.array[i][j]
            valid = True
            capture = False
            promotion = None

            if dest_square:
                if dest_square.colour != piece.colour:
                    capture = True
                else:
                    valid = False
            else:
                if piece.symbol == "p":
                    shift = 1 if piece.colour == attrs.Colour.BLACK else -1

                    if j + shift in range(8):
                        pawn = board.array[i][j + shift]

                        if pawn:
                            conditions = [
                                pawn.symbol == "p",
                                pawn.move_count == 1,
                                i in (3, 4),
                                pawn.colour != piece.colour,
                            ]

                            if all(conditions):
                                capture = True

                    final_rank = 0 if piece.colour == attrs.Colour.BLACK else 7

                    if j == final_rank:
                        promotion = pieces.Queen

            if valid:
                move_obj = move.Move(
                    piece, board, position, (i, j), capture=capture, promotion=promotion
                )
                if move_obj.legal():
                    all_moves.append(move_obj)

        if piece.symbol == "k":
            start_rank = 0 if piece.colour == attrs.Colour.WHITE else 7

            if piece.position == (start_rank, 4):
                files = (2, 4)
                offset = 2 if start_rank == 7 else 0

                for k, file in enumerate(files):
                    if board.castling_rights[k + offset]:
                        castle = (
                            attrs.Castling.QUEEN_SIDE
                            if k % 2 == 0
                            else attrs.Castling.KING_SIDE
                        )
                        castle_move = move.Move(
                            piece, board, position, (start_rank, file), castling=castle
                        )
                        if castle_move.legal():
                            all_moves.append(castle_move)

    return all_moves


def all_possible_moves(board):
    """Finds all the possible legal moves that the side to move can make."""
    all_moves = []

    for i in range(8):
        for j in range(8):
            square = board.array[i][j]
            if square:
                if board.side_to_move == square.colour:
                    all_moves.extend(all_moves_from_position(board, square.position))

    return all_moves
