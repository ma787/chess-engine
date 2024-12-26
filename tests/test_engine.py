import unittest

from chess_engine import engine, fen_parser as fp


class TestEngine(unittest.TestCase):
    def test_find_move_position_1_preserves_board(self):
        # ARRANGE
        b_string = "r1b1k2r/pppp1ppp/3Pp3/8/3P3N/3P4/PP2BKPP/RNBQ1R2 b k - 0 11"
        test_board_1 = fp.fen_to_board(b_string)
        test_board_2 = fp.fen_to_board(b_string)

        # ACT
        m = engine.find_move(test_board_1, 640)

        # ASSERT
        print(m)
        self.assertEqual(test_board_1, test_board_2)
