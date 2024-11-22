import unittest

from chess_engine import board, fen_parser as fp


class TestBoard(unittest.TestCase):
    def test_to_fen_returns_correct_start_string(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(
            test_string, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    def test_to_fen_returns_correct_string_for_valid_position_1(self):
        # ARRANGE
        b_string = (
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )
        test_board = fp.fen_to_board(b_string)

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_to_fen_returns_correct_string_for_valid_position_2(self):
        # ARRANGE
        b_string = "n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1"
        test_board = fp.fen_to_board(b_string)

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_to_fen_preserves_en_passant_target_square(self):
        # ARRANGE
        b_string = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
        test_board = fp.fen_to_board(b_string)

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)
