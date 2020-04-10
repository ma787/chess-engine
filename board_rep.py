from enum import Enum
import sys
import re
import time


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
    icons = ("", "")

    def __init__(self, colour, position):
        self.colour = colour
        self.position = position

        if self.colour == Colour.WHITE:
            self.icon = self.icons[1]
        else:
            self.icon = self.icons[0]

        self.has_moved = False

    def check_if_move_possible(self, move_class):
        """Checks if the piece's move set allows it to move to the destination square."""
        start = move_class.start
        destination = move_class.destination
        distance = (destination[0] - start[0], destination[1] - start[1])  # the change in coordinates

        conditions = ((abs(distance[0]) == abs(distance[1])), ((distance[0] == 0) or (distance[1] == 0)),
                      (abs(distance[0]) > 1) or (abs(distance[1]) > 1))

        # this tuple contains checks to see if the move is diagonal, a straight line or of a magnitude greater than 1

        if move_class.piece_class == Bishop:
            if conditions[0]:
                return move_class.try_move()
            else:
                return None

        elif move_class.piece_class == Rook:
            if conditions[1]:
                return move_class.try_move()
            else:
                return None

        elif move_class.piece_class == Queen:
            if conditions[0] or conditions[1]:
                return move_class.try_move()
            else:
                return None

        elif move_class.piece_class == King:
            if not conditions[2]:
                return move_class.try_move()
            else:
                return None

# piece class is a template with a general move checking function


class Pawn(Piece):
    value = 1
    symbol = "p"
    icons = ("\u265f", "\u2659")

    def check_if_move_possible(self, move_class):
        start = move_class.start
        destination = move_class.destination
        distance = (destination[0] - start[0], destination[1] - start[1])
        letter_ref = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        # the letters correspond to the indexing of the rows in the board array

        if (self.colour == Colour.WHITE) and (distance[0] <= 0):
            return None

        elif (self.colour == Colour.BLACK) and (distance[0] >= 0):
            return None

        condition_1 = (self.colour == Colour.WHITE) and (destination[0] == 7)
        condition_2 = (self.colour == Colour.BLACK) and (destination[0] == 0)

        if move_class.promotion and not (condition_1 or condition_2):
            return None

        elif (condition_1 or condition_2) and not move_class.promotion:
            return None

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
                # checks if the last move entered by the opponent was a pawn move two squares forward

                move_class.en_passant = form_check and (letter_ref[last_move[0]] == destination[1])
            else:
                move_class.en_passant = False

        if move_class.en_passant and (not move_class.is_capture):
            return None
        # makes sure that en passant moves must always be entered as capture moves by the user

        if move_class.is_capture:
            if (abs(distance[0]), abs(distance[1])) != (1, 1):
                return None

            return move_class.try_move()

        if distance[1] != 0:
            return None

        elif abs(distance[0]) > 1:
            if self.has_moved or (abs(distance[0]) != 2):
                return None
            else:
                return move_class.try_move()

        else:
            return move_class.try_move()


class Knight(Piece):
    value = 3
    symbol = "n"
    icons = ("\u265e", "\u2658")

    def check_if_move_possible(self, move_class):
        start = move_class.start
        destination = move_class.destination
        distance = (abs(destination[0] - start[0]), abs(destination[1] - start[1]))

        if (distance[0] == 2) and (distance[1] == 1):
            return move_class.try_move()

        elif (distance[0] == 1) and (distance[1] == 2):
            return move_class.try_move()
        else:
            return False


class Bishop(Piece):
    value = 3
    symbol = "b"
    icons = ("\u265d", "\u2657")


class Rook(Piece):
    value = 5
    symbol = "r"
    icons = ("\u265c", "\u2656")


class Queen(Piece):
    value = 9
    symbol = "q"
    icons = ("\u265b", "\u2655")


class King(Piece):
    value = sys.maxsize - 206  # 206 is the total value of all other possible pieces, prevents overflow
    symbol = "k"
    icons = ("\u265a", "\u2654")


class ChessBoard:
    def __init__(self):
        self.piece_list = []
        self.discarded_pieces = []
        self.past_three_moves = []
        self.array = [[None for i in range(8)] for i in range(8)]
        self.side_to_move = Colour.WHITE
        self.letter_ref = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        # white pieces
        self.array[0][0] = Rook(Colour.WHITE, (0, 0))
        self.array[0][1] = Knight(Colour.WHITE, (0, 1))
        self.array[0][2] = Bishop(Colour.WHITE, (0, 2))
        self.array[0][3] = Queen(Colour.WHITE, (0, 3))
        self.array[0][4] = King(Colour.WHITE, (0, 4))
        self.array[0][5] = Bishop(Colour.WHITE, (0, 5))
        self.array[0][6] = Knight(Colour.WHITE, (0, 6))
        self.array[0][7] = Rook(Colour.WHITE, (0, 7))

        # white pawns
        for i in range(0, 8):
            self.array[1][i] = Pawn(Colour.WHITE, (1, i))

        # black pieces
        self.array[7][0] = Rook(Colour.BLACK, (7, 0))
        self.array[7][1] = Knight(Colour.BLACK, (7, 1))
        self.array[7][2] = Bishop(Colour.BLACK, (7, 2))
        self.array[7][3] = Queen(Colour.BLACK, (7, 3))
        self.array[7][4] = King(Colour.BLACK, (7, 4))
        self.array[7][5] = Bishop(Colour.BLACK, (7, 5))
        self.array[7][6] = Knight(Colour.BLACK, (7, 6))
        self.array[7][7] = Rook(Colour.BLACK, (7, 7))

        # black pawns
        for i in range(0, 8):
            self.array[6][i] = Pawn(Colour.BLACK, (6, i))

        for row in self.array:
            for square in row:
                if square:
                    self.piece_list.append(square)  # adds the pieces to the piece list

    def __repr__(self):  # overrides the built-in print function
        if self.side_to_move == Colour.WHITE:
            board_to_print = reversed(self.array)
            ranks = list(range(8, 0, -1))
        else:
            board_to_print = self.array
            ranks = list(range(1, 9))

        output = ""

        for i, row in enumerate(board_to_print):
            symbols = [str(ranks[i])]
            for piece in row:
                if piece:
                    symbols.append(piece.icon)
                else:
                    symbols.append("\u2003")  # empty space unicode character

            output += "".join(symbols) + "\n"

        output += " \u0041\u0042\u0043\u0044\u0045\u0046\u0047\u0048"  # letters A-H in unicode

        return output

    def is_square_controlled(self, square_ref):
        """Checks if a square on the board can be attacked by an enemy piece."""
        piece_to_check = self.array[square_ref[0]][square_ref[1]]

        if self.side_to_move == Colour.WHITE:
            enemy_colour = Colour.BLACK
        else:
            enemy_colour = Colour.WHITE

        if piece_to_check:  # checks if the square is occupied
            capture = True
        else:
            capture = False

        can_attack = False
        piece_list = [x for x in self.piece_list if x.colour == enemy_colour]

        for piece in piece_list:
            move_to_make = Move(piece, type(piece), enemy_colour, piece.position, square_ref, self,
                                is_capture=capture, control_check=True)

            if move_to_make.check_move():
                can_attack = True
                break
            else:
                can_attack = False

        if can_attack:
            return True
        else:
            return False


class Move:
    def __init__(self, piece, piece_class, colour, start, destination, virtual_board, castling=None,
                 is_capture=False, promotion=None, control_check=False, endgame_check=False):
        self.piece = piece
        self.piece_class = piece_class
        self.colour = colour
        self.start = start
        self.destination = destination
        self.virtual_board = virtual_board
        self.castling = castling
        self.is_capture = is_capture
        self.promotion = promotion
        self.en_passant = False
        self.control_check = control_check
        self.endgame_check = endgame_check

    def check_move(self):
        """Runs the piece move checking function."""
        if (self.start == self.destination) or (not isinstance(self.piece, self.piece_class)):
            return None

        if self.castling:
            return self.check_castle_move()

        return self.piece.check_if_move_possible(self)

    def check_castle_move(self):
        """Checks if a castling move is legal."""
        if self.castling == Castling.QUEEN_SIDE:
            rook_to_move = self.virtual_board.array[self.start[0]][0]
        else:
            rook_to_move = self.virtual_board.array[self.start[0]][7]

        if not rook_to_move or not (isinstance(rook_to_move, Rook)) or (rook_to_move.colour != self.colour):
            return None  # checks if there is a rook of the same colour in the correct position

        if self.piece.has_moved or rook_to_move.has_moved:
            return None

        distance = self.piece.position[1] - rook_to_move.position[1]
        intermediate = self.start[1]

        while True:
            if distance >= 0:
                intermediate -= 1
            else:
                intermediate += 1

            if intermediate == rook_to_move.position[1]:
                break

            square = self.virtual_board.array[self.start[0]][intermediate]

            if square:
                return None  # checks if any of the squares in between the king and the rook are occupied

            if self.virtual_board.is_square_controlled((self.start[0], intermediate)):  # or vulnerable to attack
                if not ((self.castling == Castling.QUEEN_SIDE) and (abs(intermediate - distance) == 1)):
                    return None

        self.virtual_board.array[self.start[0]][self.start[1]] = None
        self.virtual_board.array[self.destination[0]][self.destination[1]] = self.piece

        if self.colour == Colour.WHITE:
            if self.castling == Castling.QUEEN_SIDE:
                rook_destination = (0, 3)
            else:
                rook_destination = (0, 5)

        elif self.castling == Castling.QUEEN_SIDE:
            rook_destination = (7, 3)

        else:
            rook_destination = (7, 5)

        self.virtual_board.array[rook_to_move.position[0]][rook_to_move.position[1]] = None
        self.virtual_board.array[rook_destination[0]][rook_destination[1]] = rook_to_move

        if self.virtual_board.is_square_controlled(self.destination):
            return None

        else:
            return self.virtual_board

    def try_move(self):
        """Simulates the move to check if it is legal."""
        start = self.start
        destination = self.destination
        intermediate = [start[0], start[1]]
        captured_piece = None

        if self.piece_class != Knight:  # knights are the only pieces that can "jump" over occupied squares
            while True:
                for i in range(0, 2):
                    if intermediate[i] < destination[i]:
                        intermediate[i] += 1

                    elif intermediate[i] > destination[i]:
                        intermediate[i] -= 1  # accounts for white and black pieces moving in different directions

                if (intermediate[0], intermediate[1]) == destination:
                    break

                square = self.virtual_board.array[intermediate[0]][intermediate[1]]

                if square:
                    return None

            # checks if there is an occupied square in between the piece's path and the destination

        if self.is_capture:
            if self.en_passant:
                if self.colour == Colour.WHITE:
                    captured_piece = self.virtual_board.array[destination[0] - 1][destination[1]]
                else:
                    captured_piece = self.virtual_board.array[destination[0] + 1][destination[1]]
                # en passant captures are the only ones where the captured piece is not at the destination square

            else:
                captured_piece = self.virtual_board.array[destination[0]][destination[1]]

                if not captured_piece:  # there must be a piece to capture at the destination
                    return None

        elif self.virtual_board.array[destination[0]][destination[1]]:
            return None  # blocks non-capture moves where the destination square is occupied

        if self.control_check:  # this flag is used to skip the king checking below
            return self.virtual_board

        else:
            self.virtual_board.array[start[0]][start[1]] = None

            if self.promotion:
                self.virtual_board.array[destination[0]][destination[1]] = self.promotion(self.colour, destination)
            else:
                self.virtual_board.array[destination[0]][destination[1]] = self.piece

            if captured_piece:
                if self.en_passant:
                    self.virtual_board.array[captured_piece.position[0]][captured_piece.position[1]] = None

                self.virtual_board.piece_list.remove(captured_piece)
                self.virtual_board.discarded_pieces.append(captured_piece)

        for i, row in enumerate(self.virtual_board.array):
            for j, square in enumerate(row):
                if square:
                    if (isinstance(square, King)) and (square.colour == self.colour):
                        coordinates = (i, j)
                        break

        invalid = self.virtual_board.is_square_controlled(coordinates)

        if invalid or self.endgame_check:
            # checks if the opposing side can capture the king if this move were to be made

            self.virtual_board.array[start[0]][start[1]] = self.piece

            if captured_piece:
                self.virtual_board.array[captured_piece.position[0]][captured_piece.position[1]] = captured_piece
                self.virtual_board.discarded_pieces.remove(captured_piece)
                self.virtual_board.piece_list.append(captured_piece)

                if self.en_passant:
                    self.virtual_board.array[destination[0]][destination[1]] = None
            else:
                self.virtual_board.array[destination[0]][destination[1]] = None

            if invalid:
                return None  # reverses the changes made if this is the case
            else:
                return self.virtual_board
        else:
            return self.virtual_board

    def perform_move(self, castling_board=None):
        """Moves the piece to the destination square."""
        if self.castling:
            self.perform_castle_move(castling_board)

        else:
            self.piece.position = self.destination

            if not self.piece.has_moved:
                self.piece.has_moved = True

    def perform_castle_move(self, castling_board):
        """Castles by moving the king and the rook."""
        self.piece.position = self.destination
        self.piece.has_moved = True

        if self.castling == Castling.QUEEN_SIDE:
            rook_destination = (self.destination[0], self.destination[1] + 1)
        else:
            rook_destination = (self.destination[0], self.destination[1] - 1)

        rook_to_move = castling_board.array[rook_destination[0]][rook_destination[1]]
        rook_to_move.position = rook_destination
        rook_to_move.has_moved = True


class Game:
    def __init__(self, board, virtual_board):
        self.board = board
        self.virtual_board = virtual_board
        self.scores = [0, 0]
        self.in_check = False
        self.fifty_move_count = 0

    def convert_lan_to_move(self, move_string):
        """Validates and changes the move string entered by the user to a class and coordinates."""

        piece_check = re.fullmatch("[BKNQR][a-h][1-8][x-][a-h][1-8]", move_string)
        pawn_check = re.fullmatch("[a-h][1-8][x-][a-h][1-8][BKNQR]?", move_string)
        castling_check = (move_string in ("0-0", "0-0-0"))

        # compares the format of the string to these expressions

        piece_type = None
        promotion = None
        castling = None
        capture = False

        if piece_check:
            for p in (Bishop, Knight, Rook, Queen, King):
                if p.symbol == move_string[0].lower():
                    piece_type = p  # matches the first letter of the string to a type
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

            if self.board.side_to_move == Colour.WHITE:
                start_string = "e1"
                end_string = end_letter + "1"

            else:
                start_string = "e8"
                end_string = end_letter + "8"
        else:
            return None

        start_coord = (int(start_string[1]) - 1, self.board.letter_ref[start_string[0]])
        end_coord = (int(end_string[1]) - 1, self.board.letter_ref[end_string[0]])

        piece_to_move = self.board.array[start_coord[0]][start_coord[1]]

        if not piece_to_move:
            return None

        colour = piece_to_move.colour
        
        move = Move(piece_to_move, piece_type, colour, start_coord, end_coord, self.virtual_board, castling=castling,
                    is_capture=capture, promotion=promotion)

        return move

    def is_in_check(self):
        """Checks if the side to move is in check."""
        for piece in self.board.piece_list:
            if (isinstance(piece, King)) and (piece.colour == self.board.side_to_move):
                king_in_check = piece
                break

        return self.board.is_square_controlled(king_in_check.position)

    def check_end_of_game(self):
        """Checks if the game is over due to checkmate, the fifty move rule, threefold repetition or a stalemate."""
        if self.fifty_move_count == 100:
            return True

        if len(self.board.past_three_moves) == 12:
            pairs = [(self.board.past_three_moves[i], self.board.past_three_moves[i + 1]) for i in (0, 2, 4, 6, 8, 10)]

            for pair in pairs:  # one full move is made when both players move a piece
                if pairs.count(pair) == 3:
                    return True

            self.board.past_three_moves.remove(self.board.past_three_moves[0])
            self.board.past_three_moves.remove(self.board.past_three_moves[1])

        piece_list = [x for x in self.board.piece_list if x.colour == self.board.side_to_move]
        destinations = []

        for i, row in enumerate(self.board.array):
            for j, square in enumerate(row):
                if square:
                    if square.colour != self.board.side_to_move:
                        destinations.append(((i, j), True))
                else:
                    destinations.append(((i, j), False))

        for piece in piece_list:
            for d in destinations:
                move_attempt = Move(piece, type(piece), piece.colour, piece.position, d[0], self.virtual_board,
                                    is_capture=d[1], endgame_check=True)

                if move_attempt.check_move():
                    return False  # checks if there are any moves that the player can make

        return True

    def play_game(self):
        """Executes a loop that runs the game itself, taking move inputs and keeping track of turns."""
        print(self.board)

        while True:
            user_input = input("Enter move ({}): ".format(self.board.side_to_move.name.title()))
            move = self.convert_lan_to_move(user_input)

            if not move:
                print("Please enter the move in the correct format, referring to a piece on the board.")

            elif (move.castling and self.in_check) or (move.colour != self.board.side_to_move):
                print("This move is not valid.")

            else:
                self.virtual_board.__dict__ = self.board.__dict__
                new_board = move.check_move()

                if not new_board:
                    print("This move is not valid.")
                else:
                    self.board = new_board
                    move.perform_move(self.board)

                    if move.is_capture:
                        last_piece = self.board.discarded_pieces[-1]
                        self.scores[self.board.side_to_move.value] += last_piece.value

                    if isinstance(move.piece, Pawn) or move.is_capture:
                        self.fifty_move_count = 0
                    else:
                        self.fifty_move_count += 1

                    self.board.past_three_moves.append(user_input)

                    if self.board.side_to_move == Colour.WHITE:
                        self.board.side_to_move = Colour.BLACK
                    else:
                        self.board.side_to_move = Colour.WHITE

                    self.in_check = self.is_in_check()

                    game_over = self.check_end_of_game()

                    if game_over:
                        print(self.board)

                        if self.in_check:
                            if self.board.side_to_move == Colour.WHITE:
                                winner = Colour.BLACK
                            else:
                                winner = Colour.WHITE
                        else:
                            winner = ""

                        if winner:
                            print("{} wins.".format(winner.name.title()))
                        else:
                            print("\nIt is a draw.\n")

                        print("White's score: {}".format(self.scores[Colour.WHITE.value]))
                        print("Black's score: {}".format(self.scores[Colour.BLACK.value]))

                        break

                    print(self.board)

                    if self.in_check:
                        print("{} is in check.".format(self.board.side_to_move.name.title()))

    def play_against_engine(self, player_colour):
        """Runs the game but against the chess engine instead of another player."""
        return


def main():
    print("Welcome!")
    while True:
        game_board = ChessBoard()
        v_board = ChessBoard()
        new_game = Game(game_board, v_board)

        divider = "\n_______________________________________________________________\n"

        print(divider + "Would you like to play with a friend or against the computer?")

        play_mode = input("""Please enter the corresponding number:
(1): With a friend
(2): Against the computer\n""")

        message = ("""Please enter all moves in the following format:
        
For pawns: [starting position]['-' or 'x' for captures][destination][First letter of piece type to promote to]
For other pieces: [First letter of piece type][starting position]['-' or 'x' for captures][destination]
        
For example, 'e2-e4', 'Ng8-h6, 'Re5xd5', 'e7-e8Q' are all valid.
For castling moves, please enter '0-0' for king-side castling and '0-0-0' for queen-side castling.""")

        while play_mode not in ("1", "2"):
            play_mode = input("Please enter either '1' or '2': ")

        play_mode = int(play_mode)

        if play_mode == 1:
            print(divider + message + divider)
            time.sleep(0.5)
            new_game.play_game()

        elif play_mode == 2:
            print(divider + "Would you like to play as Black or White?")
            colour_choice = input("""Please enter the corresponding number:
(1): Black
(2): White\n""")

            while colour_choice not in ("1", "2"):
                colour_choice = input("Please enter either '1' or '2': ")

            colour_choice = int(colour_choice)

            print(divider + message + divider)
            time.sleep(0.5)
            new_game.play_against_engine(colour_choice)

        print(divider + "Would you like to play another game?")
        repeat = input("Press 'y' to do so, or press any other key to exit: ")

        if repeat != "y":
            sys.exit()


if __name__ == "__main__":
    main()
