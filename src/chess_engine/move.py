"Module providing move making, unmaking and checking utilities."


def encode_move(start, dest, capture=False, castling=0, promotion=0):
    """Encodes the state associated with a move to an integer.

    Args:
        start (tuple): The coordinates of the starting position.
        dest (tuple): The coordinates of the destination.
        capture (bool, optional): Indicates whether the move is a capture. Defaults
            to False.
        castling (int, optional): Indicates if the move is a castle and if so,
            which type: 0 - none, 1 - kingside, 2 - queenside. Defaults to 0.
        promotion (int, optional): The piece type to change the pawn to if the move
            is a promotion. Defaults to 0.

    Returns:
        int: A number encoding the move state.
    """
    mv = start[0] << 13
    mv |= start[1] << 10
    mv |= dest[0] << 7
    mv |= dest[1] << 4

    info = 0

    if castling:
        info = 1 + castling
        return mv | info

    info |= int(capture) << 2

    if promotion:
        p_types = {1: 1, 3: 0, 5: 3, 6: 2}

        info |= int(promotion != 0) << 3
        info |= p_types[promotion]

    return mv | info


def get_info(mv):
    """Extracts the move state from the move integer.

    Args:
        mv (int): The move integer.

    Returns:
        list: A list of values associated with the move:
            [start, dest, capture, castling, promotion]
    """
    flags = mv & 0xF
    p_types = {0: 3, 1: 1, 2: 6, 3: 5}
    info = [(), (), 0, 0, 0]

    start = (mv & (0x3F << 10)) >> 10
    dest = (mv & 0x3F0) >> 4

    info[0] = ((start & 0x38) >> 3, start & 0x7)
    info[1] = ((dest & 0x38) >> 3, dest & 0x7)
    info[2] = bool(flags & 4)  # capture
    info[3] = flags - 1 if flags in (2, 3) else 0  # castling
    info[4] = 0 if not flags & 8 else p_types[flags & 3]  # promotion

    return info


def can_move_to_square(start, dest, capture, p_type):
    """Checks if the piece can move to its destination with its moveset.

    Args:
        p_type (int): The piece to analyse.

    Returns:
        bool: True if the piece can move to the destination, and False otherwise.
    """
    direction = dest[0] - start[0]
    distance = (abs(direction), abs(dest[1] - start[1]))

    b_rule = (distance[0] > 0) and (distance[0] == distance[1])
    r_rule = (distance[0] == 0) ^ (distance[1] == 0)
    scale = (distance[0] > 1) or (distance[1] > 1)

    valid = False

    if abs(p_type) == 1:  # bishop
        valid = b_rule

    if abs(p_type) == 2:  # king
        valid = (b_rule or r_rule) and not scale

    if abs(p_type) == 3:  # knight
        valid = distance in ((1, 2), (2, 1))

    if abs(p_type) == 4:  # pawn
        if capture:
            valid = distance == (1, 1)

        elif distance == (1, 0):
            valid = True

        elif distance == (2, 0):
            valid = start[0] in (1, 6)
        else:
            valid = False

        valid &= direction * p_type > 0

    if abs(p_type) == 5:  # queen
        valid = b_rule or r_rule

    if abs(p_type) == 6:  # rook
        valid = r_rule

    return valid


def is_blocked(board, start, dest, p_type):
    """Checks if a piece's path to its destination square is blocked.

    Args:
        p_type (int): The piece to analyse.
        board (Board): The board to analyse.

    Returns:
        bool: True if there is an occupied square in the piece's path,
        and False otherwise.
    """
    if abs(p_type) != 3:  # only knights may jump over other pieces
        pos = [start[0], start[1]]

        while (pos[0], pos[1]) != dest:
            for i in range(0, 2):
                if pos[i] < dest[i]:
                    pos[i] += 1

                elif pos[i] > dest[i]:
                    pos[i] -= 1

            square = board.array[pos[0]][pos[1]]

            if square != 0 and (pos[0], pos[1]) != dest:
                return True

    return False


def is_en_passant(board, start, dest):
    """Determines whether a move is an en passant capture.

    Args:
        board (Board): The board to analyse.
        start (tuple): The coordinates of the starting square.
        dest (tuple): The coordinates of the destination square.

    Returns:
        bool: True if the move is an en passant capture, and
        False otherwise.
    """
    piece = board.array[start[0]][start[1]]

    return (
        abs(piece) == 4
        and board.en_passant_square is not None
        and (
            abs(board.en_passant_square[0] - start[0]),
            abs(board.en_passant_square[1] - start[1]),
        )
        == (0, 1)
        and (
            abs(board.en_passant_square[0] - dest[0]),
            abs(board.en_passant_square[1] - dest[1]),
        )
        == (1, 0)
    )


def pseudo_legal(mv, board):
    """Checks if the move is valid without considering the check status.

    Args:
        board (Board): The board to analyse.

    Returns:
        bool: True if the move is pseudo-legal, and False otherwise.
    """
    [start, dest, capture, castling, promotion] = get_info(mv)

    piece = board.array[start[0]][start[1]]
    mul = -1 if board.black else 1
    final_rank = 0 if board.black else 7

    if piece * mul <= 0 or (promotion and dest[0] != final_rank):
        return False

    if castling:
        off = castling * (4 if not board.black else 1)

        if not board.castling_rights & off:
            return False

        files = [1, 2, 3] if castling == 2 else [5, 6]
        rank = 0 if piece > 0 else 7

        for file in files:
            if board.array[rank][file]:
                return False

        return True

    if is_blocked(board, start, dest, piece) or not can_move_to_square(
        start, dest, capture, piece
    ):
        return False

    if capture:
        if is_en_passant(board, start, dest):
            to_capture = board.array[board.en_passant_square[0]][
                board.en_passant_square[1]
            ]
        else:
            to_capture = board.array[dest[0]][dest[1]]

        return to_capture * piece < 0

    return board.array[dest[0]][dest[1]] * piece == 0


@staticmethod
def move_piece(board, start, dest, promotion=0):
    """Moves a piece to a square on the board (or removes it).

    Args:
        board (Board): The board to update.
        start (tuple): The coordinates of the starting square.
        dest (tuple): The coordinates of the destination square.
            The piece is removed if this is set to None.
        promotion (int, optional): The piece type to promote to,
            if the move is a promotion. Defaults to 0.
    """
    if promotion:
        piece = promotion * (-1 if board.black else 1)
    else:
        piece = board.array[start[0]][start[1]]

    board.array[start[0]][start[1]] = 0

    if dest:
        board.array[dest[0]][dest[1]] = piece


def make_move(mv, board):
    """Carries out a pseudo-legal move and updates the board state.

    Args:
        mv (int): The move integer.
        board (Board): The board to update.

    Raises:
        ValueError: If the move is not pseudo-legal.
    """
    if not pseudo_legal(mv, board):
        raise ValueError

    [start, dest, capture, castling, promotion] = get_info(mv)

    piece = board.array[start[0]][start[1]]

    captured_piece = 0
    is_ep = 0

    if capture:
        if is_en_passant(board, start, dest):
            is_ep = 1
            captured_piece = board.array[board.en_passant_square[0]][
                board.en_passant_square[1]
            ]
            move_piece(board, board.en_passant_square, None)
        else:
            captured_piece = board.array[dest[0]][dest[1]]

    if castling:
        first_rank = 7 if board.black else 0
        files = (0, 3) if castling == 2 else (7, 5)
        move_piece(board, (first_rank, files[0]), (first_rank, files[1]))

    board.save_state(is_ep, abs(captured_piece))
    move_piece(board, start, dest, promotion=promotion)

    # update castling rights
    c_off = 0 if piece > 0 else 2

    if abs(captured_piece) == 6 and dest[1] in (0, 7):
        c_type = 0 if dest[1] == 0 else 1
        board.remove_castling_rights(c_off + c_type)

    if castling or abs(piece) == 2:
        board.remove_castling_rights(c_off)
        board.remove_castling_rights(c_off + 1)

    if abs(piece) == 6 and start[1] in (0, 7):
        c_type = 0 if start[1] == 0 else 1
        board.remove_castling_rights(c_off + c_type)

    # mark new en passant square
    if abs(piece) == 4 and start[0] in (1, 6) and dest[0] in (3, 4):
        board.en_passant_square = dest
    else:
        board.en_passant_square = None

    if abs(piece) == 4 or capture:
        board.halfmove_clock = 0
    else:
        board.halfmove_clock += 1

    board.fullmove_num += 1
    board.switch_side()


def unmake_move(mv, board):
    """Reverses a move and any changes to the board state.

    Args:
        mv (int): The move integer.
        board (Board): The board to update.
    """
    [start, dest, capture, castling, promotion] = get_info(mv)

    board.switch_side()
    board.fullmove_num -= 1

    first_rank = 7 if board.black else 0
    mul = -1 if board.black else 1

    if castling:
        files = (3, 0) if castling == 2 else (5, 7)
        move_piece(board, (first_rank, files[0]), (first_rank, files[1]))

    move_piece(board, dest, start)
    prev_state = board.get_prev_state()

    if promotion:
        board.array[start[0]][start[1]] = 4 * mul

    if capture:
        p_type = prev_state[1]

        if p_type:
            captured = p_type * -mul
            rank = dest[0] - mul if prev_state[0] else dest[0]
            board.array[rank][dest[1]] = captured

    board.castling_rights = prev_state[2]
    board.halfmove_clock = prev_state[4]

    if prev_state[3] & 8:
        board.en_passant_square = (3 if board.black else 4, prev_state[3] & 7)
    else:
        board.en_passant_square = None


def find_threat(board, enemy_pos, attacking_side, dest, capture):
    """Determines if a piece can attack another piece.

    Args:
        board (Board): The board to analyse.
        enemy_pos (tuple): The position of the piece that may be able to attack
            the position *dest*.
        attacking_side (Colour): The colour of the side attacking the position.
        dest (tuple): The position of the square that may be threatened by
            enemy_piece.
        capture (bool): Whether the move is a capture. Used to check pinning.

    Returns:
        bool: True if there is a pseudo-legal move where enemy_piece attacks
        the position dest, and False otherwise.
    """
    switch = False

    if board.black != attacking_side:
        switch = True
        board.switch_side()

    threat = pseudo_legal(encode_move(enemy_pos, dest, capture=capture), board)

    if switch:
        board.switch_side()

    return threat


def legal(mv, board):
    """Checks if a pseudo-legal move does not leave the king in check.

    Args:
        mv (int): The move integer.
        board (Board): The board to analyse.

    Returns:
        bool: True if the move is legal, and False otherwise.
    """
    [start, dest, _, castling, _] = get_info(mv)

    side = board.black

    if castling:
        files = [2, 3, 4] if castling == 2 else [4, 5, 6]
        first_rank = 7 if board.black else 0

        for i in range(8):
            for j in range(8):
                for file in files:
                    if find_threat(
                        board,
                        (i, j),
                        not board.black,
                        (first_rank, file),
                        file == 4,
                    ):
                        return False

        return pseudo_legal(encode_move(start, dest, castling=castling), board)

    try:
        make_move(mv, board)
    except ValueError:
        return False

    king_pos = board.find_king(side)

    for i in range(8):
        for j in range(8):
            if find_threat(board, (i, j), board.black, king_pos, True):
                unmake_move(mv, board)
                return False

    unmake_move(mv, board)
    return True
