import unittest
from chess_engine.hashing import Hashing
from chess_engine.move import Move
from chess_engine.board import Board
from chess_engine.castling import Castling
from chess_engine.pieces import *


class TestHashing(unittest.TestCase):
    def test_update_hash_updates_pawn_move(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)
        test_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0))

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_piece_move(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)
        test_move = Move(test_board.array[0][1], test_board, (0, 1), (2, 2))

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_capture(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            Move(test_board.array[0][1], test_board, (0, 1), (2, 2)),
            Move(test_board.array[6][1], test_board, (6, 1), (4, 1))
        ]

        for move in moves:
            first_hash = z_hash.update_hash(first_hash, move)
            move.make_move()

        test_move = Move(test_board.array[2][2], test_board, (2, 2), (4, 1), capture=True)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_capture(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)

        pairs = [((1, 2), (3, 2)), ((6, 7), (5, 7)), ((3, 2), (4, 2)), ((6, 1), (4, 1))]

        for pair in pairs:
            move = Move(test_board.array[pair[0][0]][pair[0][1]], test_board, pair[0], pair[1])
            first_hash = z_hash.update_hash(first_hash, move)
            move.make_move()

        test_move = Move(test_board.array[4][2], test_board, (4, 2), (5, 1), capture=True)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_queen_side_castle(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            Move(test_board.array[1][3], test_board, (1, 3), (3, 3)),
            Move(test_board.array[6][0], test_board, (6, 0), (5, 0)),
            Move(test_board.array[0][2], test_board, (0, 2), (2, 4)),
            Move(test_board.array[6][1], test_board, (6, 1), (5, 1)),
            Move(test_board.array[0][3], test_board, (0, 3), (2, 3)),
            Move(test_board.array[6][2], test_board, (6, 2), (5, 2)),
            Move(test_board.array[0][1], test_board, (0, 1), (2, 2)),
            Move(test_board.array[6][3], test_board, (6, 3), (5, 3))
        ]

        for move in moves:
            first_hash = z_hash.update_hash(first_hash, move)
            move.make_move()

        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 2), castling=Castling.QUEEN_SIDE)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_king_side_castle(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            Move(test_board.array[1][4], test_board, (1, 4), (2, 4)),
            Move(test_board.array[6][0], test_board, (6, 0), (5, 0)),
            Move(test_board.array[0][5], test_board, (0, 5), (2, 3)),
            Move(test_board.array[6][1], test_board, (6, 1), (5, 1)),
            Move(test_board.array[0][6], test_board, (0, 6), (2, 7)),
            Move(test_board.array[6][2], test_board, (6, 2), (5, 2))
        ]

        for move in moves:
            first_hash = z_hash.update_hash(first_hash, move)
            move.make_move()

        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 6), castling=Castling.KING_SIDE)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_promotion(self):
        # ARRANGE
        z_hash = Hashing()
        test_board = Board()
        first_hash = z_hash.zobrist_hash(test_board)

        pairs = [((1, 1), (3, 1)), ((7, 1), (5, 2)), ((1, 4), (2, 4)), ((6, 7), (5, 7)), ((0, 5), (5, 0)),
                 ((6, 1), (5, 0), True), ((3, 1), (4, 1)), ((5, 7), (4, 7)), ((4, 1), (5, 1)), ((6, 6), (5, 6)),
                 ((5, 1), (6, 1)), ((5, 6), (4, 6))]

        for pair in pairs:
            if len(pair) == 3:
                move = Move(test_board.array[pair[0][0]][pair[0][1]], test_board, pair[0], pair[1], capture=pair[2])
            else:
                move = Move(test_board.array[pair[0][0]][pair[0][1]], test_board, pair[0], pair[1])

            first_hash = z_hash.update_hash(first_hash, move)
            move.make_move()

        test_move = Move(test_board.array[6][1], test_board, (6, 1), (7, 1), promotion=Queen)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move)
        test_move.make_move()
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)
