"Module providing functions to generate and validate moves."

from chess_engine import attributes as attrs, move


def in_check(board):
    """Searches for a pseudo-legal capture of the side to move's king.

    Args:
        board (Board): The board object to inspect.

    Returns:
        bool: True if a pseudo-legal move to capture the king exists,
        and False otherwise.
    """
    king_pos = board.find_king(board.black)

    for i in range(8):
        for j in range(8):
            if move.Move.find_threat(
                board, (i, j), not board.black, king_pos, capture=True
            ):
                return True

    return False


def all_castle_moves(board):
    """Finds all legal castle moves that can be made.

    Args:
        board (Board): The board to analyse.

    Returns:
        list: A list of legal castle moves that the side to move can make.
    """
    moves = []
    king_pos = board.find_king(board.black)

    if king_pos[1] != 4:
        return moves

    c_off = 2 if board.black else 0
    c_type = {-2: attrs.Castling.QUEEN_SIDE, 2: attrs.Castling.KING_SIDE}

    for i in range(0, 2):
        if board.get_castling_rights(c_off + i):
            for shift in (-2, 2):
                castle_move = move.Move(
                    king_pos,
                    (king_pos[0], king_pos[1] + shift),
                    c_type[shift],
                )

                if castle_move.legal(board):
                    moves.append(castle_move)

    return moves


def all_moves_from_position(board, pos):
    """Finds all the possible legal moves that can be made by a piece at a given position.

    Args:
        board (Board): The board to analyse.
        pos (tuple): The indices of the position to start from on the board
        array.

    Returns:
        list: A list of move objects consisting of every legal move
        starting from the given position on the board array.
    """
    all_moves = []
    piece = board.array[pos[0]][pos[1]]

    if not piece or piece > 0 and board.black or piece < 0 and not board.black:
        return all_moves

    for i, row in enumerate(board.array):
        final_rank = 0 if board.black else 7
        promotion = (-5 if board.black else 5) if i == final_rank else None

        for j, dest_square in enumerate(row):
            capture = dest_square * piece < 0

            if (
                abs(piece) == 4
                and board.en_passant_square is not None
                and (
                    abs(board.en_passant_square[0] - pos[0]),
                    abs(board.en_passant_square[1] - pos[1]),
                )
                == (0, 1)
                and (
                    abs(board.en_passant_square[0] - i),
                    abs(board.en_passant_square[1] - j),
                )
                == (1, 0)
            ):
                capture = True

            if dest_square == 0 or capture:
                move_obj = move.Move(pos, (i, j), capture=capture, promotion=promotion)

                if move_obj.legal(board):
                    all_moves.append(move_obj)

    if board.castling_rights:
        all_moves.extend(all_castle_moves(board))

    return all_moves


def all_possible_moves(board):
    """Finds all the possible legal moves that the side to move can make.

    Args:
        board (Board): The board to analyse.

    Returns:
        list: A list of move objects consisting of every legal move
        that the side to move can make.
    """
    all_moves = []

    for i in range(8):
        for j in range(8):
            all_moves.extend(all_moves_from_position(board, (i, j)))

    return all_moves


def perft(board, depth):
    """Returns the number of nodes at a given depth beginning from a position.

    Args:
        board (Board): The board position to begin the traversal from.
        depth (int): The depth at which the search should be halted.

    Returns:
        int: The number of nodes encountered at the search depth.
    """
    if depth == 0:
        return 1

    moves = all_possible_moves(board)
    nodes = 0

    for m in moves:
        m.make_move(board)
        nodes += perft(board, depth - 1)
        m.unmake_move(board)

    return nodes
