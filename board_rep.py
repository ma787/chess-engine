from enum import Enum
import sys
import re


class Colour(Enum):
    WHITE = 0
    BLACK = 1

# number corresponds to black/white pieces


class Castling(Enum):
    QUEEN_SIDE = 1
    KING_SIDE = 2


class Piece:
    value = 0
    symbol = ""

    def __init__(self, colour, position, board):
        self.colour = colour
        self.position = position
        self.board = board

    def check_if_move_possible(self, move_class):
        """Simulates the move to check if it is legal."""
        return True

    def perform_move(self, move_class):
        """Moves the piece to the destination square"""
        return True

# piece class as a template with a basic move function


class Pawn(Piece):
    def __init__(self, colour, position, board):
        super().__init__(colour, position, board)
        self.has_moved = False

    value = 1
    symbol = "p"

    def check_if_move_possible(self, move_class):
        """Simulates the move to check if it is legal."""
        start = move_class.start
        destination = move_class.destination
        distance = (destination[0] - start[0], destination[1] - start[1])

        if move_class.en_passant:
            if (abs(distance[0]) == 1) and (abs(distance[1]) == 1):
                if move_class.check:
                    self.board.array[start[0]][start[1]] = None
                    if move_class.colour == Colour.WHITE:
                        captured_piece = self.board.array[destination[0]][destination[1] + 1]
                    else:
                        captured_piece = self.board.array[destination[0]][destination[1] - 1]

                    self.board.array[destination[0]][destination[1]] = self
                    self.position = destination

                    self.board.piece_list.remove(captured_piece)
                    self.board.discarded_pieces.append(captured_piece)

                    for row in self.board.array:
                        for piece in row:
                            if (isinstance(piece, King)) and (piece.colour == self.colour):
                                king_in_check = piece
                                break

                    # noinspection PyUnboundLocalVariable
                    if self.board.is_square_controlled(king_in_check.position):
                        return False
                else:
                    return True

#TODO: Change the above code to a virtual board instead of the actual board.

class Knight(Piece):
    value = 3
    symbol = "n"


class Bishop(Piece):
    value = 3
    symbol = "b"


class Rook(Piece):
    value = 5
    symbol = "r"


class Queen(Piece):
    value = 9
    symbol = "q"


class King(Piece):
    value = sys.maxsize - 39  # total value of pieces, prevents overflow
    symbol = "k"


class ChessBoard:
    def __init__(self):
        self.piece_list = []
        self.discarded_pieces = []
        self.fifty_move_count = 0
        self.past_three_moves = []
        self.array = [[None for x in range(8)] for x in range(8)]

        # black pieces
        self.array[0][0] = Rook(Colour.BLACK, (0, 0), self)
        self.array[0][1] = Knight(Colour.BLACK, (0, 1), self)
        self.array[0][2] = Bishop(Colour.BLACK, (0, 2), self)
        self.array[0][3] = Queen(Colour.BLACK, (0, 3), self)
        self.array[0][4] = King(Colour.BLACK, (0, 4), self)
        self.array[0][5] = Bishop(Colour.BLACK, (0, 5), self)
        self.array[0][6] = Knight(Colour.BLACK, (0, 6), self)
        self.array[0][7] = Rook(Colour.BLACK, (0, 7), self)

        # black pawns
        self.array[1][0] = Pawn(Colour.BLACK, (1, 0), self)
        self.array[1][1] = Pawn(Colour.BLACK, (1, 1), self)
        self.array[1][2] = Pawn(Colour.BLACK, (1, 2), self)
        self.array[1][3] = Pawn(Colour.BLACK, (1, 3), self)
        self.array[1][4] = Pawn(Colour.BLACK, (1, 4), self)
        self.array[1][5] = Pawn(Colour.BLACK, (1, 5), self)
        self.array[1][6] = Pawn(Colour.BLACK, (1, 6), self)
        self.array[1][7] = Pawn(Colour.BLACK, (1, 7), self)

        # white pieces
        self.array[7][0] = Rook(Colour.WHITE, (7, 0), self)
        self.array[7][1] = Knight(Colour.WHITE, (7, 1), self)
        self.array[7][2] = Bishop(Colour.WHITE, (7, 2), self)
        self.array[7][3] = Queen(Colour.WHITE, (7, 3), self)
        self.array[7][4] = King(Colour.WHITE, (7, 4), self)
        self.array[7][5] = Bishop(Colour.WHITE, (7, 5), self)
        self.array[7][6] = Knight(Colour.WHITE, (7, 6), self)
        self.array[7][7] = Rook(Colour.WHITE, (7, 7), self)

        # white pawns
        self.array[6][0] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][1] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][2] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][3] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][4] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][5] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][6] = Pawn(Colour.WHITE, (6, 0), self)
        self.array[6][7] = Pawn(Colour.WHITE, (6, 0), self)

        for row in self.array:
            for square in row:
                if square:
                    self.piece_list.append(Piece)  # adds the pieces to the piece list

    def __repr__(self):
        output = ""
        for row in self.array:
            symbols = []
            for piece in row:
                if piece:
                    if piece.colour == Colour.BLACK:
                        symbols.append(piece.__class__.symbol.upper())
                    else:
                        symbols.append(piece.__class__.symbol)
                else:
                    symbols.append("-")
            output += "".join(symbols) + "\n"
        return output

    def is_square_controlled(self, square_ref):
        """Checks if a piece on the board is being occupied by an enemy square."""
        return


class Game:
    def __init__(self, board):
        self.board = board
        self.side_to_move = Colour.WHITE
        self.side_in_check = (0, 0)

    def convert_lan_to_move(self, move_string):
        """Validates and changes the move entered by a user to a class and coordinates."""
        letter_ref = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        colour = self.side_to_move
        piece_check = re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string)

        if self.side_in_check[colour.value] == 1:
            check = True
        else:
            check = False

        if piece_check:
            for p in (Bishop, Knight, Rook, Queen, King):
                if p.symbol == move_string[0].lower():
                    piece_type = p
                    break

            if move_string[3] == "x":
                capture = True
            else:
                capture = False

            start_string = move_string[1:3]
            end_string = move_string[-2:]

            start_coord = (int(start_string[1])-1, letter_ref[start_string[0]])
            end_coord = (int(end_string[1])-1, letter_ref[end_string[0]])

            piece_to_move = self.board.array[start_coord[0]][start_coord[1]]
            move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, check, is_capture=capture)

            return move

        else:
            pawn_check = re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string)
            if pawn_check:
                piece_type = Pawn
                promotion = None
                en_passant = False

                for p in (Bishop, Knight, Rook, Queen, King):
                    if p.symbol == move_string[-1].lower():
                        promotion = p
                        break

                if move_string[2] == "x":
                    capture = True
                else:
                    capture = False

                start_string = move_string[0:2]

                if promotion:
                    end_string = move_string[-3:-1]
                else:
                    end_string = move_string[-2:]

                start_coord = (int(start_string[1])-1, letter_ref[start_string[0]])
                end_coord = (int(end_string[1])-1, letter_ref[end_string[0]])
                piece_to_move = self.board.array[start_coord[0]][start_coord[1]]

                if capture:
                    if (colour == Colour.WHITE) and ((start_coord[0], end_coord[0]) == (4, 5)):
                        if len(self.board.past_three_moves) > 0:
                            last_move = self.board.past_three_moves[-1]
                            form_check = re.fullmatch("[a-h][7][-][a-h][5]", last_move)
                            if form_check:
                                if last_move[3] == en_passant[3]:
                                    en_passant = True
                                else:
                                    en_passant = False
                            else:
                                en_passant = False
                        else:
                            en_passant = False

                    elif (colour == Colour.BLACK) and (start_coord[0], end_coord[0]) == (3, 2):
                        if len(self.board.past_three_moves) > 0:
                            last_move = self.board.past_three_moves[-1]
                            form_check = re.fullmatch("[a-h][2][-][a-h][4]", last_move)
                            if form_check:
                                if last_move[3] == move_string[3]:
                                    en_passant = True
                                else:
                                    en_passant = False
                            else:
                                en_passant = False
                        else:
                            en_passant = False

                move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, check,
                            is_capture=capture, en_passant=en_passant, promotion=promotion)

                return move

            else:
                if move_string in ("0-0", "0-0-0"):
                    piece_type = King

                    split_string = move_string.split("-")

                    if len(split_string) == 3:
                        castling = Castling.QUEEN_SIDE
                        end_letter = "c"
                    else:
                        castling = Castling.KING_SIDE
                        end_letter = "g"

                    if colour == Colour.WHITE:
                        rank = "1"
                        start_string = "e" + rank
                        end_string = end_letter + rank

                    else:
                        rank = "8"
                        start_string = "e" + rank
                        end_string = end_letter + rank

                    start_coord = (int(start_string[1])-1, letter_ref[start_string[0]])
                    end_coord = (int(end_string[1])-1, letter_ref[end_string[0]])

                    piece_to_move = self.board.array[start_coord[0]][start_coord[1]]
                    move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, check, castling=castling)

                    return move

                else:
                    return None

    def is_in_check(self):
        """Checks if one of the players is in check."""
        return

    def check_end_of_game(self):
        """Checks if the game is over due to checkmate, the fifty move rule or threefold repetition."""
        return

    def play_game(self):
        """Executes a loop that runs the game itself, taking move inputs and keeping track of turns."""
        return


class Move:
    def __init__(self, piece, piece_class, colour, start, destination, check,
                 castling=None, is_capture=False, en_passant=False, promotion=None):
        self.piece = piece
        self.piece_class = piece_class
        self.colour = colour
        self.start = start
        self.destination = destination
        self.check = check
        self.castling = castling
        self.is_capture = is_capture
        self.en_passant = en_passant
        self.promotion = promotion

    def make_move(self):
        """Finds the piece to move on the board and executes the move."""
        if not self.piece:
            return False

        else:
            self.piece.check_if_move_possible(self)


game_board = ChessBoard()
new_game = Game(game_board)
