import unittest

from chess_engine.move_generation import *


class TestMoveGeneration(unittest.TestCase):
    def test_in_check_identifies_check(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][5], test_board, (1, 5), (2, 5)).make_move()
        Move(test_board.array[6][4], test_board, (6, 4), (5, 4)).make_move()
        Move(test_board.array[1][6], test_board, (1, 6), (3, 6)).make_move()
        test_move = Move(test_board.array[7][3], test_board, (7, 3), (3, 7))

        # ACT
        test_move.make_move()
        valid = in_check(test_board)

        # ASSERT
        self.assertTrue(valid)
