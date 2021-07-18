import copy
import math

from castling import Castling
from colour import Colour
from hashing import Hashing
from move import Move
from nodetype import NodeType
from pieces import King, Queen


class Engine:
    def __init__(self):
        self.hashing = Hashing()
        self.transposition_table = {}  # hashed board position: (move class, score, node type)

    def alpha_beta_search(self, alpha, beta, depth, board):
        """Finds the highest score attainable from the current position."""
        board_hash = self.hashing.zobrist_hash(board)

        if depth == 0:
            check = 1 if board.side_to_move == Colour.WHITE else 0
            if board.in_check[check]:
                return 10000  # can capture king

            score = Engine.evaluate(board)
            self.transposition_table[board_hash] = (None, score, NodeType.PV)
            return score

        if board_hash in self.transposition_table:
            prev_searched = self.transposition_table[board_hash]

            if prev_searched[-1] == NodeType.CUT:
                return beta
            elif prev_searched[-1] == NodeType.ALL:
                return alpha
            else:
                del prev_searched  # search tree will be extended from previous leaf node

        if len(self.transposition_table) > 10240:
            del self.transposition_table[list(self.transposition_table.keys())[0]]  # old entries always replaced

        possible_moves = Engine.check_possible_moves(board)
        possible_moves = sorted(possible_moves, key=lambda x: x.is_capture)  # move ordering
        move_change = None

        if len(possible_moves) == 0:
            if board.in_check[board.side_to_move.value]:
                return -10000  # checkmate

        for move in possible_moves:
            virtual = copy.deepcopy(board)
            move.perform_move(virtual)

            score = -self.alpha_beta_search(-beta, -alpha, depth - 1, virtual)
            # applied recursively to reach required depth
            # opponent's gains = engine's losses so values are reversed

            if score >= beta:  # 'too good', this position can be refuted by the opponent
                self.transposition_table[board_hash] = (move, beta, NodeType.CUT)
                return beta

            if score > alpha:
                alpha = score  # new lower bound set
                move_change = move

        if move_change:
            self.transposition_table[board_hash] = (move_change, alpha, NodeType.PV)
        else:
            self.transposition_table[board_hash] = (None, alpha, NodeType.ALL)
            # no moves exceeded the lower bound at this position

        return alpha

    def find_move(self, board):
        """Performs a search and returns the move that led to the best score."""
        board_hash = self.hashing.zobrist_hash(board)
        depth = 3

        self.alpha_beta_search(-math.inf, math.inf, depth, board)

        return self.transposition_table[board_hash][0]

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

    @staticmethod
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

        value += len(Engine.check_possible_moves(board))  # mobility of position
        value *= multiplier

        return value
