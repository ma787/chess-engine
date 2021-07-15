from board import Board
from colour import Colour
from engine import Engine
from hashing import Hashing
from move import Move
from pieces import Queen
import lanparser


class Game:
    def __init__(self):
        self.board = Board()
        self.scores = [0, 0]
        self.fifty_move_count = 0
        self.positions = []
        self.hash = Hashing()

    def check_if_moves_available(self):
        """Checks if there are any legal moves that the side to move can make."""
        piece_list = list(filter(lambda x: x.colour == self.board.side_to_move, self.board.piece_list))
        destinations = {}

        for i, row in enumerate(self.board.array):
            for j, square in enumerate(row):
                if square:
                    if square.colour != self.board.side_to_move:
                        destinations[(i, j)] = True
                else:
                    destinations[(i, j)] = False

        for piece in piece_list:
            for place, capture in destinations.items():
                promotion = None

                if (piece.symbol == "p") and (place[0] == (7 if piece.colour == Colour.WHITE else 0)):
                    promotion = Queen

                move = Move(piece.symbol, type(piece), piece.colour, piece.position, place, is_capture=capture,
                            promotion=promotion)

                if move.check_move(self.board):
                    return True

        return False

    def check_end_of_game(self):
        """Checks if the game is over due to checkmate, the fifty move rule, threefold repetition or a stalemate."""
        if self.fifty_move_count == 100:
            return True

        if self.positions.count(self.positions[-1]) == 3:  # checks if the last move resulted in threefold repetition
            return True

        return not self.check_if_moves_available()

    def play_game(self):
        position = self.hash.zobrist_hash(self.board)
        self.positions.append(position)

        while True:
            print(self.board)

            user_input = input("Enter move ({}): ".format(self.board.side_to_move.name.title()))

            move = lanparser.convert_lan_to_move(user_input, self.board.side_to_move)

            if not move:
                print("Please enter a move in the correct syntax.")

            elif not move.check_move(self.board):
                print("This move is not valid.")

            else:
                position = self.hash.update_hash(self.positions[-1], move, self.board)
                self.positions.append(position)

                move.perform_move(self.board)

                if move.is_capture:
                    side = 1 if self.board.side_to_move == Colour.WHITE else 0
                    self.scores[side] += self.board.discarded_pieces[-1].value

                if (move.piece_symbol == "p") or move.is_capture:
                    self.fifty_move_count = 0
                else:
                    self.fifty_move_count += 1

                game_over = self.check_end_of_game()
                in_check = self.board.in_check[self.board.side_to_move.value]

                if game_over:
                    if in_check:
                        if self.board.side_to_move == Colour.WHITE:
                            winner = Colour.BLACK
                        else:
                            winner = Colour.WHITE
                    else:
                        winner = ""

                    if winner:
                        print("\n{} wins.\n".format(winner.name.title()))
                    else:
                        print("\nIt is a draw.\n")

                    print("White's score: {}".format(self.scores[Colour.WHITE.value]))
                    print("Black's score: {}".format(self.scores[Colour.BLACK.value]))

                    break

                else:
                    if in_check:
                        print("\n{} is in check.\n".format(self.board.side_to_move.name.title()))

    def play_engine(self, colour):
        return
