"""Module providing a class which keeps track of the game state."""

from chess_engine import (
    attributes as attrs,
    board,
    hashing,
    lan_parser as lan,
    move_generation as mg,
)


class Game:
    """A class representing the state associated with a game of chess.

    Attributes:
    board (Board): The board object associated with the game.
    check (bool): Indicates whether the side to move is in check.
    hashing (Hashing): A Hashing object used to hash board positions.
    half_move_count (int): A record of the number of half-moves made by
        pieces other than pawns.
    positions (list): A list of all hashed board positions.
    state (int): Indicates the state of the game:
        -1 - ongoing, 0 - white win, 1 - black win, 2 - draw
    scores (list): The total value of opponent pieces captured by white
        and black respectively.
    """

    def __init__(self):
        self.board = board.Board()
        self.check = False  # if the side to move is in check
        self.hashing = hashing.Hashing()
        self.half_move_count = 0
        self.positions = []
        self.state = -1  # -1 = ongoing, 0 = white win, 1 = black win, 2 = draw
        self.scores = [0, 0]  # white, black

    def update_game_state(self, move_string):
        """Updates the state of the game after a move is submitted. Returns False if there is no change."""
        if self.state != -1:
            return False

        move = lan.convert_lan_to_move(move_string, self.board)

        if not move:
            return False

        if move.legal(self.board):
            move.make_move(self.board)
        else:
            return False

        if move.capture:
            self.scores[
                int(not self.board.side_to_move.value)
            ] += self.board.captured_pieces[-1].value
            self.half_move_count = 0

        position = self.hashing.zobrist_hash(self.board)
        self.positions.append(position)

        if self.positions.count(position) == 5:  # fivefold repetition
            self.state = 2
            return True

        elif move.piece_type.symbol == "p":
            self.half_move_count = 0
        else:
            self.half_move_count += 1

        if self.half_move_count == 100:  # fifty move rule
            self.state = 2
            return True

        self.check = mg.in_check(self.board)
        moves = []

        for i in range(8):
            for j in range(8):
                moves.extend(mg.all_moves_from_position(self.board, (i, j)))

        if not moves:
            if self.check:
                self.state = int(
                    self.board.side_to_move == attrs.Colour.WHITE
                )  # checkmate
                return True
            else:
                self.state = 2  # stalemate
                return True

        return True
