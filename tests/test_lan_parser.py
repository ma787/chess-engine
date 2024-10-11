import unittest

from chess_engine import board, lan_parser as lp, move


class TestLanParser(unittest.TestCase):
    def test_convert_move_to_lan_converts_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x10, 0x20)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "a2-a3")
