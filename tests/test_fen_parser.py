import unittest

from chess_engine import board, constants as cs, fen_parser as fp


class TestFenParser(unittest.TestCase):
    @staticmethod
    def validate_piece_list(bd):
        i = 0x44

        while i < 0xBB:
            square = bd.array[i]
            if square == cs.GD:
                i = (i & 0xF0) + 0x14
            elif square:
                if bd.piece_list[square >> 4] != i:
                    return False
            i += 1

        # fmt: off
        starting_types = [
            cs.WR, cs.WN, cs.WB, cs.WQ, cs.WK, cs.WB, cs.WN, cs.WR,
            cs.BR, cs.BN, cs.BB, cs.BQ, cs.BK, cs.BB, cs.BN, cs.BR,
        ]
        # fmt: on

        for i in range(8):
            if bd.piece_list[i] != -1:
                pos = bd.piece_list[i]
                piece = bd.array[pos]
                p_type = starting_types[i]

                if piece != p_type | (i << 4):
                    return False

            if bd.piece_list[cs.SIDE_OFFSET + i] != -1:
                pos = bd.piece_list[cs.SIDE_OFFSET + i]
                piece = bd.array[pos]
                p_type = starting_types[8 + i]

                if piece != p_type | ((cs.SIDE_OFFSET + i) << 4):
                    return False

        return True

    def test_fen_to_board_returns_starting_position(self):
        # ARRANGE
        test_board_1 = board.Board()
        b_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # ACT
        test_board_2 = fp.fen_to_board(b_string)

        # ASSERT
        self.assertEqual(test_board_1.halfmove_clock, test_board_2.halfmove_clock)

    def test_fen_to_board_returns_valid_position_1(self):
        # ARRANGE
        # fmt: off
        arr = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.WR, cs.NL, cs.NL, cs.NL, cs.WK, cs.NL, cs.NL, cs.WR, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.WP, cs.WP, cs.WP, cs.WB, cs.WB, cs.WP, cs.WP, cs.WP, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.WN, cs.NL, cs.NL, cs.WQ, cs.NL, cs.BP, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.BP, cs.NL, cs.NL, cs.WP, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.WP, cs.WN, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.BB, cs.BN, cs.NL, cs.NL, cs.BP, cs.BN, cs.BP, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.BP, cs.NL, cs.BP, cs.BP, cs.BQ, cs.BP, cs.BB, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.BR, cs.NL, cs.NL, cs.NL, cs.BK, cs.NL, cs.NL, cs.BR, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]

        # fmt: on
        test_board_1 = board.Board(arr=arr)

        # ACT
        test_board_2 = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ASSERT
        self.assertEqual(test_board_1.to_fen(), test_board_2.to_fen())

    def test_fen_to_board_returns_valid_position_2(self):
        # ARRANGE
        # fmt: off
        arr = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.WN, cs.NL, cs.WN, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.NL, cs.WK, cs.BP, cs.BP, cs.BP, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.WP, cs.WP, cs.WP, cs.BK, cs.NL, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.BN, cs.NL, cs.BN, cs.NL, cs.NL, cs.NL, cs.NL, cs.NL, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, cs.GD, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        # fmt: on
        test_board_1 = board.Board(arr=arr, black=1, cr=[False, False, False, False])

        # ACT
        test_board_2 = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ASSERT
        self.assertEqual(test_board_1.to_fen(), test_board_2.to_fen())

    def test_fen_to_board_identifies_contact_check(self):
        # ACT
        test_board = fp.fen_to_board(
            "rnbqkbnr/ppp2Qpp/8/3pp3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
        )

        # ASSERT
        self.assertEqual(test_board.check, 1)

    def test_fen_to_board_identifies_distant_check(self):
        # ACT
        test_board = fp.fen_to_board(
            "r1bqkbnr/ppp3pp/n2P4/8/2B4P/4R3/PPPP1PP1/RNB1K1N1 b Q - 0 9"
        )

        # ASSERT
        self.assertEqual(test_board.check, 2)

    def test_fen_to_board_identifies_discovered_check(self):
        # ACT
        test_board = fp.fen_to_board(
            "rnbq1bnr/ppp2kpp/3P4/8/2B1p3/8/PPPP1PPP/RNB1K1NR b KQ - 0 6"
        )

        # ASSERT
        self.assertEqual(test_board.check, 2)

    def test_fen_to_board_identifies_double_check(self):
        # ACT
        test_board = fp.fen_to_board("rnbqkbn1/pp6/8/8/4Kr2/8/PP4b1/R3Q1BR w - - 1 2")

        # ASSERT
        self.assertEqual(test_board.check, 3)

    def test_fen_to_board_identifies_double_distant_check(self):
        # ACT
        test_board = fp.fen_to_board(
            "r5k1/ppp3p1/3pb3/7p/8/5r1K/PB3bPP/RN1Q3R w - - 2 21"
        )

        # ASSERT
        self.assertEqual(test_board.check, 3)

    def test_fen_to_board_identifies_en_passant_discovered_check(self):
        # ACT
        test_board = fp.fen_to_board(
            "4B1kr/p4p2/6pb/2Bp4/2pPq3/1PP2pP1/P2K4/RN1Q4 w - - 0 29"
        )

        # ASSERT
        self.assertEqual(test_board.check, 2)

    def test_fen_to_board_identifies_en_passant_double_check(self):
        # ACT
        test_board = fp.fen_to_board(
            "r1bq1r2/pp2n3/4N1Pk/3pPp2/1b1n2Q1/2N5/PP3PP1/R1B1K2R b KQ - 0 15"
        )

        # ASSERT
        self.assertEqual(test_board.check, 3)

    def test_fen_to_board_does_not_set_check_when_pawn_is_pinned(self):
        # ACT
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/1B1PN3/1p2P3/2N2Q1p/PPPB1PPP/R3K2R b KQkq - 1 1"
        )

        # ASSERT
        self.assertEqual(test_board.check, 0)

    def test_fen_to_board_identifies_distant_rook_check(self):
        # ACT
        test_board = fp.fen_to_board("4k2r/8/8/8/8/8/8/R1r1K2R w KQk - 1 2")

        # ASSERT
        self.assertEqual(test_board.check, 2)

    def test_get_piece_list_on_starting_position(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)
        self.assertEqual(test_board.piece_list, cs.STARTING_PIECE_LIST)

    def test_get_piece_list_on_valid_position_1(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_get_piece_list_on_valid_position_2(self):
        # ARRANGE
        test_board = fp.fen_to_board("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1")

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_get_piece_list_on_valid_position_3(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "4B1kr/p4p2/6pb/2Bp4/2pPq3/1PP2pP1/P2K4/RN1Q4 w - - 0 29"
        )

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_get_piece_list_on_double_check_position(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r5k1/ppp3p1/3pb3/7p/8/5r1K/PB3bPP/RN1Q3R w - - 2 21"
        )

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_get_piece_list_on_distant_check_position(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/ppp3pp/n2P4/8/2B4P/4R3/PPPP1PP1/RNB1K1N1 b Q - 0 9"
        )

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_get_piece_list_for_en_passant_position(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppp1ppp/p7/3Pp3/8/8/PPP1PPPP/RNBQKBNR w KQkq e6 0 5"
        )

        # ACT
        valid = TestFenParser.validate_piece_list(test_board)

        # ASSERT
        self.assertTrue(valid)
