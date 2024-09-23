import unittest

from chess_engine import board


class TestBoard(unittest.TestCase):
    def test_of_string_returns_starting_position(self):
        # ARRANGE
        test_board_1 = board.Board()
        b_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # ACT
        test_board_2 = board.Board.of_string(b_string)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_of_string_returns_valid_position_1(self):
        # ARRANGE
        test_board_1 = board.Board(
            arr=[
                [6, 0, 0, 0, 2, 0, 0, 6],
                [4, 4, 4, 1, 1, 4, 4, 4],
                [0, 0, 3, 0, 0, 5, 0, -4],
                [0, -4, 0, 0, 4, 0, 0, 0],
                [0, 0, 0, 4, 3, 0, 0, 0],
                [-1, -3, 0, 0, -4, -3, -4, 0],
                [-4, 0, -4, -4, -5, -4, -1, 0],
                [-6, 0, 0, 0, -2, 0, 0, -6],
            ],
        )

        # ACT
        test_board_2 = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_of_string_returns_valid_position_2(self):
        # ARRANGE
        test_board_1 = board.Board(
            arr=[
                [0, 0, 0, 0, 0, 3, 0, 3],
                [0, 0, 0, 0, 2, -4, -4, -4],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [4, 4, 4, -2, 0, 0, 0, 0],
                [-3, 0, -3, 0, 0, 0, 0, 0],
            ],
            black=True,
            cr=0,
        )

        # ACT
        test_board_2 = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_to_string_returns_correct_start_string(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        test_string = test_board.to_string()

        # ASSERT
        self.assertEqual(
            test_string, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    def test_to_string_returns_correct_string_for_valid_position_1(self):
        # ARRANGE
        b_string = (
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )
        test_board = board.Board.of_string(b_string)

        # ACT
        test_string = test_board.to_string()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_to_string_returns_correct_string_for_valid_position_2(self):
        # ARRANGE
        b_string = "n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1"
        test_board = board.Board.of_string(b_string)

        # ACT
        test_string = test_board.to_string()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_find_king_finds_white_king_in_start_position(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        pos = test_board.find_king(False)

        # ASSERT
        self.assertEqual(pos, (0, 4))

    def test_find_king_finds_black_king_in_start_position(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        pos = test_board.find_king(True)

        # ASSERT
        self.assertEqual(pos, (7, 4))

    def test_find_king_finds_white_king_that_has_moved(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        pos = test_board.find_king(False)

        # ASSERT
        self.assertEqual(pos, (1, 4))

    def test_find_king_finds_black_king_that_has_moved(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        pos = test_board.find_king(True)

        # ASSERT
        self.assertEqual(pos, (6, 3))
