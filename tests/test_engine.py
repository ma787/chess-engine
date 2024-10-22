import math
import unittest

from chess_engine import board, engine


class TestEngine(unittest.TestCase):
    def test_alpha_beta_search_position_1(self):
        # ARRANGE
        b_string = "r1b1k2r/pppp1ppp/3Pp3/8/3P3N/3P4/PP2BKPP/RNBQ1R2 b k - 0 11"
        test_board_1 = board.Board.of_string(b_string)
        test_board_2 = board.Board.of_string(b_string)
        eng = engine.Engine(True)

        # ACT
        eng.alpha_beta_search(test_board_1, -math.inf, math.inf, 3)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)
