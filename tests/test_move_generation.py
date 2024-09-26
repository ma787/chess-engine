import unittest

from chess_engine import board, move, move_generation


class TestMoveGeneration(unittest.TestCase):
    def test_in_check_identifies_check(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 5), (2, 5)), test_board)
        move.make_move(move.encode_move((6, 4), (5, 4)), test_board)
        move.make_move(move.encode_move((1, 6), (3, 6)), test_board)
        test_move = move.encode_move((7, 3), (3, 7))

        # ACT
        move.make_move(test_move, test_board)
        valid = move_generation.in_check(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_all_moves_from_position_preserves_board(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        for bd in (test_board_1, test_board_2):
            move.make_move(move.encode_move((1, 4), (3, 4)), bd)
            move.make_move(move.encode_move((6, 2), (5, 2)), bd)
            move.make_move(move.encode_move((3, 4), (4, 4)), bd)
            move.make_move(move.encode_move((6, 3), (4, 3)), bd)

        # ACT
        for i in range(8):
            for j in range(8):
                move_generation.all_moves_from_position(test_board_1, (i, j))

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_all_moves_from_position_preserves_board_2(self):
        # ARRANGE
        b_string = "rnbqkbnr/1pppp1pp/8/p4p2/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq f5 0 5"
        test_board_1 = board.Board.of_string(b_string)
        test_board_2 = board.Board.of_string(b_string)

        # ACT
        for i in range(8):
            for j in range(8):
                move_generation.all_moves_from_position(test_board_1, (i, j))

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_all_moves_from_position_preserves_board_3(self):
        # ARRANGE
        b_string = "r1bqkbnr/1pp1pppp/8/p2pP3/3n4/N1P5/PP1P1PPP/R1BQKBNR w KQkq d5 0 9"
        test_board_1 = board.Board.of_string(b_string)
        test_board_2 = board.Board.of_string(b_string)

        # ACT
        for i in range(8):
            for j in range(8):
                move_generation.all_moves_from_position(test_board_1, (i, j))

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

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

    def test_perft_1_from_test_position_equals_48(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = move_generation.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 48)

    def test_perft_2_from_test_position_equals_2039(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = move_generation.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 2039)

    def test_perft_3_from_test_position_equals_97862(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = move_generation.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 97862)

    def test_perft_1_from_promotion_test_position_equals_24(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = move_generation.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 24)

    def test_perft_2_from_promotion_test_position_equals_496(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = move_generation.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 496)

    def test_perft_3_from_promotion_test_position_equals_9483(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = move_generation.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 9483)
