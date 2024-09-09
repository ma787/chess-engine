from chess_engine import attributes as attrs


class Move:
    def __init__(
        self,
        piece,
        board,
        start,
        destination,
        capture=False,
        castling=None,
        promotion=None,
    ):
        self.piece = piece
        self.board = board
        self.start = start
        self.destination = destination
        self.distance = (abs(destination[0] - start[0]), abs(destination[1] - start[1]))
        self.capture = capture
        self.castling = castling
        self.promotion = promotion

    def __eq__(self, other):
        return (
            self.piece == other.piece
            and self.board == other.board
            and self.start == other.start
            and self.destination == other.destination
            and self.capture == other.capture
            and self.castling == other.castling
            and self.promotion == other.promotion
        )

    def pseudo_legal(self):
        """Checks if the move is valid without considering the check status."""
        if self.board.side_to_move != self.piece.colour:
            return False

        if self.castling:
            files = [1, 2, 3] if self.castling == attrs.Castling.QUEEN_SIDE else [5, 6]
            rank = 0 if self.piece.colour == attrs.Colour.WHITE else 7

            for file in files:
                if self.board.array[rank][file]:
                    return False

            return True

        can_move = False

        for v in self.piece.move_set:
            if self.piece.scale:
                check = [False, False]

                if v == (1, 0):
                    check[0] = self.distance[0] % v[0] == 0 and self.distance[0] > 0
                    check[1] = self.distance[1] == 0

                elif v == (0, 1):
                    check[0] = self.distance[0] == 0
                    check[1] = self.distance[1] % v[1] == 0 and self.distance[1] > 0
                else:
                    if self.distance[0] == self.distance[1] and self.distance[0] > 0:
                        check = [True, True]

                if all(check):
                    can_move = True
                    break

            elif self.distance == v:
                if self.piece.symbol in ("n", "k"):
                    can_move = True
                    break

                else:
                    rank = 7 if self.piece.colour == attrs.Colour.WHITE else 0

                    if self.promotion and self.destination[0] != rank:
                        return False

                    direction = self.destination[0] - self.start[0]

                    if direction < 0:
                        direction /= -direction
                    else:
                        direction /= direction

                    invalid = [
                        self.capture and v != (1, 1),
                        not self.capture and v == (1, 1),
                        v == (2, 0) and self.start[0] not in (1, 6),
                        direction < 0 and self.piece.colour == attrs.Colour.WHITE,
                        direction > 0 and self.piece.colour == attrs.Colour.BLACK,
                    ]

                    if not any(invalid):
                        can_move = True
                        break
                    # pawns can only capture diagonally and must move forward otherwise
                    # pawns can only move two squares forward from their starting rank

        if not can_move:
            return False

        blocked = False

        if (
            self.board.array[self.destination[0]][self.destination[1]]
            and not self.capture
        ):
            blocked = True

        elif self.piece.symbol != "n":
            intermediate = [self.start[0], self.start[1]]

            while (intermediate[0], intermediate[1]) != self.destination:
                for i in range(0, 2):
                    if intermediate[i] < self.destination[i]:
                        intermediate[i] += 1

                    elif intermediate[i] > self.destination[i]:
                        intermediate[
                            i
                        ] -= 1  # accounts for white and black pieces moving in different directions

                square = self.board.array[intermediate[0]][intermediate[1]]

                if square:
                    if square.position != self.destination:
                        blocked = True
                        break

        if blocked:
            return False

        if self.capture:
            piece_to_capture = self.board.array[self.destination[0]][
                self.destination[1]
            ]

            if not piece_to_capture:
                offset = -1 if self.piece.colour == attrs.Colour.WHITE else 1
                en_passant_piece = self.board.array[self.destination[0] + offset][
                    self.destination[1]
                ]

                if not en_passant_piece:
                    return False

                if en_passant_piece.colour == self.piece.colour:
                    return False

            elif piece_to_capture.colour == self.piece.colour:
                return False

        return True

    def make_move(self):
        """Carries out a pseudo-legal move and updates the board state."""
        if not self.pseudo_legal():
            return

        self.board.array[self.start[0]][self.start[1]] = None

        if self.capture:
            captured_piece = self.board.array[self.destination[0]][self.destination[1]]

            if not captured_piece:  # en passant capture
                offset = -1 if self.piece.colour == attrs.Colour.WHITE else 1
                captured_piece = self.board.array[self.destination[0] + offset][
                    self.destination[1]
                ]
                self.board.array[self.destination[0] + offset][
                    self.destination[1]
                ] = None

            elif captured_piece.symbol == "r" and captured_piece.move_count == 0:
                colour = 0 if captured_piece.colour == attrs.Colour.WHITE else 2
                castle = 0 if captured_piece.position[1] == 0 else 1
                self.board.castling_rights[colour + castle] = False
                self.board.array[self.destination[0]][self.destination[1]] = None
            else:
                self.board.array[self.destination[0]][self.destination[1]] = None

            self.board.captured_pieces.append(captured_piece)

        if self.promotion:
            self.board.array[self.destination[0]][self.destination[1]] = self.promotion(
                self.piece.colour, self.destination
            )

        elif self.castling:
            if self.piece.colour == attrs.Colour.WHITE:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = self.board.array[0][0]
                    rook_destination = (0, 3)
                else:
                    rook = self.board.array[0][7]
                    rook_destination = (0, 5)

                self.board.castling_rights[0] = False
                self.board.castling_rights[1] = False

            else:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = self.board.array[7][0]
                    rook_destination = (7, 3)
                else:
                    rook = self.board.array[7][7]
                    rook_destination = (7, 5)

                self.board.castling_rights[2] = False
                self.board.castling_rights[3] = False

            self.board.array[rook.position[0]][rook.position[1]] = None
            self.board.array[rook_destination[0]][rook_destination[1]] = rook

            rook.position = rook_destination
            rook.move_count += 1

            self.board.array[self.destination[0]][self.destination[1]] = self.piece
            self.piece.position = self.destination
            self.piece.move_count += 1

        else:
            self.board.array[self.destination[0]][self.destination[1]] = self.piece
            self.piece.position = self.destination
            self.piece.move_count += 1

            index = 0 if self.piece.colour == attrs.Colour.WHITE else 2

            if self.piece.move_count == 1:
                if self.piece.symbol == "k":
                    self.board.castling_rights[index] = False
                    self.board.castling_rights[index + 1] = False

                elif self.piece.symbol == "r":
                    castle = 0 if self.piece.position[1] == 0 else 1
                    self.board.castling_rights[index + castle] = False

        self.board.half_move_clock += 1
        en_passant = -1

        if self.piece.symbol == "p" and self.piece.move_count == 1:
            if self.distance[0] == 2:
                for shift in (1, -1):
                    if self.destination[1] + shift in range(8):
                        enemy_pawn = self.board.array[self.destination[0]][
                            self.destination[1] + shift
                        ]
                        if enemy_pawn:
                            if (
                                enemy_pawn.symbol == "p"
                                and enemy_pawn.colour != self.piece.colour
                            ):
                                en_passant = self.destination[1]

        # en passant capture is only possible immediately after a pawn advances two squares in one move
        self.board.en_passant_file = en_passant

        if self.board.side_to_move == attrs.Colour.WHITE:
            self.board.side_to_move = attrs.Colour.BLACK
        else:
            self.board.side_to_move = attrs.Colour.WHITE

    def unmake_move(self):
        """Reverses a move and any changes to the board state."""
        if self.board.side_to_move == attrs.Colour.WHITE:
            self.board.side_to_move = attrs.Colour.BLACK
        else:
            self.board.side_to_move = attrs.Colour.WHITE

        self.board.half_move_clock -= 1
        self.board.en_passant_file = -1
        self.board.array[self.destination[0]][self.destination[1]] = None

        if self.castling:
            if self.piece.colour == attrs.Colour.WHITE:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = self.board.array[0][3]
                    rook_destination = (0, 0)
                    self.board.castling_rights[0] = True
                else:
                    rook = self.board.array[0][5]
                    rook_destination = (0, 7)
                    self.board.castling_rights[1] = True
            else:
                if self.castling == attrs.Castling.QUEEN_SIDE:
                    rook = self.board.array[7][3]
                    rook_destination = (7, 0)
                    self.board.castling_rights[2] = True
                else:
                    rook = self.board.array[7][5]
                    rook_destination = (7, 7)
                    self.board.castling_rights[3] = True

            self.board.array[rook_destination[0]][rook_destination[1]] = rook
            self.board.array[rook.position[0]][rook.position[1]] = None
            rook.position = rook_destination
            rook.move_count -= 1

            other_rook = self.board.array[rook_destination[0]][7 - rook_destination[1]]
            offset = int(self.castling == attrs.Castling.QUEEN_SIDE)
            index = 0 if self.piece.colour == attrs.Colour.WHITE else 2

            if other_rook:
                if other_rook.move_count == 0:
                    self.board.castling_rights[index + offset] = True

            self.board.array[self.start[0]][self.start[1]] = self.piece
            self.piece.position = self.start
            self.piece.move_count -= 1

        else:
            if self.piece.colour == attrs.Colour.WHITE:
                index = 0
                rank = 0
            else:
                index = 2
                rank = 7

            if self.piece.symbol == "k":
                if self.piece.move_count == 1:
                    r_queen = self.board.array[rank][0]
                    r_king = self.board.array[rank][7]

                    for i, r in enumerate((r_queen, r_king)):
                        if r:
                            if r.symbol == "r" and r.move_count == 0:
                                self.board.castling_rights[index + i] = True

            elif self.piece.symbol == "r":
                king = self.board.array[rank][4]

                if king:
                    if king.symbol == "k" and king.move_count == 0:
                        if self.piece.move_count == 1:
                            castle = 0 if self.start[1] == 0 else 1
                            self.board.castling_rights[index + castle] = True

            if self.capture:
                captured = self.board.captured_pieces[-1]
                self.board.array[captured.position[0]][captured.position[1]] = captured

                if (
                    captured.symbol == "r" and captured.move_count == 0
                ):  # restore castling rights for captured rook
                    king = self.board.array[captured.position[0]][4]

                    if king:
                        if king.symbol == "k" and king.move_count == 0:
                            castle = 0 if captured.position[1] == 0 else 1
                            r_index = 2 if index == 0 else 0
                            self.board.castling_rights[r_index + castle] = True

                self.board.captured_pieces.remove(captured)

            self.board.en_passant_file = -1
            en_passant_rank = 4 if self.piece.colour == attrs.Colour.WHITE else 3

            for i, piece in enumerate(self.board.array[en_passant_rank]):
                if piece:
                    conditions = [
                        piece.symbol == "p",
                        piece.colour != self.piece.colour,
                        piece.move_count == 1,
                    ]
                    if all(conditions):
                        self.board.en_passant_file = (
                            i  # restore file of possible en passant capture
                        )

            self.board.array[self.start[0]][self.start[1]] = self.piece
            self.piece.position = self.start
            self.piece.move_count -= 1

    def legal(self):
        """Checks if a pseudo-legal move leaves the king in check."""
        if not self.pseudo_legal():
            return False

        if self.castling:
            files = (
                [2, 3, 4] if self.castling == attrs.Castling.QUEEN_SIDE else [4, 5, 6]
            )

            if self.piece.colour == attrs.Colour.WHITE:
                rank = 0
                self.board.side_to_move = attrs.Colour.BLACK
            else:
                rank = 7
                self.board.side_to_move = attrs.Colour.WHITE

            for row in self.board.array:
                for enemy_piece in row:
                    if enemy_piece:
                        if enemy_piece.colour != self.piece.colour:
                            for file in files:
                                threat = Move(
                                    enemy_piece,
                                    self.board,
                                    enemy_piece.position,
                                    (rank, file),
                                    capture=(file == 4),
                                )
                                if threat.pseudo_legal():
                                    self.board.side_to_move = self.piece.colour
                                    return False

            self.board.side_to_move = self.piece.colour
            return True

        self.make_move()

        index_1 = 0 if self.piece.colour == attrs.Colour.WHITE else 7
        index_2 = 7 - index_1
        step = 1 if index_2 > index_1 else -1

        for i in range(index_1, index_2 + step, step):
            for piece in self.board.array[i]:
                if piece:
                    if piece.symbol == "k" and piece.colour == self.piece.colour:
                        king = piece
                        break

        for i in range(index_2, index_1 - step, -step):
            for enemy_piece in self.board.array[i]:
                if enemy_piece:
                    if enemy_piece.colour != self.piece.colour:
                        threat = Move(
                            enemy_piece,
                            self.board,
                            enemy_piece.position,
                            king.position,
                            capture=True,
                        )
                        if threat.pseudo_legal():
                            self.unmake_move()
                            return False

        self.unmake_move()
        return True
