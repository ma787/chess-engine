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
            piece_to_capture = board.array[self.destination[0]][self.destination[1]]

            if not piece_to_capture:
                offset = -1 if piece.colour == attrs.Colour.WHITE else 1
                en_passant_piece = board.array[self.destination[0] + offset][
                    self.destination[1]
                ]

                if not en_passant_piece:
                    return False

                if en_passant_piece.colour == piece.colour:
                    return False

            elif piece_to_capture.colour == piece.colour:
                return False

        return True

    def make_move(self, board):
        """Carries out a pseudo-legal move and updates the board state."""
        if not self.pseudo_legal(board):
            return

        piece = board.array[self.start[0]][self.start[1]]

        board.array[self.start[0]][self.start[1]] = None

        if self.capture:
            captured_piece = board.array[self.destination[0]][self.destination[1]]

            if not captured_piece:  # en passant capture
                offset = -1 if piece.colour == attrs.Colour.WHITE else 1
                captured_piece = board.array[self.destination[0] + offset][
                    self.destination[1]
                ]
                board.array[self.destination[0] + offset][self.destination[1]] = None

            elif captured_piece.symbol == "r" and captured_piece.move_count == 0:
                colour = 0 if captured_piece.colour == attrs.Colour.WHITE else 2
                castle = 0 if captured_piece.position[1] == 0 else 1
                board.castling_rights[colour + castle] = False
                board.array[self.destination[0]][self.destination[1]] = None
            else:
                board.array[self.destination[0]][self.destination[1]] = None

            board.captured_pieces.append(captured_piece)

        if self.promotion:
            board.array[self.destination[0]][self.destination[1]] = self.promotion(
                piece.colour, self.destination
            )

        elif self.castling:
            if piece.colour == attrs.Colour.WHITE:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = board.array[0][0]
                    rook_destination = (0, 3)
                else:
                    rook = board.array[0][7]
                    rook_destination = (0, 5)

                board.castling_rights[0] = False
                board.castling_rights[1] = False

            else:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = board.array[7][0]
                    rook_destination = (7, 3)
                else:
                    rook = board.array[7][7]
                    rook_destination = (7, 5)

                board.castling_rights[2] = False
                board.castling_rights[3] = False

            board.array[rook.position[0]][rook.position[1]] = None
            board.array[rook_destination[0]][rook_destination[1]] = rook

            rook.position = rook_destination
            rook.move_count += 1

            board.array[self.destination[0]][self.destination[1]] = piece
            piece.position = self.destination
            piece.move_count += 1

        else:
            board.array[self.destination[0]][self.destination[1]] = piece
            piece.position = self.destination
            piece.move_count += 1

            index = 0 if piece.colour == attrs.Colour.WHITE else 2

            if piece.move_count == 1:
                if piece.symbol == "k":
                    board.castling_rights[index] = False
                    board.castling_rights[index + 1] = False

                elif piece.symbol == "r":
                    castle = 0 if piece.position[1] == 0 else 1
                    board.castling_rights[index + castle] = False

        board.half_move_clock += 1
        en_passant = -1

        if piece.symbol == "p" and piece.move_count == 1:
            if abs(self.destination[0] - self.start[0]) == 2:
                for shift in (1, -1):
                    if self.destination[1] + shift in range(8):
                        enemy_pawn = board.array[self.destination[0]][
                            self.destination[1] + shift
                        ]
                        if enemy_pawn:
                            if (
                                enemy_pawn.symbol == "p"
                                and enemy_pawn.colour != piece.colour
                            ):
                                en_passant = self.destination[1]

        # en passant capture is only possible immediately after a pawn advances two squares in one move
        board.en_passant_file = en_passant

        if board.side_to_move == attrs.Colour.WHITE:
            board.side_to_move = attrs.Colour.BLACK
        else:
            board.side_to_move = attrs.Colour.WHITE

    def unmake_move(self, board):
        """Reverses a move and any changes to the board state."""
        if board.side_to_move == attrs.Colour.WHITE:
            board.side_to_move = attrs.Colour.BLACK
        else:
            board.side_to_move = attrs.Colour.WHITE

        board.half_move_clock -= 1
        board.en_passant_file = -1

        piece = board.array[self.destination[0]][self.destination[1]]
        board.array[self.destination[0]][self.destination[1]] = None

        if self.castling:
            if piece.colour == attrs.Colour.WHITE:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = board.array[0][3]
                    rook_destination = (0, 0)
                    board.castling_rights[0] = True
                else:
                    rook = board.array[0][5]
                    rook_destination = (0, 7)
                    board.castling_rights[1] = True
            else:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = board.array[7][3]
                    rook_destination = (7, 0)
                    board.castling_rights[2] = True
                else:
                    rook = board.array[7][5]
                    rook_destination = (7, 7)
                    board.castling_rights[3] = True

            board.array[rook_destination[0]][rook_destination[1]] = rook
            board.array[rook.position[0]][rook.position[1]] = None
            rook.position = rook_destination
            rook.move_count -= 1

            other_rook = board.array[rook_destination[0]][7 - rook_destination[1]]
            offset = int(self.castling == attrs.Castling.QUEEN_SIDE)
            index = 0 if piece.colour == attrs.Colour.WHITE else 2

            if other_rook:
                if other_rook.move_count == 0:
                    board.castling_rights[index + offset] = True

            board.array[self.start[0]][self.start[1]] = piece
            piece.position = self.start
            piece.move_count -= 1

        else:
            if piece.colour == attrs.Colour.WHITE:
                index = 0
                rank = 0
            else:
                index = 2
                rank = 7

            if piece.symbol == "k":
                if piece.move_count == 1:
                    r_queen = board.array[rank][0]
                    r_king = board.array[rank][7]

                    for i, r in enumerate((r_queen, r_king)):
                        if r:
                            if r.symbol == "r" and r.move_count == 0:
                                board.castling_rights[index + i] = True

            elif piece.symbol == "r":
                king = board.array[rank][4]

                if king:
                    if king.symbol == "k" and king.move_count == 0:
                        if piece.move_count == 1:
                            castle = 0 if self.start[1] == 0 else 1
                            board.castling_rights[index + castle] = True

            if self.capture:
                captured = board.captured_pieces[-1]
                board.array[captured.position[0]][captured.position[1]] = captured

                if (
                    captured.symbol == "r" and captured.move_count == 0
                ):  # restore castling rights for captured rook
                    king = board.array[captured.position[0]][4]

                    if king:
                        if king.symbol == "k" and king.move_count == 0:
                            castle = 0 if captured.position[1] == 0 else 1
                            r_index = 2 if index == 0 else 0
                            board.castling_rights[r_index + castle] = True

                board.captured_pieces.remove(captured)

            board.en_passant_file = -1
            en_passant_rank = 4 if piece.colour == attrs.Colour.WHITE else 3

            for i, p in enumerate(board.array[en_passant_rank]):
                if p:
                    conditions = [
                        p.symbol == "p",
                        p.colour != piece.colour,
                        p.move_count == 1,
                    ]
                    if all(conditions):
                        board.en_passant_file = (
                            i  # restore file of possible en passant capture
                        )

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
