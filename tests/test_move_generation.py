import unittest

from chess_engine import board, move, move_generation


class TestMoveGeneration(unittest.TestCase):
    def test_in_check_identifies_check(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 5), (2, 5)).make_move(test_board)
        move.Move((6, 4), (5, 4)).make_move(test_board)
        move.Move((1, 6), (3, 6)).make_move(test_board)
        test_move = move.Move((7, 3), (3, 7))

        # ACT
        test_move.make_move(test_board)
        valid = move_generation.in_check(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_perft_1_equals_20(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = move_generation.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 20)

    def test_perft_2_equals_400(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = move_generation.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 400)

    def test_perft_3_equals_8902(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = move_generation.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 8902)

    def test_perft_4_equals_197281(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = move_generation.perft(test_board, 4)

        # ASSERT
        self.assertEqual(n, 197281)
