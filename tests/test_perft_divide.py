import unittest


from chess_engine import board, perft_divide as pd


class TestPerftDivide(unittest.TestCase):
    def test_perft_1_equals_20(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 20)

    def test_perft_2_equals_400(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 400)

    def test_perft_3_equals_8902(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 8902)

    def test_perft_4_equals_197281(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = pd.perft(test_board, 4)

        # ASSERT
        self.assertEqual(n, 197281)

    def test_perft_1_from_test_position_equals_48(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 48)

    def test_perft_2_from_test_position_equals_2039(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 2039)

    def test_perft_3_from_test_position_equals_97862(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 97862)

    def test_perft_1_from_promotion_test_position_equals_24(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 24)

    def test_perft_2_from_promotion_test_position_equals_496(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 496)

    def test_perft_3_from_promotion_test_position_equals_9483(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 9483)
