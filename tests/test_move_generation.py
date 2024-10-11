import unittest

from chess_engine import board, constants as cs, move, move_generation as mg


class TestMoveGeneration(unittest.TestCase):
    def test_square_under_threat_identifies_check(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x15, 0x25), test_board)
        move.make_move(move.encode_move(0x64, 0x54), test_board)
        move.make_move(move.encode_move(0x16, 0x36), test_board)
        test_move = move.encode_move(0x73, 0x37)

        # ACT
        move.make_move(test_move, test_board)
        valid = mg.square_under_threat(
            test_board, test_board.find_king(test_board.black), not test_board.black
        )

        # ASSERT
        self.assertTrue(valid)

    def test_all_pseudo_legal_moves_preserves_board(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        for bd in (test_board_1, test_board_2):
            move.make_move(move.encode_move(0x14, 0x34), bd)
            move.make_move(move.encode_move(0x62, 0x52), bd)
            move.make_move(move.encode_move(0x34, 0x44), bd)
            move.make_move(move.encode_move(0x63, 0x43), bd)

        # ACT
        mg.all_pseudo_legal_moves(test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_all_pseudo_legal_moves_preserves_board_2(self):
        # ARRANGE
        b_string = "rnbqkbnr/1pppp1pp/8/p4p2/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq f5 0 5"
        test_board_1 = board.Board.of_string(b_string)
        test_board_2 = board.Board.of_string(b_string)

        # ACT
        mg.all_pseudo_legal_moves(test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_all_pseudo_legal_moves_preserves_board_3(self):
        # ARRANGE
        b_string = "r1bqkbnr/1pp1pppp/8/p2pP3/3n4/N1P5/PP1P1PPP/R1BQKBNR w KQkq d5 0 9"
        test_board_1 = board.Board.of_string(b_string)
        test_board_2 = board.Board.of_string(b_string)

        # ACT
        mg.all_pseudo_legal_moves(test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_legal_returns_true_for_legal_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x13, 0x23)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x13, 0x23), test_board)
        move.make_move(move.encode_move(0x71, 0x52), test_board)
        move.make_move(move.encode_move(0x23, 0x33), test_board)
        test_move = move.encode_move(0x52, 0x33, capture=True)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_move_in_check(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x64, 0x44), test_board)
        move.make_move(move.encode_move(0x15, 0x25), test_board)
        move.make_move(move.encode_move(0x44, 0x34), test_board)
        move.make_move(move.encode_move(0x16, 0x36), test_board)
        move.make_move(move.encode_move(0x73, 0x37), test_board)
        test_move = move.encode_move(0x25, 0x34, capture=True)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_true_for_legal_queenside_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x05, 0x23), test_board)
        move.make_move(move.encode_move(0x61, 0x51), test_board)
        move.make_move(move.encode_move(0x06, 0x27), test_board)
        move.make_move(move.encode_move(0x62, 0x52), test_board)
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_kingside_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move(0x13, 0x33), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x02, 0x24), test_board)
        move.make_move(move.encode_move(0x61, 0x51), test_board)
        move.make_move(move.encode_move(0x03, 0x23), test_board)
        move.make_move(move.encode_move(0x62, 0x52), test_board)
        move.make_move(move.encode_move(0x01, 0x22), test_board)
        move.make_move(move.encode_move(0x63, 0x53), test_board)
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_queenside_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x76, 0x55), test_board)
        move.make_move(move.encode_move(0x05, 0x23), test_board)
        move.make_move(move.encode_move(0x55, 0x36), test_board)
        move.make_move(move.encode_move(0x06, 0x27), test_board)
        move.make_move(move.encode_move(0x36, 0x24, capture=True), test_board)
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_false_for_illegal_kingside_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move(0x13, 0x33), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
        move.make_move(move.encode_move(0x02, 0x24), test_board)
        move.make_move(move.encode_move(0x50, 0x31), test_board)
        move.make_move(move.encode_move(0x03, 0x23), test_board)
        move.make_move(move.encode_move(0x31, 0x23, capture=True), test_board)
        move.make_move(move.encode_move(0x01, 0x22), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)
