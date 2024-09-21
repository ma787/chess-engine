"Module providing functions to generate and validate moves."

from chess_engine import attributes as attrs, move, pieces


def in_check(board):
    """Searches for a pseudo-legal capture of the side to move's king.

    Args:
        board (Board): The board object to inspect.

    Returns:
        bool: True if a pseudo-legal move to capture the king exists,
        and False otherwise.
    """
    opposite_side = (
        attrs.Colour.WHITE
        if board.side_to_move == attrs.Colour.BLACK
        else attrs.Colour.BLACK
    )

    king = board.find_king(board.side_to_move)

    for i in range(8):
        for j in range(8):
            enemy_piece = board.array[i][j]

            if move.Move.find_threat(
                board, enemy_piece, opposite_side, king.position, capture=True
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
    king = board.find_king(board.side_to_move)

    if king.position[1] != 4:
        return moves

    c_off = 0 if board.side_to_move == attrs.Colour.WHITE else 2
    c_type = {-2: attrs.Castling.QUEEN_SIDE, 2: attrs.Castling.KING_SIDE}

    for i in range(0, 2):
        if board.get_castling_rights(c_off + i):
            for shift in (-2, 2):
                castle_move = move.Move(
                    king.position,
                    (king.position[0], king.position[1] + shift),
                    pieces.King,
                    c_type[shift],
                )

                if castle_move.legal(board):
                    moves.append(castle_move)

    return moves


def all_moves_from_position(board, position):
    """Finds all the possible legal moves that can be made by a piece at a given position.

    Args:
        board (Board): The board to analyse.
        position (tuple): The indices of the position to start from on the board
        array.

    Returns:
        list: A list of move objects consisting of every legal move
        starting from the given position on the board array.
    """
    all_moves = []
    piece = board.array[position[0]][position[1]]

    if piece is None or piece.colour != board.side_to_move:
        return all_moves

    for i, row in enumerate(board.array):
        final_rank = 7 if board.side_to_move == attrs.Colour.WHITE else 0
        promotion = pieces.Queen if i == final_rank else None

        for j, dest_square in enumerate(row):
            capture = dest_square is not None and dest_square.colour != piece.colour

            if (
                piece.symbol == "p"
                and board.en_passant_square is not None
                and (abs(position[0] - i), abs(position[1] - j)) == (1, 0)
            ):
                capture = True

            if dest_square is None or capture:
                move_obj = move.Move(
                    position, (i, j), type(piece), capture=capture, promotion=promotion
                )

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
