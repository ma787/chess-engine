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

    def check_if_move_possible(self, destination):
        """Simulates the move to check if it is legal."""
        return True

    def perform_move(self, destination):
        """Moves the piece to the destination square"""
        return True

# piece class as a template with a basic move function


class Pawn(Piece):
    value = 1
    symbol = "p"


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


game_board = ChessBoard()


class Game:
    def __init__(self):
        self.board = game_board
        self.side_to_move = Colour.WHITE

    def convert_lan_to_move(self, move_string):
        """Validates and changes the move entered by a user to a class and coordinates."""
        letter_ref = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        colour = self.side_to_move
        piece_check = re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string)

        if piece_check:
            for p in (Bishop, Knight, Rook, Queen, King):
                if p.symbol == move_string[0].lower():
                    piece_type = p

            if move_string[3] == "x":
                capture = True
            else:
                capture = False

            start_string = move_string[1:3]
            end_string = move_string[-2:]

            start_coord = (letter_ref[start_string[0]], int(start_string[1]))
            end_coord = (letter_ref[end_string[0]], int(end_string[1]))

            piece_to_move = self.board.array[start_coord[0]][start_coord[1]]
            move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, is_capture=capture)

            return (move, True)

        else:
            pawn_check = re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string)
            if pawn_check:
                piece_type = Pawn
                promotion = None
                en_passant = False

                for p in (Bishop, Knight, Rook, Queen, King):
                    if p.symbol == move_string[-1].lower:
                        promotion = p

                if move_string[2] == "x":
                    capture = True
                else:
                    capture = False

                start_string = move_string[0:2]
                end_string = move_string[-2:]

                start_coord = (letter_ref[start_string[0]], int(start_string[1]))
                end_coord = (letter_ref[end_string[0]], int(end_string[1]))
                piece_to_move = self.board.array[start_coord[0]][start_coord[1]]

                if capture:
                    if (colour == Colour.WHITE) and ((start_coord[1], end_coord[1]) == (5, 6)):
                        if len(self.board.past_three_moves) > 0:
                            last_move = self.board.past_three_moves[-1]
                            form_check = re.fullmatch("[a-h][7][-][a-h][5]", last_move)
                            if form_check:
                                en_passant = True
                            else:
                                en_passant = False
                        else:
                            en_passant = False

                    elif (start_coord[1], end_coord[1]) == (4, 3):
                        if len(self.board.past_three_moves) > 0:
                            last_move = self.board.past_three_moves[-1]
                            form_check = re.fullmatch("[a-h][2][-][a-h][4]", last_move)
                            if form_check:
                                en_passant = True
                            else:
                                en_passant = False
                        else:
                            en_passant = False

                move = Move(piece_to_move, piece_type, colour, start_coord, end_coord,
                            is_capture=capture, en_passant=en_passant, promotion=promotion)

                return (move, True)

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

                    start_coord = (letter_ref[start_string[0]], int(start_string[1]))
                    end_coord = (letter_ref[end_string[0]], int(end_string[1]))

                    piece_to_move = self.board.array[start_coord[0]][start_coord[1]]
                    move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, castling=castling)

                    return (move, True)

                else:
                    return (None, False)

    def check_end_of_game(self):
        """Checks if the game is over due to checkmate, the fifty move rule or threefold repetition."""
        return

    def play_game(self):
        """Executes a loop that runs the game itself, taking move inputs and keeping track of turns."""
        return


class Move:
    def __init__(self, piece, piece_class, colour, start, destination,
                 castling=None, is_capture=False, en_passant=False, promotion=None):
        self.piece = piece
        self.piece_class = piece_class
        self.colour = colour
        self.start = start
        self.destination = destination
        self.castling = castling
        self.is_capture = is_capture
        self.en_passant = en_passant
        self.promotion = promotion


new_game = Game()
