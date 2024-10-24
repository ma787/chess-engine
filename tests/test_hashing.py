import unittest

from chess_engine import board, constants as cs, hashing as hsh, move


class TestHashing(unittest.TestCase):
    def test_update_hash_updates_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x10, 0x20)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_piece_move(self):
        # ARRANGE
        test_board = board.Board()
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x01, 0x22)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/p1pppppp/8/1p6/8/2N5/PPPPPPPP/R1BQKBNR w KQkq b5 0 3"
        )
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x22, 0x41, capture=True)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_file(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppppppp1/7p/2P5/8/8/PP1PPPPP/RNBQKBNR b KQkq - 0 4"
        )
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x61, 0x41)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/p1pppppp/8/8/Pp6/6PP/1PPPPP2/RNBQKBNR b KQkq a4 0 6"
        )
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x31, 0x20, capture=True)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)

    def test_update_hash_updates_promotion(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pPpppp2/p1n5/6pp/8/4P3/P1PP1PPP/RNBQK1NR w KQkq - 0 13"
        )
        first_hash = hsh.zobrist_hash(test_board)
        test_move = move.encode_move(0x61, 0x71, promotion=cs.QUEEN)

        # ACT
        first_hash = hsh.update_hash(first_hash, test_move, test_board)
        move.make_move(test_move, test_board)
        second_hash = hsh.zobrist_hash(test_board)

        # ASSERT
        self.assertEqual(first_hash, second_hash)
