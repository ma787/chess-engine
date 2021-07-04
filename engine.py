import copy
import math

from castling import Castling
from colour import Colour
from hashing import Hashing
from move import Move
from nodetype import NodeType
from pieces import King, Queen
import lanparser


class Searching:
    def __init__(self):
        self.hashing = Hashing()
        self.transposition_table = []  # contains (hashed board position, move class, score, root, node type)

    @staticmethod
    def check_possible_moves(board):
        """Finds all of the legal moves that the side to move can make."""
        piece_list = list(filter(lambda x: x.colour == board.side_to_move, board.piece_list))
        destinations = {}
        possible_moves = []

        for i, row in enumerate(board.array):
            for j, square in enumerate(row):
                if square:
                    if square.colour != board.side_to_move:
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

                if move.check_move(board):
                    possible_moves.append(move)

        s = 0 if board.side_to_move == Colour.WHITE else 7

        castles = [Move("k", King, board.side_to_move, (s, 4), (s, 2), castling=Castling.QUEEN_SIDE),
                   Move("k", King, board.side_to_move, (s, 4), (s, 6), castling=Castling.KING_SIDE)]

        for c in castles:
            if c.check_move(board):
                possible_moves.append(c)

        return possible_moves

    def alpha_beta_search(self, alpha, beta, depth, board):
        """Finds the highest score attainable from the current position."""
        board_hash = self.hashing.zobrist_hash(board)

        if depth == 0:
            score = evaluate(board)
            self.transposition_table.append((board_hash, None, score, True, NodeType.PV))
            return score

        prev_searched = None

        for table in self.transposition_table:  # checks if the current node has already been reached
            if board_hash == table[0]:
                prev_searched = table
                break

        if prev_searched:
            if prev_searched[-1] == NodeType.CUT:
                return beta
            elif prev_searched[-1] == NodeType.ALL:
                return alpha
            else:
                self.transposition_table.remove(prev_searched)  # search tree will be extended from previous leaf node

        if len(self.transposition_table) > 128:
            self.transposition_table.remove(self.transposition_table[0])

        possible_moves = Searching.check_possible_moves(board)
        move_change = None

        for move in possible_moves:
            virtual = copy.deepcopy(board)
            move.perform_move(virtual)

            user_input = lanparser.convert_move_to_lan(move)
            board.last_move = user_input

            if board.side_to_move == Colour.WHITE:
                board.side_to_move = Colour.BLACK
            else:
                board.side_to_move = Colour.WHITE  # updating the board state

            score = -self.alpha_beta_search(-beta, -alpha, depth - 1, board)
            # applied recursively to reach required depth
            # opponent's gains = engine's losses so values are reversed

            if score >= beta:  # 'too good'
                self.transposition_table.append((board_hash, None, beta, False, NodeType.CUT))
                return beta

            if score > alpha:
                alpha = score  # new lower bound set
                move_change = move

        if move_change:
            self.transposition_table.append((board_hash, move_change, alpha, False, NodeType.PV))
        else:
            self.transposition_table.append((board_hash, None, alpha, False, NodeType.ALL))

        return alpha

    def find_move(self, board):  # 'retraces' the path of the alpha-beta search
        """Finds the move that will attain the best score."""
        board_hash = self.hashing.zobrist_hash(board)
        score = self.alpha_beta_search(math.inf, (-math.inf), 3, board)
        virtual = copy.deepcopy(board)

        for t in self.transposition_table:
            if t[0] == board_hash:
                table = t
                break

        current_hash = board_hash
        initial_move = None

        while True:
            move = table[1]

            if move:
                current_hash = self.hashing.update_hash(current_hash, move, virtual)

                for t in self.transposition_table:
                    if t[0] == current_hash:
                        table = t
                        move.perform_move(virtual)
                        break

                if not initial_move:
                    initial_move = move

                if table[2] == score:
                    return initial_move


def evaluate(board):
    """Returns the value of a certain position."""
    white_piece_values = {"p": [[0, 0, 0, 0, 0, 0, 0, 0],
                                [50, 50, 50, 50, 50, 50, 50, 50],
                                [10, 10, 20, 30, 30, 20, 10, 10],
                                [5, 5, 10, 25, 25, 10, 5, 5],
                                [0, 0, 0, 20, 20, 0, 0, 0],
                                [5, -5, -10, 0, 0, -10, -5, 5],
                                [5, 10, 10, -20, -20, 10, 10, 5],
                                [0, 0, 0, 0, 0, 0, 0, 0]],

                          "b": [[-20, -10, -10, -10, -10, -10, -10, -20],
                                [-10, 0, 0, 0, 0, 0, 0, -10],
                                [-10, 0, 5, 10, 10, 5, 0, -10],
                                [-10, 5, 5, 10, 10, 5, 5, -10],
                                [-10, 0, 10, 10, 10, 10, 0, -10],
                                [-10, 10, 10, 10, 10, 10, 10, -10],
                                [-10, 5, 0, 0, 0, 0, 5, -10],
                                [-20, -10, -10, -10, -10, -10, -10, -20]],

                          "n": [[-50, -40, -30, -30, -30, -30, -40, -50],
                                [-40, -20, 0, 0, 0, 0, -20, -40],
                                [-30, 0, 10, 15, 15, 10, 0, -30],
                                [-30, 5, 15, 20, 20, 15, 5, -30],
                                [-30, 0, 15, 20, 20, 15, 0, -30],
                                [-30, 5, 10, 15, 15, 10, 5, -30],
                                [-40, -20, 0, 5, 5, 0, -20, -40],
                                [-50, -40, -30, -30, -30, -30, -40, -50]],

                          "r": [[0, 0, 0, 0, 0, 0, 0, 0],
                                [5, 10, 10, 10, 10, 10, 10, 5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [0, 0, 0, 5, 5, 0, 0, 0]],

                          "q": [[-20, -10, -10, -5, -5, -10, -10, -20],
                                [-10, 0, 0, 0, 0, 0, 0, -10],
                                [-10, 0, 5, 5, 5, 5, 0, -10],
                                [-5, 0, 5, 5, 5, 5, 0, -5],
                                [0, 0, 5, 5, 5, 5, 0, -5],
                                [-10, 5, 5, 5, 5, 5, 0, -10],
                                [-10, 0, 5, 0, 0, 0, 0, -10],
                                [-20, -10, -10, -5, -5, -10, -10, -20]],

                          "k": [[-30, -40, -40, -50, -50, -40, -40, -30],
                                [-30, -40, -40, -50, -50, -40, -40, -30],
                                [-30, -40, -40, -50, -50, -40, -40, -30],
                                [-30, -40, -40, -50, -50, -40, -40, -30],
                                [-20, -30, -30, -40, -40, -30, -30, -20],
                                [-10, -20, -20, -20, -20, -20, -20, -10],
                                [20, 20, 0, 0, 0, 0, 20, 20],
                                [20, 30, 10, 0, 0, 10, 30, 20]]
                          }  # pieces are more or less useful at certain positions

    black_piece_values = {x: list(reversed(y)) for x, y in white_piece_values.items()}

    white_values = []
    black_values = []

    for i, row in enumerate(board.array):
        for j, square in enumerate(row):
            if square:
                if square.colour == Colour.WHITE:
                    white_values.append(square.value + white_piece_values[square.symbol][i][j])
                else:
                    black_values.append(square.value + black_piece_values[square.symbol][i][j])

    value = sum(white_values) - sum(black_values)

    if board.side_to_move == Colour.WHITE:
        multiplier = 1  # opposite signs to distinguish between black and white
    else:
        multiplier = -1

    value += len(Searching.check_possible_moves(board))
    value *= multiplier

    return value
