import re
import string

from castling import Castling
from colour import Colour
from pieces import Pawn
import lanparser


class Move:
    def __init__(self, piece_symbol, piece_class, colour, start, destination, castling=None,
                 is_capture=False, promotion=None):
        self.piece_symbol = piece_symbol
        self.piece_class = piece_class
        self.colour = colour
        self.start = start
        self.destination = destination
        self.castling = castling
        self.is_capture = is_capture
        self.promotion = promotion
        self.en_passant = False

    def check_move(self, board):
        """Simulates the move after validating it to ensure that it is legal."""
        if self.castling:
            valid_move = self.check_castle_move(board)
        else:
            valid_move = self.check_move_validity(board)

        if not valid_move:
            return False

        last_move = board.last_move
        self.simulate_move(board)

        king = list(filter(lambda k: k.symbol == "k" and (k.colour == board.side_to_move), board.piece_list))[0]

        legal = not Move.is_square_controlled(board, king.position)

        self.unmake_simulation(board, last_move)

        return legal

    def check_move_validity(self, board):
        piece = board.array[self.start[0]][self.start[1]]

        if not piece:
            return False

        if piece.colour != board.side_to_move:
            return False

        if self.piece_symbol == "p":
            possible = piece.can_move_to_square(self.destination, capture=self.is_capture)
        else:
            possible = piece.can_move_to_square(self.destination)

        if not possible:
            return False

        self.en_passant = self.is_en_passant(board)

        return self.check_path_validity(board)

    def is_en_passant(self, board):
        if not board.last_move:
            return False

        if not str.islower(board.last_move[0]):  # checks if the last move was a pawn move
            return False

        if not ((self.piece_symbol == "p") and self.is_capture):
            return False

        if self.colour == Colour.WHITE:
            ranks = (4, 5)
            move_match = "[a-h][7][-][a-h][5]"
        else:
            ranks = (3, 2)
            move_match = "[a-h][2][-][a-h][4]"

        conditions = [(self.start[0], self.destination[0]) == ranks, re.fullmatch(move_match, board.last_move),
                      string.ascii_lowercase.index(board.last_move[0]) == self.destination[1]]

        return all(conditions)

    def check_path_validity(self, board):
        intermediate = [self.start[0], self.start[1]]

        if self.piece_symbol != "n":  # knights are the only pieces that can "jump" over occupied squares
            while True:
                for i in range(0, 2):
                    if intermediate[i] < self.destination[i]:
                        intermediate[i] += 1

                    elif intermediate[i] > self.destination[i]:
                        intermediate[i] -= 1  # accounts for white and black pieces moving in different directions

                if (intermediate[0], intermediate[1]) == self.destination:
                    break

                square = board.array[intermediate[0]][intermediate[1]]

                if square:
                    return False

        if self.is_capture:
            if self.en_passant:
                if self.colour == Colour.WHITE:
                    captured_piece = board.array[self.destination[0] - 1][self.destination[1]]
                else:
                    captured_piece = board.array[self.destination[0] + 1][self.destination[1]]
                # en passant captures are the only ones where the captured piece is not at the destination square

            else:
                captured_piece = board.array[self.destination[0]][self.destination[1]]

            if not captured_piece:  # there must be a piece to capture at the destination
                return False

        elif board.array[self.destination[0]][self.destination[1]]:
            return False  # blocks non-capture moves where the destination square is occupied

        return True

    def simulate_move(self, board):
        piece = board.array[self.start[0]][self.start[1]]
        board.array[self.start[0]][self.start[1]] = None

        if self.is_capture:
            if self.en_passant:
                if self.colour == Colour.WHITE:
                    captured_piece = board.array[self.destination[0] - 1][self.destination[1]]
                else:
                    captured_piece = board.array[self.destination[0] + 1][self.destination[1]]

                board.array[captured_piece.position[0]][captured_piece.position[1]] = None

            else:
                captured_piece = board.array[self.destination[0]][self.destination[1]]

                if captured_piece.symbol == "r":
                    if not captured_piece.moves_made:
                        colour = 0 if captured_piece.colour == Colour.WHITE else 2
                        castle = 0 if captured_piece.position[1] == 0 else 1
                        board.castling_rights[colour + castle] = False

            board.piece_list.remove(captured_piece)
            board.discarded_pieces.append(captured_piece)

        if self.promotion:
            board.piece_list.remove(piece)
            piece = self.promotion(self.colour, self.destination)
            board.piece_list.append(piece)

        if self.castling:
            if self.castling == Castling.QUEEN_SIDE:
                rook = board.array[self.start[0]][0]
            else:
                rook = board.array[self.start[0]][7]

            if self.colour == Colour.WHITE:
                if self.castling == Castling.QUEEN_SIDE:
                    rook_destination = (0, 3)
                else:
                    rook_destination = (0, 5)

            elif self.castling == Castling.QUEEN_SIDE:
                rook_destination = (7, 3)
            else:
                rook_destination = (7, 5)

            board.array[rook.position[0]][rook.position[1]] = None
            board.array[rook_destination[0]][rook_destination[1]] = rook

            rook.position = rook_destination
            rook.moves_made += 1

        board.array[self.destination[0]][self.destination[1]] = piece
        piece.position = self.destination
        piece.moves_made += 1

        index = 0 if self.colour == Colour.WHITE else 2

        if piece.symbol == "k":
            board.castling_rights[index] = False
            board.castling_rights[index + 1] = False

        elif piece.symbol == "r":
            if self.colour == Colour.WHITE:
                queen_side = board.array[0][0]
                king_side = board.array[0][7]
            else:
                queen_side = board.array[7][0]
                king_side = board.array[7][7]

            for i, r in enumerate([queen_side, king_side]):
                if not r:
                    board.castling_rights[index + i] = False
                elif r.moves_made:
                    board.castling_rights[index + i] = False

        board.last_move = lanparser.convert_move_to_lan(self)

    def perform_move(self, board):
        self.simulate_move(board)
        Move.update_board_side(board)

    def check_castle_move(self, board):
        offset = 0 if self.colour == Colour.WHITE else 2

        if self.castling == Castling.QUEEN_SIDE:
            rook = board.array[self.start[0]][0]
            check = board.castling_rights[offset]
        else:
            rook = board.array[self.start[0]][7]
            check = board.castling_rights[offset + 1]

        if not check:
            return False  # checks principle castling rights

        if Move.is_square_controlled(board, self.start):
            return False

        if Move.is_square_controlled(board, rook.position):
            return False

        distance = self.start[1] - rook.position[1]
        intermediate = self.start[1]

        while True:
            if distance >= 0:
                intermediate -= 1
            else:
                intermediate += 1

            if intermediate == rook.position[1]:
                break

            square = board.array[self.start[0]][intermediate]

            if square:
                return False  # checks if any of the squares in between the king and the rook are occupied

            if Move.is_square_controlled(board, (self.start[0], intermediate)):  # or vulnerable to attack
                return False

        return True

    def unmake_simulation(self, board, last_move):
        board.last_move = last_move

        side = Colour.WHITE if board.side_to_move == Colour.BLACK else Colour.BLACK
        indices = (0, 1) if side == Colour.WHITE else (2, 3)

        piece = board.array[self.destination[0]][self.destination[1]]
        board.array[self.destination[0]][self.destination[1]] = None

        if self.castling:
            if self.castling == Castling.QUEEN_SIDE:
                board.castling_rights[indices[0]] = True
                offset = 1
                original = 0
            else:
                board.castling_rights[indices[1]] = True
                offset = -1
                original = 7

            rook = board.array[self.destination[0]][self.destination[1] + offset]

            board.array[self.destination[0]][self.destination[1]] = None
            board.array[self.start[0]][original] = rook

            rook.position = (self.start[0], original)
            rook.moves_made -= 1

        if self.promotion:
            board.piece_list.remove(piece)

            moves = piece.moves_made
            piece = Pawn(side, self.destination)
            piece.moves_made = moves

            board.piece_list.append(piece)

        if self.is_capture:
            if self.en_passant:
                offset = -1 if side == Colour.WHITE else 1
                destination = (self.destination[0] + offset, self.destination[1])
            else:
                destination = self.destination

            captured_piece = board.discarded_pieces[-1]

            board.discarded_pieces.remove(captured_piece)
            board.piece_list.append(captured_piece)

            board.array[destination[0]][destination[1]] = captured_piece

        board.array[self.start[0]][self.start[1]] = piece
        piece.position = self.start
        piece.moves_made -= 1

        rook_left = board.array[self.start[0]][0]
        rook_right = board.array[self.start[0]][7]
        king = board.array[self.start[0]][4]

        if king:
            if not king.moves_made:
                for i, piece in enumerate((rook_left, rook_right)):
                    if piece:
                        if not piece.moves_made:
                            board.castling_rights[indices[i]] = True

    def unmake_move(self, board, last_move):
        self.unmake_simulation(board, last_move)
        side = Colour.WHITE if board.side_to_move == Colour.BLACK else Colour.BLACK

        board.in_check[board.side_to_move.value] = False
        board.side_to_move = side

        king = list(filter(lambda k: k.colour == side and k.symbol == "k", board.piece_list))[0]
        board.in_check[side.value] = Move.is_square_controlled(board, king.position)

    @staticmethod
    def is_square_controlled(board, square_ref):
        """Checks if a square on the board can be attacked by an enemy piece."""
        piece_to_check = board.array[square_ref[0]][square_ref[1]]
        side = board.side_to_move

        if side == Colour.WHITE:
            enemy_colour = Colour.BLACK
        else:
            enemy_colour = Colour.WHITE

        if piece_to_check:  # checks if the square is occupied
            capture = True
        else:
            capture = False

        piece_list = [x for x in board.piece_list if x.colour == enemy_colour]

        for piece in piece_list:
            move_to_make = Move(piece.symbol, type(piece), enemy_colour, piece.position, square_ref,
                                is_capture=capture)

            board.side_to_move = enemy_colour

            can_attack = move_to_make.check_move_validity(board)
            board.side_to_move = side

            if can_attack:
                return True

        return False

    @staticmethod
    def update_board_side(board):
        """Switches the side to move and updates the check status of the other side."""
        board.in_check[board.side_to_move.value] = False  # the side that has made a successful move cannot be in check

        if board.side_to_move == Colour.WHITE:
            board.side_to_move = Colour.BLACK
        else:
            board.side_to_move = Colour.WHITE

        king = list(filter(lambda k: k.symbol == "k" and (k.colour == board.side_to_move), board.piece_list))[0]

        if Move.is_square_controlled(board, king.position):
            board.in_check[board.side_to_move.value] = True
