import unittest

from chess_engine import board, attributes as attrs, hashing, move, pieces


class TestHashing(unittest.TestCase):
    def test_update_hash_updates_pawn_move(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)
        test_move = move.Move((1, 0), (2, 0), pieces.Pawn)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_piece_move(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)
        test_move = move.Move((0, 1), (2, 2), pieces.Knight)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_capture(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        first_move = move.Move((0, 1), (2, 2), pieces.Knight)
        first_hash = z_hash.update_hash(first_hash, first_move, test_board)
        first_move.make_move(test_board)

        second_move = move.Move((6, 1), (4, 1), pieces.Pawn)
        first_hash = z_hash.update_hash(first_hash, second_move, test_board)
        second_move.make_move(test_board)

        test_move = move.Move((2, 2), (4, 1), pieces.Knight, capture=True)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_file(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.Move((1, 2), (3, 2), pieces.Pawn),
            move.Move((6, 7), (5, 7), pieces.Pawn),
            move.Move((3, 2), (4, 2), pieces.Pawn),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            m.make_move(test_board)

        test_move = move.Move((6, 1), (4, 1), pieces.Pawn)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_capture(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.Move((1, 7), (2, 7), pieces.Pawn),
            move.Move((6, 1), (4, 1), pieces.Pawn),
            move.Move((1, 6), (2, 6), pieces.Pawn),
            move.Move((4, 1), (3, 1), pieces.Pawn),
            move.Move((1, 0), (3, 0), pieces.Pawn),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            m.make_move(test_board)
            x_hash = z_hash.zobrist_hash(test_board)
            self.assertEqual(first_hash, x_hash)

        test_move = move.Move((3, 1), (2, 0), pieces.Pawn, capture=True)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_queen_side_castle(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.Move((1, 3), (3, 3), pieces.Pawn),
            move.Move((6, 0), (5, 0), pieces.Pawn),
            move.Move((0, 2), (2, 4), pieces.Bishop),
            move.Move((6, 1), (5, 1), pieces.Pawn),
            move.Move((0, 3), (2, 3), pieces.Queen),
            move.Move((6, 2), (5, 2), pieces.Pawn),
            move.Move((0, 1), (2, 2), pieces.Knight),
            move.Move((6, 3), (5, 3), pieces.Pawn),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            m.make_move(test_board)

        test_move = move.Move(
            (0, 4), (0, 2), pieces.King, castling=attrs.Castling.QUEEN_SIDE
        )

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_king_side_castle(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.Move((1, 4), (2, 4), pieces.Pawn),
            move.Move((6, 0), (5, 0), pieces.Pawn),
            move.Move((0, 5), (2, 3), pieces.Bishop),
            move.Move((6, 1), (5, 1), pieces.Pawn),
            move.Move((0, 6), (2, 7), pieces.Knight),
            move.Move((6, 2), (5, 2), pieces.Pawn),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            m.make_move(test_board)

        test_move = move.Move(
            (0, 4), (0, 6), pieces.King, castling=attrs.Castling.KING_SIDE
        )

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_promotion(self):
        # ARRANGE
        z_hash = hashing.Hashing()
        test_board = board.Board()
        first_hash = z_hash.zobrist_hash(test_board)

        moves = [
            move.Move((1, 1), (3, 1), pieces.Pawn),
            move.Move((7, 1), (5, 2), pieces.Knight),
            move.Move((1, 4), (2, 4), pieces.Pawn),
            move.Move((6, 7), (5, 7), pieces.Pawn),
            move.Move((0, 5), (5, 0), pieces.Bishop),
            move.Move((6, 1), (5, 0), pieces.Pawn, capture=True),
            move.Move((3, 1), (4, 1), pieces.Pawn),
            move.Move((5, 7), (4, 7), pieces.Pawn),
            move.Move((4, 1), (5, 1), pieces.Pawn),
            move.Move((6, 6), (5, 6), pieces.Pawn),
            move.Move((5, 1), (6, 1), pieces.Pawn),
            move.Move((5, 6), (4, 6), pieces.Pawn),
        ]

        for m in moves:
            first_hash = z_hash.update_hash(first_hash, m, test_board)
            m.make_move(test_board)

        test_move = move.Move((6, 1), (7, 1), pieces.Pawn, promotion=pieces.Queen)

        # ACT
        first_hash = z_hash.update_hash(first_hash, test_move, test_board)
        test_move.make_move(test_board)
        second_hash = z_hash.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)
