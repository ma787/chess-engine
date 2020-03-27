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

    def __init__(self, colour, position, board, icon):
        self.colour = colour
        self.position = position
        self.board = board
        self.icon = icon

    def check_if_move_possible(self, move_class):
        """Checks if the move is pseudo-legal."""
        start = move_class.start
        destination = move_class.destination
        distance = (destination[0] - start[0], destination[1] - start[1])

        conditions = ((abs(distance[0]) == abs(distance[1])), (distance[0] == 0) or (distance[1] == 0),
                      (abs(distance[0]) > 1) or (abs(distance[1]) > 1))

        if move_class.piece_class == Bishop:
            if conditions[0]:
                return self.try_move(move_class)
            else:
                return False

        elif move_class.piece_class == Rook:
            if conditions[1]:
                return self.try_move(move_class)
            else:
                return False

        elif move_class.piece_class == Queen:
            if conditions[0] or conditions[1]:
                return self.try_move(move_class)
            else:
                return False

        elif move_class.piece_class == King:
            if not conditions[2]:
                return self.try_move(move_class)
            else:
                return False

    def try_move(self, move_class):
        """Simulates the move to check if it is legal."""
        start = move_class.start
        destination = move_class.destination
        intermediate = [start[0], start[1]]

        if move_class.piece_class != Knight:
            while True:
                if (intermediate[0], intermediate[1]) == destination:
                    break

                for i in range(0, 2):
                    if intermediate[i] < destination[i]:
                        intermediate[i] += 1

                    elif intermediate[i] > destination[i]:
                        intermediate[i] -= 1

                square = move_class.virtual_board.array[intermediate[0]][intermediate[1]]

                if square:
                    return False

        if move_class.en_passant:
            if move_class.colour == Colour.WHITE:
                captured_piece = move_class.virtual_board.array[destination[0] - 1][destination[1]]
            else:
                captured_piece = move_class.virtual_board.array[destination[0] + 1][destination[1]]

            move_class.virtual_board.piece_list.remove(captured_piece)
            move_class.virtual_board.discarded_pieces.append(captured_piece)

        elif move_class.is_capture:
            captured_piece = move_class.virtual_board.array[destination[0]][destination[1]]

            if not captured_piece:
                return False
            else:
                move_class.virtual_board.piece_list.remove(captured_piece)
                move_class.virtual_board.discarded_pieces.append(captured_piece)

        else:
            if move_class.virtual_board.array[destination[0]][destination[1]]:
                return False

        move_class.virtual_board.array[start[0]][start[1]] = None
        move_class.virtual_board.array[destination[0]][destination[1]] = self

        for piece in move_class.virtual_board.piece_list:
            if (isinstance(piece, King)) and (piece.colour == self.colour):
                king_in_check = piece
                break

        if not move_class.control_check:
            if move_class.virtual_board.is_square_controlled(king_in_check.position, move_class.virtual_board,
                                                             move_class.side_to_move):
                return False
            else:
                return True
        else:
            return True

    def perform_move(self, move_class):
        """Moves the piece to the destination square"""
        start = move_class.start
        destination = move_class.destination

        if move_class.en_passant:
            if move_class.colour == Colour.WHITE:
                captured_piece = self.board.array[destination[0] - 1][destination[1]]
            else:
                captured_piece = self.board.array[destination[0] + 1][destination[1]]

            self.board.piece_list.remove(captured_piece)
            self.board.discarded_pieces.append(captured_piece)

        elif move_class.is_capture:
            captured_piece = self.board.array[destination[0]][destination[1]]

            self.board.piece_list.remove(captured_piece)
            self.board.discarded_pieces.append(captured_piece)

        self.board.array[start[0]][start[1]] = None
        self.board.array[destination[0]][destination[1]] = self

        self.position = destination

        return

# piece class as a template with a basic move function


class Pawn(Piece):
    def __init__(self, colour, position, board, icon):
        super().__init__(colour, position, board, icon)
        self.has_moved = False

    value = 1
    symbol = "p"

    def check_if_move_possible(self, move_class):
        start = move_class.start
        destination = move_class.destination
        distance = (destination[0] - start[0], destination[1] - start[1])
        letter_ref = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        if (self.colour == Colour.WHITE) and (distance[0] <= 0):
            return False

        elif (self.colour == Colour.BLACK) and (distance[0] >= 0):
            return False

        if move_class.promotion:
            if (self.colour == Colour.WHITE) and (destination[0] != 8):
                return False

            elif (self.colour == Colour.BLACK) and (destination[0] != 0):
                return False

        if move_class.is_capture:
            if abs(distance[1]) != 1:
                return False

            if (self.colour == Colour.WHITE) and ((start[0], destination[0]) == (4, 5)):
                ep_check = True

            elif (self.colour == Colour.BLACK) and ((start[0], destination[0]) == (3, 2)):
                ep_check = True
            else:
                ep_check = False

            if ep_check:
                if len(move_class.virtual_board.past_three_moves) > 0:
                    last_move = move_class.virtual_board.past_three_moves[-1]

                    if self.colour == Colour.WHITE:
                        form_check = re.fullmatch("[a-h][7][-][a-h][5]", last_move)
                    else:
                        form_check = re.fullmatch("[a-h][2][-][a-h][4]", last_move)

                    if form_check:
                        last_file = letter_ref[last_move[0]]

                        if last_file == destination[1]:
                            move_class.en_passant = True
                            return self.try_move(move_class)
                        else:
                            move_class.en_passant = False
                    else:
                        move_class.en_passant = False
                else:
                    move_class.en_passant = False

            return self.try_move(move_class)

        if distance[1] != 0:
            return False

        elif abs(distance[0]) > 1:
            if self.has_moved or (abs(distance[0]) != 2):
                return False
            else:
                return self.try_move(move_class)

        else:
            return self.try_move(move_class)


class Knight(Piece):
    value = 3
    symbol = "n"

    def check_if_move_possible(self, move_class):
        start = move_class.start
        destination = move_class.destination
        distance = (abs(destination[0] - start[0]), abs(destination[1] - start[1]))

        if (distance[0] == 2) and (distance[1] == 1):
            return self.try_move(move_class)

        elif (distance[0] == 1) and (distance[1] == 2):
            return self.try_move(move_class)
        else:
            return False


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
    value = sys.maxsize - 206  # total value of all other possible pieces, prevents overflow
    symbol = "k"


class ChessBoard:
    def __init__(self):
        self.piece_list = []
        self.discarded_pieces = []
        self.fifty_move_count = 0
        self.past_three_moves = []
        self.array = [[None for i in range(8)] for i in range(8)]
        self.letter_ref = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        # black pieces
        self.array[0][0] = Rook(Colour.WHITE, (0, 0), self, "\u2656")
        self.array[0][1] = Knight(Colour.WHITE, (0, 1), self, "\u2658")
        self.array[0][2] = Bishop(Colour.WHITE, (0, 2), self, "\u2657")
        self.array[0][3] = Queen(Colour.WHITE, (0, 3), self, "\u2655")
        self.array[0][4] = King(Colour.WHITE, (0, 4), self, "\u2654")
        self.array[0][5] = Bishop(Colour.WHITE, (0, 5), self, "\u2657")
        self.array[0][6] = Knight(Colour.WHITE, (0, 6), self, "\u2658")
        self.array[0][7] = Rook(Colour.WHITE, (0, 7), self, "\u2656")

        # black pawns
        for i in range(0, 8):
            self.array[1][i] = Pawn(Colour.WHITE, (1, i), self, "\u2659")

        # white pieces
        self.array[7][0] = Rook(Colour.BLACK, (7, 0), self, "\u265c")
        self.array[7][1] = Knight(Colour.BLACK, (7, 1), self, "\u265e")
        self.array[7][2] = Bishop(Colour.BLACK, (7, 2), self, "\u265d")
        self.array[7][3] = Queen(Colour.BLACK, (7, 3), self, "\u265b")
        self.array[7][4] = King(Colour.BLACK, (7, 4), self, "\u265a")
        self.array[7][5] = Bishop(Colour.BLACK, (7, 5), self, "\u265d")
        self.array[7][6] = Knight(Colour.BLACK, (7, 6), self, "\u265e")
        self.array[7][7] = Rook(Colour.BLACK, (7, 7), self, "\u265c")

        # white pawns
        for i in range(0, 8):
            self.array[6][i] = Pawn(Colour.BLACK, (6, i), self, "\u265f")

        for row in self.array:
            for square in row:
                if square:
                    self.piece_list.append(square)  # adds the pieces to the piece list

    def __repr__(self):
        output = ""
        for row in reversed(self.array):
            symbols = []
            for piece in row:
                if piece:
                    symbols.append(piece.icon)
                else:
                    symbols.append("-")
            output += "".join(symbols) + "\n"
        return output

    # TODO: When choosing a side against the engine, must change orientation of board to reflect this.

    def is_square_controlled(self, square_ref, virtual_board, side_to_move):
        """Checks if a square on the board can be attacked by an enemy piece."""
        piece_to_check = self.array[square_ref[0]][square_ref[1]]

        if side_to_move == Colour.WHITE:
            enemy_colour = Colour.BLACK
        else:
            enemy_colour = Colour.WHITE

        if piece_to_check:
            capture = True
        else:
            capture = False

        initial_vb = virtual_board
        pseudo = False

        for piece in self.piece_list:
            if piece.colour == enemy_colour:
                move_to_make = Move(piece, type(piece), enemy_colour, piece.position, square_ref, virtual_board,
                                    side_to_move, is_capture=capture, control_check=True)

                if move_to_make.check_move():
                    pseudo = True
                    break
                else:
                    pseudo = False
                    virtual_board = initial_vb

        if pseudo:
            return True
        else:
            return False


class Game:
    def __init__(self, board, virtual_board):
        self.board = board
        self.virtual_board = virtual_board
        self.side_to_move = Colour.WHITE
        self.scores = [0, 0]

    def convert_lan_to_move(self, move_string):
        """Validates and changes the move entered by a user to a class and coordinates."""
        colour = self.side_to_move

        piece_check = re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string)
        pawn_check = re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string)
        castling_check = (move_string in ("0-0", "0-0-0"))

        piece_type = None
        promotion = None
        castling = None
        capture = False

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

        elif pawn_check:
            piece_type = Pawn

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

        elif castling_check:
            piece_type = King
            split_string = move_string.split("-")

            if len(split_string) == 3:
                castling = Castling.QUEEN_SIDE
                end_letter = "c"
            else:
                castling = Castling.KING_SIDE
                end_letter = "g"

            if colour == Colour.WHITE:
                start_string = "e1"
                end_string = end_letter + "1"

            else:
                start_string = "e8"
                end_string = end_letter + "8"
        else:
            return None

        start_coord = (int(start_string[1]) - 1, self.board.letter_ref[start_string[0]])
        end_coord = (int(end_string[1]) - 1, self.board.letter_ref[end_string[0]])

        if start_coord == end_coord:
            return None

        piece_to_move = self.board.array[start_coord[0]][start_coord[1]]
        
        move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, self.virtual_board, self.side_to_move,
                    castling=castling, is_capture=capture, promotion=promotion)

        return move

    def is_in_check(self):
        """Checks if one of the players is in check."""
        return

    def check_end_of_game(self):
        """Checks if the game is over due to checkmate, the fifty move rule, threefold repetition or a stalemate."""
        return ""

    def play_game(self):
        """Executes a loop that runs the game itself, taking move inputs and keeping track of turns."""
        while True:
            side = self.side_to_move.name.lower()
            user_input = input("Enter move ({}): ".format(side))
            move = self.convert_lan_to_move(user_input)

            if not move:
                print("Please enter the move in the correct format.")
            else:
                if not move.check_move():
                    print("This move is not valid.")

                else:
                    move.make_move()
                    print(self.board)

                    if move.is_capture:
                        last_piece = self.board.discarded_pieces[-1]
                        self.scores[self.side_to_move.value] += last_piece.value

                    if isinstance(move.piece, Pawn) or move.is_capture:
                        self.board.fifty_move_count = 0
                    else:
                        self.board.fifty_move_count += 1

                    self.board.past_three_moves.append(user_input)

                    result = self.check_end_of_game()

                    if result:
                        break

                    if self.side_to_move == Colour.WHITE:
                        self.side_to_move = Colour.BLACK
                    else:
                        self.side_to_move = Colour.WHITE

                    self.virtual_board = self.board

        print("Done.")


class Move:
    def __init__(self, piece, piece_class, colour, start, destination, virtual_board, side_to_move, castling=None,
                 is_capture=False, promotion=None, control_check=False):
        self.piece = piece
        self.piece_class = piece_class
        self.colour = colour
        self.start = start
        self.destination = destination
        self.virtual_board = virtual_board
        self.side_to_move = side_to_move
        self.castling = castling
        self.is_capture = is_capture
        self.promotion = promotion
        self.en_passant = False
        self.control_check = control_check

    def check_move(self):
        """Finds the piece to move on the board and executes the move."""
        if (not self.piece) or (not isinstance(self.piece, self.piece_class)):
            return False

        else:
            return self.piece.check_if_move_possible(self)

    def make_move(self):
        """Finds the piece to move on the board and executes the move."""
        self.piece.perform_move(self)


game_board = ChessBoard()
v_board = ChessBoard()
new_game = Game(game_board, v_board)
