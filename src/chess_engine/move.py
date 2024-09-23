"Module providing move making, unmaking and checking utilities."

from chess_engine import attributes as attrs


class Move:
    """A class representing the state associated with a move.

    Attributes:
        start (tuple): The coordinates of the piece on the board array.
        destination (tuple): The coordinates of the destination on the board array.
        capture (bool, optional): Indicates whether the move is a capture. Defaults
        to False.
        castling (Castling, optional): Indicates whether the move is a queenside or
        kingside castle (if it is a castle). Defaults to None.
        promotion (int, optional): The piece type to change the pawn to if the move
        is a promotion. Defaults to 0.
    """

    def __init__(
        self,
        start,
        destination,
        capture=False,
        castling=None,
        promotion=0,
    ):
        self.start = start
        self.destination = destination
        self.capture = capture
        self.castling = castling
        self.promotion = promotion

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.destination == other.destination
            and self.capture == other.capture
            and self.castling == other.castling
            and self.promotion == other.promotion
        )

    def can_move_to_square(self, p_type):
        """Checks if the piece can move to its destination with its moveset.

        Args:
            p_type (int): The piece to analyse.

        Returns:
            bool: True if the piece can move to the destination, and False otherwise.
        """
        direction = self.destination[0] - self.start[0]
        distance = (abs(direction), abs(self.destination[1] - self.start[1]))

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
            if self.capture:
                valid = distance == (1, 1)

            elif distance == (1, 0):
                valid = True

            elif distance == (2, 0):
                valid = self.start[0] in (1, 6)
            else:
                valid = False

            valid &= direction * p_type > 0

        if abs(p_type) == 5:  # queen
            valid = b_rule or r_rule

        if abs(p_type) == 6:  # rook
            valid = r_rule

        return valid

    def is_blocked(self, board, p_type):
        """Checks if a piece's path to its destination square is blocked.

        Args:
            p_type (int): The piece to analyse.
            board (Board): The board to analyse.

        Returns:
            bool: True if there is an occupied square in the piece's path,
            and False otherwise.
        """
        if board.array[self.destination[0]][self.destination[1]] and not self.capture:
            return True

        if abs(p_type) != 3:  # only knights may jump over other pieces
            pos = [self.start[0], self.start[1]]

            while (pos[0], pos[1]) != self.destination:
                for i in range(0, 2):
                    if pos[i] < self.destination[i]:
                        pos[i] += 1

                    elif pos[i] > self.destination[i]:
                        pos[i] -= 1

                square = board.array[pos[0]][pos[1]]

                if square != 0 and (pos[0], pos[1]) != self.destination:
                    return True

        return False

    @staticmethod
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
                abs(board.en_passant_square[1] - start[0]),
            )
            == (0, 1)
            and (
                abs(board.en_passant_square[0] - dest[0]),
                abs(board.en_passant_square[1] - dest[1]),
            )
            == (1, 0)
        )

    def pseudo_legal(self, board):
        """Checks if the move is valid without considering the check status.

        Args:
            board (Board): The board to analyse.

        Returns:
            bool: True if the move is pseudo-legal, and False otherwise.
        """
        piece = board.array[self.start[0]][self.start[1]]
        mul = -1 if board.black else 1
        final_rank = 0 if board.black else 7

        if piece * mul <= 0 or (self.promotion and self.destination[0] != final_rank):
            return False

        if self.castling:
            files = [1, 2, 3] if self.castling == attrs.Castling.QUEEN_SIDE else [5, 6]
            rank = 0 if piece > 0 else 7

            for file in files:
                if board.array[rank][file]:
                    return False

            return True

        if self.is_blocked(board, piece) or not self.can_move_to_square(piece):
            return False

        if self.capture:
            if Move.is_en_passant(board, self.start, self.destination):
                to_capture = board.array[board.en_passant_square[0]][
                    board.en_passant_square[1]
                ]
            else:
                to_capture = board.array[self.destination[0]][self.destination[1]]

            return to_capture * piece < 0

        return True

    def update_castling_rights(self, board, piece, cap_piece=0):
        """Updates the castling rights after a move.

        Args:
            board (Board): The board to analyse and update.
            piece (int): The piece that was moved.
            cap_piece (optional, int): The piece that was captured
            (if this move is a capture move). Defaults to 0.
        """
        c_off = 0 if piece > 0 else 2

        if abs(cap_piece) == 6 and self.destination[1] in (0, 7):
            c_type = 0 if self.destination[1] == 0 else 1
            board.remove_castling_rights(c_off + c_type)

        if self.castling or abs(piece) == 2:
            board.remove_castling_rights(c_off)
            board.remove_castling_rights(c_off + 1)

        if abs(piece) == 6 and self.start[1] in (0, 7):
            c_type = 0 if self.start[1] == 0 else 1
            board.remove_castling_rights(c_off + c_type)

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

    def make_move(self, board):
        """Carries out a pseudo-legal move and updates the board state.

        Args:
            board (Board): The board to update.

        Raises:
            ValueError: If the move is not pseudo-legal.
        """
        if not self.pseudo_legal(board):
            raise ValueError

        piece = board.array[self.start[0]][self.start[1]]

        captured_piece = 0
        is_en_passant = 0

        if self.capture:
            if (
                board.en_passant_square is not None
                and abs(piece) == 4
                and abs(self.destination[0] - board.en_passant_square[0]) == 1
                and self.destination[1] == board.en_passant_square[1]
            ):
                is_en_passant = 1
                captured_piece = board.array[board.en_passant_square[0]][
                    board.en_passant_square[1]
                ]
                Move.move_piece(board, board.en_passant_square, None)
            else:
                captured_piece = board.array[self.destination[0]][self.destination[1]]

        if self.castling:
            first_rank = 7 if board.black else 0
            files = (0, 3) if self.castling == attrs.Castling.QUEEN_SIDE else (7, 5)
            Move.move_piece(board, (first_rank, files[0]), (first_rank, files[1]))

        board.save_state(is_en_passant, abs(captured_piece))

        Move.move_piece(board, self.start, self.destination, promotion=self.promotion)
        self.update_castling_rights(board, piece, cap_piece=captured_piece)

        # mark new en passant square
        if (
            abs(piece) == 4
            and self.start[0] in (1, 6)
            and self.destination[0] in (3, 4)
        ):
            board.en_passant_square = self.destination
        else:
            board.en_passant_square = None

        if abs(piece) == 4 or self.capture:
            board.halfmove_clock = 0
        else:
            board.halfmove_clock += 1

        board.fullmove_num += 1
        board.switch_side()

    def unmake_move(self, board):
        """Reverses a move and any changes to the board state.

        Args:
            board (Board): The board to update.
        """
        board.switch_side()
        board.fullmove_num -= 1

        first_rank = 7 if board.black else 0

        if self.castling:
            files = (3, 0) if self.castling == attrs.Castling.QUEEN_SIDE else (5, 7)
            Move.move_piece(board, (first_rank, files[0]), (first_rank, files[1]))

        Move.move_piece(board, self.destination, self.start)
        prev_state = board.get_prev_state()

        if self.capture:
            p_type = prev_state[1]
            mul = 1 if board.black else -1

            if p_type:
                captured = p_type * mul
                rank = (
                    self.destination[0] - mul if prev_state[0] else self.destination[0]
                )
                board.array[rank][self.destination[1]] = captured

        board.castling_rights = prev_state[2]
        board.halfmove_clock = prev_state[4]

        if prev_state[3] & 8:
            board.en_passant_square = (3 if board.black else 4, prev_state[3] & 7)

    @staticmethod
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

        threat = Move(enemy_pos, dest, capture=capture).pseudo_legal(board)

        if switch:
            board.switch_side()

        return threat

    def legal(self, board):
        """Checks if a pseudo-legal move does not leave the king in check.

        Args:
            board (Board): The board to analyse.

        Returns:
            bool: True if the move is legal, and False otherwise.
        """
        if not self.pseudo_legal(board):
            return False

        side = board.black

        if self.castling:
            files = (
                [2, 3, 4] if self.castling == attrs.Castling.QUEEN_SIDE else [4, 5, 6]
            )
            first_rank = 7 if board.black else 0

            for i in range(8):
                for j in range(8):
                    for file in files:
                        if Move.find_threat(
                            board,
                            (i, j),
                            not board.black,
                            (first_rank, file),
                            file == 4,
                        ):
                            return False

            return True

        self.make_move(board)

        king_pos = board.find_king(side)

        for i in range(8):
            for j in range(8):
                if Move.find_threat(board, (i, j), board.black, king_pos, True):
                    self.unmake_move(board)
                    return False

        self.unmake_move(board)
        return True
