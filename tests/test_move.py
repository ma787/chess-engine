import unittest

from chess_engine import board, constants as cs, fen_parser as fp, move, utils


class TestMove(unittest.TestCase):
    def test_string_to_int_correctly_extracts_quiet_move(self):
        # ARRANGE
        test_attrs = (utils.string_to_coord("f2"), utils.string_to_coord("f4"), 0)

        # ACT
        move_attrs = move.decode(move.string_to_int(board.Board(), "f2f4"))

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_string_to_int_correctly_extracts_piece_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/p7/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        )
        test_attrs = (utils.string_to_coord("f1"), utils.string_to_coord("a6"), 0)

        # ACT
        move_attrs = move.decode(move.string_to_int(test_board, "f1a6"))

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_make_move_moves_pawn(self):
        # ARRANGE
        test_board = board.Board()
        piece = test_board.array[utils.string_to_coord("a2")]

        # ACT
        move.make_move_from_string("a2a3", test_board)

        # ASSERT
        self.assertEqual(test_board.array[utils.string_to_coord("a3")], piece)

    def test_make_move_capture(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3"
        )
        piece = test_board.array[utils.string_to_coord("e4")]

        # ACT
        move.make_move_from_string("e4d5", test_board)
        new_piece = test_board.array[utils.string_to_coord("d5")]

        # ASSERT
        self.assertEqual(piece, new_piece)

    def test_make_move_castling_queenside(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )

        # ACT
        move.make_move_from_string("e1c1", test_board)

        # ASSERT
        self.assertEqual(test_board.array[utils.string_to_coord("c1")] & 15, cs.K)
        self.assertEqual(test_board.array[utils.string_to_coord("d1")] & 15, cs.R)

    def test_make_move_castling_kingside(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )

        # ACT
        move.make_move_from_string("e1g1", test_board)

        # ASSERT
        self.assertEqual(test_board.array[utils.string_to_coord("g1")] & 15, cs.K)
        self.assertEqual(test_board.array[utils.string_to_coord("f1")] & 15, cs.R)

    def test_make_move_marks_white_en_passant_square(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppp1ppp/8/1N6/4p3/8/PPPPPPPP/R1BQKBNR w KQkq - 0 3"
        )

        # ACT
        move.make_move_from_string("f2f4", test_board)

        # ASSERT
        self.assertEqual(test_board.ep_square, utils.string_to_coord("f3"))

    def test_make_move_marks_black_en_passant_square(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/p7/3P4/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 4"
        )

        # ACT
        move.make_move_from_string("e7e5", test_board)

        # ASSERT
        self.assertEqual(test_board.ep_square, utils.string_to_coord("e6"))

    def test_make_move_promotes_pawn(self):
        test_board = fp.fen_to_board(
            "r1bqkbnr/pPpppp2/p1n5/6pp/8/4P3/P1PP1PPP/RNBQK1NR w KQkq - 0 13"
        )

        # ACT
        move.make_move_from_string("b7b8q", test_board)

        # ASSERT
        self.assertEqual(test_board.array[utils.string_to_coord("b8")] & 15, cs.Q)

    def test_make_move_en_passant_capture(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppp1ppp/p7/3Pp3/8/8/PPP1PPPP/RNBQKBNR w KQkq e6 0 5"
        )
        piece = test_board.array[utils.string_to_coord("d5")]

        # ACT
        move.make_move_from_string("d5e6", test_board)

        # ASSERT
        self.assertEqual(test_board.array[utils.string_to_coord("e6")], piece)
        self.assertFalse(test_board.array[utils.string_to_coord("e5")])

    def test_make_move_removes_queenside_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/pppppppp/n7/8/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 1 3"
        )

        # ACT
        move.make_move_from_string("a1a2", test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, False, True, True])

    def test_make_move_removes_queenside_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/p7/P7/8/8/1PPPPPPP/RNBQKBNR b KQkq - 0 4"
        )

        # ACT
        move.make_move_from_string("a8a7", test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, False])

    def test_make_move_removes_kingside_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/pppppppp/n7/8/7P/8/PPPPPPP1/RNBQKBNR w KQkq - 1 3"
        )

        # ACT
        move.make_move_from_string("h1h2", test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, True, True, True])

    def test_make_move_removes_kingside_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/ppppppp1/7p/7P/8/8/PPPPPPP1/RNBQKBNR b KQkq - 0 4"
        )

        # ACT
        move.make_move_from_string("h8h7", test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, False, True])

    def test_make_move_removes_castling_rights_after_king_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/pppppppp/n7/8/8/4P3/PPPP1PPP/RNBQKBNR w KQkq - 1 3"
        )

        # ACT
        move.make_move_from_string("e1e2", test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, False, True, True])

    def test_make_move_removes_castling_rights_after_black_king_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 4"
        )

        # ACT
        move.make_move_from_string("e8e7", test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, False, False])

    def test_unmake_move(self):
        # ARRANGE
        test_board = board.Board()
        test_string = test_board.to_fen()

        test_move = "a2a3"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)
        bd_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(bd_string, test_string)

    def test_unmake_move_unmakes_castling_queen_side(self):
        # ARRANGE
        test_string = "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        test_board = fp.fen_to_board(test_string)

        test_move = "e1c1"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)
        bd_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(bd_string, test_string)

    def test_unmake_move_unmakes_castling_king_side(self):
        # ARRANGE
        test_string = "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        test_board = fp.fen_to_board(test_string)
        test_move = "e1g1"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)
        bd_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(bd_string, test_string)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/pppppppp/n7/8/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 1 3"
        )
        test_move = "a1a2"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_black_rook_move(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/p7/P7/8/8/1PPPPPPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = "a8a7"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/pppppppp/n7/8/7P/8/PPPPPPP1/RNBQKBNR w KQkq - 1 3"
        )
        test_move = "h1h2"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_black_rook_move(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/ppppppp1/7p/7P/8/8/PPPPPPP1/RNBQKBNR b KQkq - 0 4"
        )
        test_move = "h8h7"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_castling_rights_after_unmaking_king_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/pppppppp/n7/8/8/4P3/PPPP1PPP/RNBQKBNR w KQkq - 1 3"
        )
        test_move = "e1e2"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_castling_rights_after_unmaking_black_king_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = "e8e7"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_does_not_restore_castling_rights_for_rook_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r1bqkbnr/p1pppppp/n7/1p6/7P/8/PPPPPPP1/RNBQKBNR w Qkq - 0 7"
        )
        test_move = "a1a2"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, True, True, True])

    def test_unmake_move_does_not_restore_castling_rights_for_king_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/1ppppppp/8/8/p7/4P3/PPPP1PPP/RNBQKBNR w kq - 0 7"
        )
        test_move = "e1e2"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, False, True, True])

    def test_unmake_move_restores_castling_rights_for_captured_rook(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rn1qkbn1/ppp1ppp1/3p3r/P7/6b1/3P4/1PP1PPP1/RN1QKBNR b KQq - 0 12"
        )
        test_move = "h6h1"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, False, True])

    def test_unmake_move_restores_ep_square(self):
        # ARRANGE
        test_string = (
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b KQkq a3 0 1"
        )
        test_board = fp.fen_to_board(test_string)
        test_move = "e8d8"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)
        b_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_unmake_move_en_passant_capture(self):
        # ARRANGE
        test_string = (
            "r3k2r/p2pqpb1/bn2pnp1/2pPN3/1p2P3/2N1BQ1p/PPP1BPPP/R3K2R w KQkq c6 0 2"
        )
        test_board = fp.fen_to_board(test_string)
        test_move = "d5c6"
        move.make_move_from_string(test_move, test_board)

        # ACT
        move.unmake_move_from_string(test_move, test_board)
        b_string = test_board.to_fen()

        # ASSERT
        self.assertEqual(b_string, test_string)

    def test_unmake_move_unmakes_a_series_of_moves(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        moves = ["d2d3", "h7h6", "c1h6", "g7h6", "h2h3", "d7d6"]

        for m in moves:
            move.make_move_from_string(m, test_board_1)

        # ACT
        for m in reversed(moves):
            move.unmake_move_from_string(m, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_unmakes_consecutive_captures(self):
        # ARRANGE
        test_string = "rnbqk1nr/pppp1ppp/8/2b1p3/3P4/4B3/PPPQPPPP/RN2KBNR b KQkq - 3 3"

        test_board_1 = fp.fen_to_board(test_string)
        test_board_2 = fp.fen_to_board(test_string)

        moves = ["e5d4", "e3d4", "c5d4", "d2d4"]

        for m in moves:
            move.make_move_from_string(m, test_board_1)

        # ACT
        for m in reversed(moves):
            move.unmake_move_from_string(m, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_unmakes_promotion(self):
        # ARRANGE
        test_string = "n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1"
        test_move = "g2g1"
        test_board_1 = fp.fen_to_board(test_string)
        test_board_2 = fp.fen_to_board(test_string)
        move.make_move_from_string(test_move, test_board_1)

        # ACT
        move.unmake_move_from_string(test_move, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_update_check_does_not_incorrectly_set_check_when_piece_ray_intersects_with_king(
        self,
    ):
        # ARRANGE
        test_board = fp.fen_to_board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )

        # ACT
        move.make_move_from_string("f3h5", test_board)

        # ASSERT
        self.assertEqual(test_board.check, 0)

    def test_update_check_correctly_sets_distant_check_when_king_cannot_move(self):
        # ARRANGE
        test_board = fp.fen_to_board(
            "rnbqkbnr/pp2pppp/2pp4/8/Q7/2P5/PP1PPPPP/RNB1KBNR w KQkq - 0 3"
        )

        # ACT
        move.make_move_from_string("a4c6", test_board)

        # ASSERT
        self.assertEqual(test_board.check, 2)
