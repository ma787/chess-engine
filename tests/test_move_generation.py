import unittest

from chess_engine import board, move, move_generation as mg


class TestMoveGeneration(unittest.TestCase):
    def test_in_check_identifies_check(self):
        # ARRANGE
        test_board = board.Board.of_fen(
            "rnbqkbnr/pppp1ppp/4p3/8/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g3 0 4"
        )

        # ACT
        move.make_move_from_string("d8h4", test_board)
        valid = mg.in_check(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_all_moves_preserves_board(self):
        # ARRANGE
        test_string = "rnbqkbnr/pppp1ppp/8/8/4P3/P4N2/1pP2PPP/R1BQKB1R b KQkq - 1 5"
        test_board = board.Board.of_fen(test_string)

        # ACT
        mg.all_moves(test_board)
        b_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)
