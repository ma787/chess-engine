"""Module providing a class which keeps track of the game state."""

from chess_engine import (
    board,
    hashing,
    lan_parser as lp,
    move,
    move_generation as mg,
)


class Game:
    """A class representing the state associated with a game of chess.

    Attributes:
    board (Board): The board object associated with the game.
    check (bool): Indicates whether the side to move is in check.
    hashing (Hashing): A Hashing object used to hash board positions.
    positions (list): A list of all hashed board positions.
    state (int): Indicates the state of the game:
        -1 - ongoing, 0 - white win, 1 - black win, 2 - draw
    scores (list): The total value of opponent pieces captured by white
        and black respectively.
    """

    def __init__(self):
        self.board = board.Board()
        self.check = False
        self.hashing = hashing.Hashing()
        self.positions = []
        self.state = -1

    def attempt_legal_move(self, move_string):
        """Attempts to make a legal move.

        Args:
            move_string (string): The LAN representation of the requested move.

        Returns:
            int: 0 if successful, and -1 otherwise.
        """
        if self.state != -1:
            return -1

        mv = lp.convert_lan_to_move(move_string, self.board)

        if not mv:
            return -1

        if move.legal(mv, self.board):
            move.make_move(mv, self.board)
            return mv

        return -1

    def update_game_state(self, move_string):
        """Updates the state of the game after a move is submitted.

        Args:
            move_string (string): The LAN representation of the requested move.

        Returns:
            bool: True if a valid move has been performed, and False otherwise.

        """
        res = self.attempt_legal_move(move_string)

        if res == -1:
            return False

        board_hash = self.hashing.zobrist_hash(self.board)
        self.positions.append(board_hash)

        # check draw due to fivefold repetition or fifty move rule
        if self.positions.count(board_hash) == 5 or self.board.halfmove_clock == 100:
            self.state = 2
            return True

        self.check = mg.in_check(self.board)
        moves = mg.all_possible_moves(self.board)

        # checkmate or stalemate
        if len(moves) == 0:
            self.state = int(not self.board.black) if self.check else 2

        return True
