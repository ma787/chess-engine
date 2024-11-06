import unittest

from chess_engine import board, constants as cs


class TestBoard(unittest.TestCase):
    def test_of_fen_returns_starting_position(self):
        # ARRANGE
        test_board_1 = board.Board()
        b_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # ACT
        test_board_2 = board.Board.of_fen(b_string)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_of_fen_returns_valid_position_1(self):
        # ARRANGE
        # fmt: off
        arr = [
            cs.R, 0, 0, 0, cs.K, 0, 0, cs.R, 0, 0, 0, 0, 0, 0, 0, 0,
            cs.P, cs.P, cs.P, cs.B, cs.B, cs.P, cs.P, cs.P, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, cs.N, 0, 0, cs.Q, 0, cs.p, 0, 0, 0, 0, 0, 0, 0, 0,
            0, cs.p, 0, 0, cs.P, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, cs.P, cs.N, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            cs.b, cs.n, 0, 0, cs.p, cs.n, cs.p, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            cs.p, 0, cs.p, cs.p, cs.q, cs.p, cs.b, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            cs.r, 0, 0, 0, cs.k, 0, 0, cs.r, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        # fmt: on
        test_board_1 = board.Board(arr=arr)

        # ACT
        test_board_2 = board.Board.of_fen(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ASSERT
        self.assertEqual(test_board_1.array, test_board_2.array)

    def test_of_fen_returns_valid_position_2(self):
        # ARRANGE
        arr = [0 for _ in range(128)]
        arr[5:8] = [cs.N, 0, cs.N]
        arr[20:24] = [cs.K, cs.p, cs.p, cs.p]
        arr[96:100] = [cs.P, cs.P, cs.P, cs.k]
        arr[112:115] = [cs.n, 0, cs.n]
        test_board_1 = board.Board(arr=arr, black=1, cr=[False, False, False, False])

        # ACT
        test_board_2 = board.Board.of_fen("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_to_fen_returns_correct_start_string(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(
            test_string, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    def test_to_fen_returns_correct_string_for_valid_position_1(self):
        # ARRANGE
        b_string = (
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )
        test_board = board.Board.of_fen(b_string)

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_to_fen_returns_correct_string_for_valid_position_2(self):
        # ARRANGE
        b_string = "n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1"
        test_board = board.Board.of_fen(b_string)

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_to_fen_preserves_en_passant_target_square(self):
        # ARRANGE
        b_string = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
        test_board = board.Board.of_fen(b_string)

        # ACT
        test_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_find_king_finds_white_king_in_start_position(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        pos = test_board.find_king(cs.WHITE)

        # ASSERT
        self.assertEqual(pos, 0x04)

    def test_find_king_finds_black_king_in_start_position(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        pos = test_board.find_king(cs.BLACK)

        # ASSERT
        self.assertEqual(pos, 0x74)

    def test_find_king_finds_white_king_that_has_moved(self):
        # ARRANGE
        test_board = board.Board.of_fen("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        pos = test_board.find_king(cs.WHITE)

        # ASSERT
        self.assertEqual(pos, 0x14)

    def test_find_king_finds_black_king_that_has_moved(self):
        # ARRANGE
        test_board = board.Board.of_fen("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        pos = test_board.find_king(cs.BLACK)

        # ASSERT
        self.assertEqual(pos, 0x63)
