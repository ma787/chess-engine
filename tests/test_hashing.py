import unittest

from chess_engine import board, hashing, move


class TestHashing(unittest.TestCase):
    def test_update_hash_updates_pawn_move(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)
        test_move = move.encode_move((1, 0), (2, 0))

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_piece_move(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)
        test_move = move.encode_move((0, 1), (2, 2))

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_capture(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        first_move = move.encode_move((0, 1), (2, 2))
        first_hash = z_hash.update_hash(first_hash, first_move, test_board)
        move.make_move(first_move, test_board)

        second_move = move.encode_move((6, 1), (4, 1))
        first_hash = z_hash.update_hash(first_hash, second_move, test_board)
        move.make_move(second_move, test_board)

        test_move = move.encode_move((2, 2), (4, 1), capture=True)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_file(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.encode_move((1, 2), (3, 2)),
            move.encode_move((6, 7), (5, 7)),
            move.encode_move((3, 2), (4, 2)),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            move.make_move(m, test_board)

        test_move = move.encode_move((6, 1), (4, 1))

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_capture(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.encode_move((1, 7), (2, 7)),
            move.encode_move((6, 1), (4, 1)),
            move.encode_move((1, 6), (2, 6)),
            move.encode_move((4, 1), (3, 1)),
            move.encode_move((1, 0), (3, 0)),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            move.make_move(m, test_board)
            x_hash = z_hash.zobrist_hash(test_board)
            self.assertEqual(first_hash, x_hash)

        test_move = move.encode_move((3, 1), (2, 0), capture=True)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_queen_side_castle(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.encode_move((1, 3), (3, 3)),
            move.encode_move((6, 0), (5, 0)),
            move.encode_move((0, 2), (2, 4)),
            move.encode_move((6, 1), (5, 1)),
            move.encode_move((0, 3), (2, 3)),
            move.encode_move((6, 2), (5, 2)),
            move.encode_move((0, 1), (2, 2)),
            move.encode_move((6, 3), (5, 3)),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            move.make_move(m, test_board)

        test_move = move.encode_move((0, 4), (0, 2), castling=2)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_king_side_castle(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.encode_move((1, 4), (2, 4)),
            move.encode_move((6, 0), (5, 0)),
            move.encode_move((0, 5), (2, 3)),
            move.encode_move((6, 1), (5, 1)),
            move.encode_move((0, 6), (2, 7)),
            move.encode_move((6, 2), (5, 2)),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            move.make_move(m, test_board)

        test_move = move.encode_move((0, 4), (0, 6), castling=1)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_promotion(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.encode_move((1, 1), (3, 1)),
            move.encode_move((7, 1), (5, 2)),
            move.encode_move((1, 4), (2, 4)),
            move.encode_move((6, 7), (5, 7)),
            move.encode_move((0, 5), (5, 0)),
            move.encode_move((6, 1), (5, 0), capture=True),
            move.encode_move((3, 1), (4, 1)),
            move.encode_move((5, 7), (4, 7)),
            move.encode_move((4, 1), (5, 1)),
            move.encode_move((6, 6), (5, 6)),
            move.encode_move((5, 1), (6, 1)),
            move.encode_move((5, 6), (4, 6)),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            move.make_move(m, test_board)

        test_move = move.encode_move((6, 1), (7, 1), promotion=5)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)
