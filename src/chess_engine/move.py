from chess_engine import attributes as attrs


class Move:
    def __init__(
        self,
        start,
        destination,
        piece_type,
        capture=False,
        castling=None,
        promotion=None,
    ):
        self.start = start
        self.destination = destination
        self.piece_type = piece_type
        self.capture = capture
        self.castling = castling
        self.promotion = promotion

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.destination == other.destination
            and self.piece_type == other.piece_type
            and self.capture == other.capture
            and self.castling == other.castling
            and self.promotion == other.promotion
        )

    def can_move_to_square(self, colour):
        direction = self.destination[0] - self.start[0]
        distance = (abs(direction), abs(self.destination[1] - self.start[1]))

        for v in self.piece_type.move_set:
            if self.piece_type.scale:
                check = [False, False]

                if v == (1, 0):
                    check[0] = distance[0] % v[0] == 0 and distance[0] > 0
                    check[1] = distance[1] == 0
                elif v == (0, 1):
                    check[0] = distance[0] == 0
                    check[1] = distance[1] % v[1] == 0 and distance[1] > 0
                else:
                    if distance[0] == distance[1] and distance[0] > 0:
                        check = [True, True]

                if all(check):
                    return True

            elif distance == v:
                if self.piece_type.symbol in ("n", "k"):
                    return True

                invalid = [
                    self.capture and v != (1, 1),
                    not self.capture and v == (1, 1),
                    v == (2, 0) and self.start[0] not in (1, 6),  # TODO: fix this
                    direction < 0 and colour == attrs.Colour.WHITE,
                    direction > 0 and colour == attrs.Colour.BLACK,
                ]

                if not any(invalid):
                    return True

        return False

    def is_blocked(self, board):
        if board.array[self.destination[0]][self.destination[1]] and not self.capture:
            return True

        if self.piece_type.symbol != "n":
            intermediate = [self.start[0], self.start[1]]

            while (intermediate[0], intermediate[1]) != self.destination:
                for i in range(0, 2):
                    if intermediate[i] < self.destination[i]:
                        intermediate[i] += 1

                    elif intermediate[i] > self.destination[i]:
                        intermediate -= 1

                square = board.array[intermediate[0]][intermediate[1]]

                if square is not None and square.position != self.destination:
                    return True

        return False

    def valid_capture(self, board):
        piece = board.array[self.start[0]][self.start[1]]
        to_capture = board.array[self.destination[0]][self.destination[1]]

        if to_capture is None:
            if piece.symbol != "p":
                return False

            # check if the capture is an en passant capture
            off = -1 if piece.colour == attrs.Colour.WHITE else 1
            en_passant_piece = board.array[self.destination[0] + off][
                self.destination[1]
            ]

            if en_passant_piece is None or en_passant_piece.colour == piece.colour:
                return False

        elif to_capture.colour == piece.colour:
            return False

        return True

    def pseudo_legal(self, board):
        """Checks if the move is valid without considering the check status."""
        piece = board.array[self.start[0]][self.start[1]]

        if piece is None or board.side_to_move != piece.colour:
            return False

        if self.castling:
            files = [1, 2, 3] if self.castling == attrs.Castling.QUEEN_SIDE else [5, 6]
            rank = 0 if piece.colour == attrs.Colour.WHITE else 7

            for file in files:
                if board.array[rank][file]:
                    return False

            return True

        if self.is_blocked(board) or not self.can_move_to_square(board.side_to_move):
            return False

        if self.capture:
            return self.valid_capture(board)

        return True

    def update_en_passant(self, board):
        for shift in (1, -1):
            if self.destination[1] + shift in range(8):
                pawn = board.array[self.destination[0]][self.destination[1] + shift]
                if (
                    pawn is not None
                    and pawn.symbol == "p"
                    and pawn.colour != board.side_to_move
                ):
                    return self.destination[1]
        return -1

    def update_castling_rights(self, board, piece, cap_piece=None):
        c_off = 0 if piece.colour == attrs.Colour.WHITE else 2

        if (
            cap_piece is not None
            and cap_piece.symbol == "p"
            and cap_piece.move_count == 0
        ):
            c_type = 0 if cap_piece.position[1] == 0 else 1
            board.castling_rights[c_off + c_type] = False

        indices = [0, 1] if piece.colour == attrs.Colour.WHITE else [2, 3]

        if self.castling:
            board.castling_rights[indices[0]] = False
            board.castling_rights[indices[1]] = False

        elif piece.move_count == 1:
            if piece.symbol == "k":
                board.castling_rights[c_off] = False
                board.castling_rights[c_off + 1] = False

        elif piece.symbol == "r":
            c_type = 0 if cap_piece.position[1] == 0 else 1
            board.castling_rights[c_off + c_type] = False

    def make_move(self, board):
        """Carries out a pseudo-legal move and updates the board state."""
        if not self.pseudo_legal(board):
            raise ValueError

        piece = board.array[self.start[0]][self.start[1]]

        # removing piece from its original position
        board.array[self.start[0]][self.start[1]] = None

        if self.capture:
            captured_piece = board.array[self.destination[0]][self.destination[1]]

            if captured_piece is None:  # en passant capture
                shift = -1 if piece.colour == attrs.Colour.WHITE else 1
                captured_piece = board.array[self.destination[0] + shift][
                    self.destination[1]
                ]
                board.array[self.destination[0] + shift][self.destination[1]] = None

            else:
                board.array[self.destination[0]][self.destination[1]] = None

            board.captured_pieces.append(captured_piece)

        if self.promotion:
            board.array[self.destination[0]][self.destination[1]] = self.promotion(
                piece.colour, self.destination
            )

        elif self.castling:
            rook_rank = 0 if piece.colour == attrs.Colour.WHITE else 7
            rook_file = 0 if self.castling == attrs.Castling.QUEEN_SIDE else 7
            new_file = 0 if self.castling == attrs.Castling.QUEEN_SIDE else 5

            rook = board.array[rook_rank][rook_file]
            board.array[rook_rank][rook_file] = None
            board.array[rook_rank][new_file] = rook

            rook.position = (rook_rank, new_file)
            rook.move_count += 1

            board.array[self.destination[0]][self.destination[1]] = piece
            piece.position = self.destination
            piece.move_count += 1

        else:
            board.array[self.destination[0]][self.destination[1]] = piece
            piece.position = self.destination
            piece.move_count += 1

        self.update_castling_rights(board, piece, cap_piece=captured_piece)
        board.half_move_clock += 1

        en_passant_conditions = [
            piece.symbol == "p",
            piece.move_count == 1,
            abs(self.destination[0] - self.start[0]) == 2,
        ]

        if all(en_passant_conditions):
            board.en_passant_file = self.update_en_passant(board)

        if board.side_to_move == attrs.Colour.WHITE:
            board.side_to_move = attrs.Colour.BLACK
        else:
            board.side_to_move = attrs.Colour.WHITE

    def unmake_castle(self, board, piece):
        c_off = 0 if piece.colour == attrs.Colour.WHITE else 2

        rook_rank = 0 if piece.colour == attrs.Colour.WHITE else 7
        rook_file = 3 if self.castling == attrs.Castling.QUEEN_SIDE else 5
        new_file = 0 if self.castling == attrs.Castling.QUEEN_SIDE else 7

        rook = board.array[rook_rank][rook_file]
        other_rook = board.array[rook_rank][7 - new_file]

        if (
            other_rook is not None
            and other_rook.symbol == "r"
            and other_rook.move_count == 0
        ):
            board.castling_rights[c_off] = True
            board.castling_rights[c_off + 1] = True
        else:
            c_type = 0 if self.castling == attrs.Castling.QUEEN_SIDE else 1
            board.castling_rights[c_off + c_type] = True

        board.array[rook_rank][rook_file] = None
        board.array[rook_rank][new_file] = rook
        rook.position = (rook_rank, new_file)
        rook.move_count -= 1

        board.array[self.start[0]][self.start[1]] = piece
        piece.position = self.start
        piece.move_count -= 1

    def unmake_move(self, board):
        """Reverses a move and any changes to the board state."""

        def piece_check(p, s, n):
            return p is not None and p.symbol == s and p.move_count == n

        if board.side_to_move == attrs.Colour.WHITE:
            board.side_to_move = attrs.Colour.BLACK
        else:
            board.side_to_move = attrs.Colour.WHITE

        board.half_move_clock -= 1
        board.en_passant_file = -1

        piece = board.array[self.destination[0]][self.destination[1]]
        board.array[self.destination[0]][self.destination[1]] = None

        if board.side_to_move == attrs.Colour.WHITE:
            first_rank = 0
            c_off = 0
        else:
            first_rank = 7
            c_off = 2

        if self.castling:
            self.unmake_castle(board, piece)

        else:
            # restore any castling rights lost from king or rook moves
            if piece.symbol == "k" and piece.move_count == 1:
                if piece_check(board.array[first_rank][0], "r", 0):
                    board.castling_rights[c_off] = True

                if piece_check(board.array[first_rank][7], "r", 0):
                    board.castling_rights[c_off + 1] = True

            elif piece.symbol == "r" and piece.move_count == 1:
                if piece_check(board.array[first_rank][4], "k", 0):
                    c_type = 0 if self.start[1] == 0 else 1
                    board.castling_rights[c_off + c_type] = True

            if self.capture:
                captured = board.captured_pieces[-1]
                board.array[captured.position[0]][captured.position[1]] = captured

                # restore castling rights for captured rook
                if piece_check(captured, "r", 0) and piece.move_count == 1:
                    if piece_check(board.array[7 - first_rank][4], "k", 0):
                        c_type = 0 if captured.position[1] == 0 else 1
                        board.castling_rights[2 - c_off][c_type] = True

                board.captured_pieces.remove(captured)

            # restore file of possible en passant capture
            board.en_passant_file = -1
            en_passant_rank = 4 if piece.colour == attrs.Colour.WHITE else 3

            for i, p in enumerate(board.array[en_passant_rank]):
                if (
                    p is not None
                    and piece_check(piece, "p", 1)
                    and p.colour != piece.colour
                ):
                    board.en_passant_file = i
                    break

            board.array[self.start[0]][self.start[1]] = piece
            piece.position = self.start
            piece.move_count -= 1

    def legal(self, board):
        """Checks if a pseudo-legal move leaves the king in check."""
        if not self.pseudo_legal(board):
            return False

        piece = board.array[self.start[0]][self.start[1]]

        if self.castling:
            files = (
                [2, 3, 4] if self.castling == attrs.Castling.QUEEN_SIDE else [4, 5, 6]
            )

            if piece.colour == attrs.Colour.WHITE:
                rank = 0
                board.side_to_move = attrs.Colour.BLACK
            else:
                rank = 7
                board.side_to_move = attrs.Colour.WHITE

            for row in board.array:
                for enemy_piece in row:
                    if enemy_piece:
                        if enemy_piece.colour != piece.colour:
                            for file in files:
                                threat = Move(
                                    enemy_piece.position,
                                    (rank, file),
                                    type(enemy_piece),
                                    capture=(file == 4),
                                )
                                if threat.pseudo_legal(board):
                                    self.board.side_to_move = self.piece.colour
                                    return False

            board.side_to_move = piece.colour
            return True

        self.make_move(board)

        index_1 = 0 if piece.colour == attrs.Colour.WHITE else 7
        index_2 = 7 - index_1
        step = 1 if index_2 > index_1 else -1

        for i in range(index_1, index_2 + step, step):
            for piece in board.array[i]:
                if piece:
                    if piece.symbol == "k" and piece.colour == piece.colour:
                        king = piece
                        break

        for i in range(index_2, index_1 - step, -step):
            for enemy_piece in board.array[i]:
                if enemy_piece:
                    if enemy_piece.colour != piece.colour:
                        threat = Move(
                            enemy_piece.position,
                            king.position,
                            type(enemy_piece),
                            capture=True,
                        )
                        if threat.pseudo_legal(board):
                            self.unmake_move(board)
                            return False

        self.unmake_move(board)
        return True
