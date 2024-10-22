import unittest

from chess_engine import board, constants as cs, move, move_generation as mg


class TestMoveGeneration(unittest.TestCase):
    def test_in_check_identifies_check(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/pppp1ppp/4p3/8/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g4 0 4"
        )
        test_move = move.encode_move(0x73, 0x37)

        # ACT
        move.make_move(test_move, test_board)
        valid = mg.in_check(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_all_pseudo_legal_moves_preserves_board(self):
        # ARRANGE
        test_string = "rnbqkbnr/pp2pppp/2p5/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d5 0 5"
        test_board = board.Board.of_string(test_string)

        # ACT
        mg.all_pseudo_legal_moves(test_board)
        b_string = test_board.to_string()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_all_pseudo_legal_moves_preserves_board_2(self):
        # ARRANGE
        test_string = "rnbqkbnr/1pppp1pp/8/p4p2/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq f5 0 5"
        test_board = board.Board.of_string(test_string)

        # ACT
        mg.all_pseudo_legal_moves(test_board)
        b_string = test_board.to_string()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_all_pseudo_legal_moves_preserves_board_3(self):
        # ARRANGE
        test_string = (
            "r1bqkbnr/1pp1pppp/8/p2pP3/3n4/N1P5/PP1P1PPP/R1BQKBNR w KQkq d5 0 9"
        )
        test_board = board.Board.of_string(test_string)

        # ACT
        mg.all_pseudo_legal_moves(test_board)
        b_string = test_board.to_string()

        # ASSERT
        self.assertEqual(b_string, test_string)

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
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/2n5/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x52, 0x33, capture=True)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_move_in_check(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnb1kbnr/pppp1ppp/8/8/4p1Pq/4PP2/PPPP3P/RNBQKBNR w KQkq - 1 7"
        )
        test_move = move.encode_move(0x25, 0x34, capture=True)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_true_for_legal_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkb1r/pppppppp/8/8/8/3Bn2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_false_for_illegal_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/1ppppppp/p7/8/3P4/2NnB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = mg.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)
