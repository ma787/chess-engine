import unittest

from chess_engine import board, constants as cs, move, move_generation as mg


class TestMoveGeneration(unittest.TestCase):
    def test_in_check_identifies_check(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "rnbqkbnr/pppp1ppp/4p3/8/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g3 0 4"
        )

        # ACT
        move.make_move("d8h4", test_board)
        valid = mg.in_check(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        start, dest, promotion = move.get_info("d2d3")

        # ACT
        valid = mg.legal(test_board, start, dest, 0, promotion)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_capture(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "r1bqkbnr/pppppppp/2n5/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 4"
        )
        start, dest, promotion = move.get_info("c6d4")

        # ACT
        valid = mg.legal(test_board, start, dest, 0, promotion)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_move_in_check(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "rnb1kbnr/pppp1ppp/8/8/4p1Pq/4PP2/PPPP3P/RNBQKBNR w KQkq - 1 7"
        )
        start, dest, promotion = move.get_info("f3e4")

        # ACT
        valid = mg.legal(test_board, start, dest, 0, promotion)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_true_for_legal_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        start, dest, promotion = move.get_info("e1c1")

        # ACT
        valid = mg.legal(test_board, start, dest, cs.QUEENSIDE, promotion)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        start, dest, promotion = move.get_info("e1g1")

        # ACT
        valid = mg.legal(test_board, start, dest, cs.KINGSIDE, promotion)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "rnbqkb1r/pppppppp/8/8/8/3Bn2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        start, dest, promotion = move.get_info("e1c1")

        # ACT
        valid = mg.legal(test_board, start, dest, cs.QUEENSIDE, promotion)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_false_for_illegal_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "r1bqkbnr/1ppppppp/p7/8/3P4/2NnB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        start, dest, promotion = move.get_info("e1g1")

        # ACT
        valid = mg.legal(test_board, start, dest, cs.KINGSIDE, promotion)

        # ASSERT
        self.assertFalse(valid)

    def test_all_moves_preserves_board(self):
        # ARRANGE
        test_string = "rnbqkbnr/pppp1ppp/8/8/4P3/P4N2/1pP2PPP/R1BQKB1R b KQkq - 1 5"
        test_board = board.Board.of_fen(test_string)

        # ACT
        mg.all_moves(test_board)
        b_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)
