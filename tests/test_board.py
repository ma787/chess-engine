import unittest
import numpy as np

from chess_engine import board, constants as cs


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
        arr = np.zeros(128)
        arr[0:8] = np.array([cs.ROOK, 0, 0, 0, cs.KING, 0, 0, cs.ROOK])
        arr[16:24] = np.array(
            [cs.PAWN, cs.PAWN, cs.PAWN, cs.BISHOP, cs.BISHOP, cs.PAWN, cs.PAWN, cs.PAWN]
        )
        arr[32:40] = np.array([0, 0, cs.KNIGHT, 0, 0, cs.QUEEN, 0, -cs.PAWN])
        arr[48:56] = np.array([0, -cs.PAWN, 0, 0, cs.PAWN, 0, 0, 0])
        arr[64:72] = np.array([0, 0, 0, cs.PAWN, cs.KNIGHT, 0, 0, 0])
        arr[80:88] = np.array(
            [-cs.BISHOP, -cs.KNIGHT, 0, 0, -cs.PAWN, -cs.KNIGHT, -cs.PAWN, 0]
        )
        arr[96:104] = np.array(
            [-cs.PAWN, 0, -cs.PAWN, -cs.PAWN, -cs.QUEEN, -cs.PAWN, -cs.BISHOP, 0]
        )
        arr[112:120] = np.array([-cs.ROOK, 0, 0, 0, -cs.KING, 0, 0, -cs.ROOK])
        test_board_1 = board.Board(arr=arr)

        # ACT
        test_board_2 = board.Board.of_string(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_of_string_returns_valid_position_2(self):
        # ARRANGE
        arr = np.zeros(128)
        arr[0:8] = np.array([0, 0, 0, 0, 0, cs.KNIGHT, 0, cs.KNIGHT])
        arr[16:24] = np.array([0, 0, 0, 0, cs.KING, -cs.PAWN, -cs.PAWN, -cs.PAWN])
        arr[96:104] = np.array([cs.PAWN, cs.PAWN, cs.PAWN, -cs.KING, 0, 0, 0, 0])
        arr[112:120] = np.array([-cs.KNIGHT, 0, -cs.KNIGHT, 0, 0, 0, 0, 0])
        test_board_1 = board.Board(arr=arr, black=True, cr=0)

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
        self.assertEqual(pos, 0x04)

    def test_find_king_finds_black_king_in_start_position(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        pos = test_board.find_king(True)

        # ASSERT
        self.assertEqual(pos, 0x74)

    def test_find_king_finds_white_king_that_has_moved(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        pos = test_board.find_king(False)

        # ASSERT
        self.assertEqual(pos, 0x14)

    def test_find_king_finds_black_king_that_has_moved(self):
        # ARRANGE
        test_board = board.Board.of_string("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        pos = test_board.find_king(True)

        # ASSERT
        self.assertEqual(pos, 0x63)