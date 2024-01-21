import math

from .colour import Colour
from .hashing import Hashing
from .lan_parser import convert_move_to_lan
from .move_generation import all_moves_from_position, all_possible_moves


class Engine:
    def __init__(self, colour):
        self.colour = colour
        self.hashing = Hashing()
        self.t_table = {}  # hashed board position: (move string, score)

    def alpha_beta_search(self, board, alpha, beta, depth):
        """Finds the highest score attainable from the current position."""
        if depth == 0:
            return Engine.evaluate(board)

        board_hash = self.hashing.zobrist_hash(board)

        if board_hash in self.t_table.keys():
            return self.t_table[board_hash][1]

        value = -math.inf
        moves = all_possible_moves(board)
        best_move = None

        for move in moves:
            move.make_move()
            value = max(value, -self.alpha_beta_search(board, -beta, -alpha, depth - 1))

            if value >= beta:
                move.unmake_move()
                self.t_table[board_hash] = (convert_move_to_lan(move), value)
                return beta  # beta cutoff

            if value > alpha:
                best_move = move
                alpha = value

            move.unmake_move()

        if best_move:
            best_move = convert_move_to_lan(best_move)

        self.t_table[board_hash] = (best_move, value)
        return alpha

    def find_move(self, board):
        """Performs a search and returns the move that led to the best score."""
        board_hash = self.hashing.zobrist_hash(board)
        depth = 3

        if board_hash in self.t_table.keys():
            return self.t_table[board_hash][0]

        else:
            self.alpha_beta_search(board, -math.inf, math.inf, depth)
            return self.t_table[board_hash][0]

    @staticmethod
    def evaluate(board):
        """Returns the value of a certain position."""
        score = 0

        white_squares = {"p": [[0, 0, 0, 0, 0, 0, 0, 0],
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
                              }  # the utility of a piece varies with its position

        black_squares = {x: list(reversed(y)) for x, y in white_squares.items()}

        white_pieces = []
        black_pieces = []

        for i in range(8):
            for j in range(8):
                square = board.array[i][j]
                if square:
                    if square.colour == Colour.WHITE:
                        white_pieces.append(square)
                    else:
                        black_pieces.append(square)

        white_material = sum([piece.value + white_squares[piece.symbol][piece.position[0]][piece.position[1]]
                              for piece in white_pieces])

        black_material = sum([piece.value + black_squares[piece.symbol][piece.position[0]][piece.position[1]]
                              for piece in black_pieces])

        if board.side_to_move == Colour.WHITE:
            mobility = len([all_moves_from_position(board, piece.position) for piece in white_pieces])
            material = white_material - black_material
            score = material + mobility
        else:
            mobility = len([all_moves_from_position(board, piece.position) for piece in black_pieces])
            material = (black_material - white_material) * -1
            score = material - mobility

        return score
