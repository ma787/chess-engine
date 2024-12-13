import unittest


from chess_engine import board, fen_parser as fp, perft_divide as pd


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

    def test_perft_5_equals_4865609(self):
        # ARRANGE
        test_board = board.Board()

        # ACT
        n = pd.perft(test_board, 5)

        # ASSERT
        self.assertEqual(n, 4865609)

    def test_perft_1_from_test_position_equals_48(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 48)

    def test_perft_2_from_test_position_equals_2039(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 2039)

    def test_perft_3_from_test_position_equals_97862(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 97862)

    def test_perft_1_in_check_from_test_position_equals_4(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q2/PPPBBPpP/R4K1R w kq - 0 2"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 4)

    def test_perft_1_from_pinned_pawn_equals_39(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/1B1PN3/1p2P3/2N2Q1p/PPPB1PPP/R3K2R b KQkq - 1 1"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 39)

    def test_perft_1_from_test_position_after_move_equals_36(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/Bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPB1PPP/R3K2R b KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 36)

    def test_perft_1_from_test_position_after_move_2_equals_44(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/P1N2Q1p/1PPBBPPP/R3K2R b KQkq - 0 1"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 44)

    def test_perft_1_from_test_position_after_two_moves_equals_46(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/4P3/1pN2Q1p/PPPBBPPP/R3KR2 w Qkq - 0 2"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 46)

    def test_perft_1_from_promotion_test_position_equals_24(self):
        # ARRANGE
        test_board = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 24)

    def test_perft_2_from_promotion_test_position_equals_496(self):
        # ARRANGE
        test_board = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 496)

    def test_perft_1_from_promotion_test_position_2_equals_21(self):
        # ARRANGE
        test_board = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kp1p/5N1b w - - 0 2")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 21)

    def test_perft_3_from_promotion_test_position_equals_9483(self):
        # ARRANGE
        test_board = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 9483)

    def test_perft_1_from_check_test_position_equals_1(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "1nbqkbnr/r2pp2p/ppp2pB1/4P2Q/3P4/2N5/PPP2PPP/R1B1K1NR b KQk - 0 7"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 1)

    def test_perft_1_again_equals_21(self):
        # ARRANGE
        test_board = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kp1p/5N1q w - - 0 2")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 21)

    def test_perft_3_from_black_position_equals_32675(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppp1ppp/8/8/4P3/2p2N2/PPP2PPP/R1BQKB1R b KQkq - 1 4"
        )

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 32675)

    def test_perft_2_from_white_position_equals_1424(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppp1ppp/8/8/4P3/5N2/PpP2PPP/R1BQKB1R w KQkq - 0 5"
        )

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 1424)

    def test_perft_1_from_white_position_after_move_equals_41(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppp1ppp/8/8/4P3/5N2/PpP1QPPP/R1B1KB1R b KQkq - 1 5"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 41)

    def test_perft_2_from_ep_pinned_pawn_equals_117(self):
        # ARRANGE
        test_board = fp.fen_to_board("8/8/8/8/k3p2Q/8/3P4/3K4 w - - 0 1")

        # ACT
        n = pd.perft(test_board, 2)

        # ASSERT
        self.assertEqual(n, 117)

    def test_perft_1_when_ep_pinned_pawn_moves_equals_6(self):
        # ARRANGE
        test_board = fp.fen_to_board("8/8/8/8/k2Pp2Q/8/8/3K4 b - - 0 1")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 6)

    def test_perft_1_from_check_position_equals_4(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbq1bnr/ppppkppp/8/6B1/4P3/2p2N2/PPP2PPP/R2QKB1R b KQ - 3 5"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 4)

    def test_perft_1_from_check_with_multiple_blocks_equals_7(self):
        # ARRANGE
        test_board = fp.fen_to_board("8/K7/5Q2/8/8/8/5b2/7k w - - 0 1")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 7)

    def test_perft_3_from_game_position_equals_13828(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1b1k2r/pppp1ppp/3Pp3/8/3P3N/3P4/PP2BKPP/RNBQ1R2 b k - 0 11"
        )

        # ACT
        n = pd.perft(test_board, 3)

        # ASSERT
        self.assertEqual(n, 13828)

    def test_perft_1_from_pinned_pawn_equals_22(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/4Q3/p7/8/2P5/PP1PPPPP/RNB1KBNR b KQkq - 1 3"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 21)

    def test_perft_1_from_pinned_pawn_2_equals_21(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/8/p7/4Q3/2P5/PP1PPPPP/RNB1KBNR b KQkq - 1 3"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 21)

    def test_perft_1_from_check_position_with_no_king_moves_equals_5(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pp2pppp/2Qp4/8/8/2P5/PP1PPPPP/RNB1KBNR b KQkq - 0 3"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 5)

    def test_perft_1_from_knight_check_position_equals_2(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r2k3r/p1ppqNb1/bn2pQp1/3P4/1p2P3/2N4p/PPPBBPPP/R3K2R b KQ - 0 2"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 2)

    def test_perft_1_from_knight_check_position_2_equals_5(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r4k1r/p1pNqpb1/bn2pnp1/3P4/1p2P3/P1N2Q1p/1PPBBPPP/R3K2R b KQ - 0 2"
        )

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 5)

    def test_perft_1_from_rook_check_position_equals_4(self):
        # ARRANGE
        test_board = fp.fen_to_board("4k2r/8/8/8/8/8/8/R1r1K2R w KQk - 1 2")

        # ACT
        n = pd.perft(test_board, 1)

        # ASSERT
        self.assertEqual(n, 4)
