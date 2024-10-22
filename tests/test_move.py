import unittest

from chess_engine import board, constants as cs, move


class TestMove(unittest.TestCase):
    def test_encode_move_correctly_encodes_quiet_move(self):
        # ARRANGE
        test_attrs = [0x15, 0x35, False, 0, 0]

        # ACT
        test_move = move.encode_move(test_attrs[0], test_attrs[1])
        move_attrs = move.get_info(test_move)

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_encode_move_correctly_encodes_capture(self):
        # ARRANGE
        test_attrs = [0x05, 0x50, True, 0, 0]

        # ACT
        test_move = move.encode_move(
            test_attrs[0], test_attrs[1], capture=test_attrs[2]
        )
        move_attrs = move.get_info(test_move)

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_encode_move_correctly_encodes_queenside_castle(self):
        # ARRANGE
        test_attrs = [0x74, 0x72, False, cs.QUEENSIDE, 0]

        # ACT
        test_move = move.encode_move(
            test_attrs[0], test_attrs[1], castling=test_attrs[3]
        )
        move_attrs = move.get_info(test_move)

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_encode_move_correctly_encodes_kingside_castle(self):
        # ARRANGE
        test_attrs = [0x74, 0x76, False, cs.KINGSIDE, 0]

        # ACT
        test_move = move.encode_move(
            test_attrs[0], test_attrs[1], castling=test_attrs[3]
        )
        move_attrs = move.get_info(test_move)

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_encode_move_correctly_encodes_promotion(self):
        # ARRANGE
        test_attrs = [0x17, 0x07, False, 0, cs.QUEEN]

        # ACT
        test_move = move.encode_move(
            test_attrs[0], test_attrs[1], promotion=test_attrs[4]
        )
        move_attrs = move.get_info(test_move)

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_encode_move_correctly_encodes_promotion_capture(self):
        # ARRANGE
        test_attrs = [0x64, 0x73, True, 0, cs.BISHOP]

        # ACT
        test_move = move.encode_move(
            test_attrs[0], test_attrs[1], capture=test_attrs[2], promotion=test_attrs[4]
        )
        move_attrs = move.get_info(test_move)

        # ASSERT
        self.assertEqual(test_attrs, move_attrs)

    def test_pseudo_legal_returns_true_for_valid_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x10, 0x20)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_true_for_sliding_piece_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppppppp/p7/8/8/3P4/PPP1PPPP/RNBQKBNR w kqKQ - 0 3"
        )
        test_move = move.encode_move(0x02, 0x57)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_true_for_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x10, 0x30)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_promotion(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x10, 0x20, promotion=cs.QUEEN)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppp1ppp/p7/3Pp3/8/8/PPP1PPPP/RNBQKBNR w KQkq e5 0 5"
        )
        test_move = move.encode_move(0x43, 0x54, capture=True)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppppp1pp/8/8/1P2Pp2/8/P1PP1PPP/RNBQKBNR b KQkq - 0 6"
        )
        test_move = move.encode_move(0x35, 0x24, capture=True)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_valid_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1pppppp1/8/p6p/2B5/4PN2/PPPP1PPP/RNBQK2R w KQkq - 0 4"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_true_for_valid_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1pppppp1/p7/7p/2B5/4P3/PPPP1PPP/RNBQK1NR w KQkq - 0 3"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_false_for_invalid_queenside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppppppp1/7p/8/8/N7/PPPPPPPP/R1BQKBNR w KQkq - 0 2"
        )
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_false_for_enemy_piece_blocking_kingside_castle(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkb1r/pppppppp/8/8/2B1P3/5N2/PPPP1PPP/RNBQKn1R w KQkq - 1 5"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_false_for_no_castling_rights_kingside(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqk2r/pppp1pp1/4pP2/1P5p/8/8/1PPP1PPP/RNBQKBNR b KQq - 0 7"
        )
        test_move = move.encode_move(0x74, 0x76, castling=cs.KINGSIDE)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_make_move_moves_pawn(self):
        # ARRANGE
        test_board = board.Board()
        piece = test_board.array[0x10]
        test_move = move.encode_move(0x10, 0x20)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x20], piece)

    def test_make_move_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d5 0 3"
        )
        piece = test_board.array[0x34]
        test_move = move.encode_move(0x34, 0x43, capture=True)

        # ACT
        move.make_move(test_move, test_board)
        new_piece = test_board.array[0x43]

        # ASSERT
        self.assertEqual(piece, new_piece)

    def test_make_move_castling_queenside(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x02], cs.KING)
        self.assertEqual(test_board.array[0x03], cs.ROOK)

    def test_make_move_castling_kingside(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(abs(test_board.array[0x06]), cs.KING)
        self.assertEqual(abs(test_board.array[0x05]), cs.ROOK)

    def test_make_move_marks_en_passant_square(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppppppp/p7/3P4/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x64, 0x44)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.ep_square, 0x44)

    def test_make_move_promotes_pawn(self):
        test_board = board.Board.of_string(
            "r1bqkbnr/pPpppp2/p1n5/6pp/8/4P3/P1PP1PPP/RNBQK1NR w KQkq - 0 13"
        )
        test_move = move.encode_move(0x61, 0x71, promotion=cs.QUEEN)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x71], cs.QUEEN)

    def test_make_move_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppp1ppp/p7/3Pp3/8/8/PPP1PPPP/RNBQKBNR w KQkq e5 0 5"
        )
        piece = test_board.array[0x43]
        test_move = move.encode_move(0x43, 0x54, capture=True)

        # ACT
        print(f"ep square: {test_board.ep_square:02x}")
        move.make_move(test_move, test_board)
        print(test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x54], piece)
        self.assertEqual(test_board.array[0x44], cs.NULL_PIECE)

    def test_make_move_removes_queenside_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/n7/8/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 1 3"
        )
        test_move = move.encode_move(0x00, 0x10)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1110)

    def test_make_move_removes_queenside_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppppppp/p7/P7/8/8/1PPPPPPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x70, 0x60)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1011)

    def test_make_move_removes_kingside_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/n7/8/7P/8/PPPPPPP1/RNBQKBNR w KQkq - 1 3"
        )
        test_move = move.encode_move(0x07, 0x17)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1101)

    def test_make_move_removes_kingside_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppppppp1/7p/7P/8/8/PPPPPPP1/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x77, 0x67)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0111)

    def test_make_move_removes_castling_rights_after_king_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/n7/8/8/4P3/PPPP1PPP/RNBQKBNR w KQkq - 1 3"
        )
        test_move = move.encode_move(0x04, 0x14)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1100)

    def test_make_move_removes_castling_rights_after_black_king_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x74, 0x64)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0011)

    def test_unmake_move(self):
        # ARRANGE
        test_board = board.Board()
        test_string = test_board.to_string()

        test_move = move.encode_move(0x10, 0x20)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)
        bd_string = test_board.to_string()

        # ASSERT
        self.assertEqual(bd_string, test_string)

    def test_unmake_move_unmakes_castling_queen_side(self):
        # ARRANGE
        test_string = "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        test_board = board.Board.of_string(test_string)
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)
        bd_string = test_board.to_string()

        # ASSERT
        self.assertEqual(bd_string, test_string)

    def test_unmake_move_unmakes_castling_king_side(self):
        # ARRANGE
        test_string = "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        test_board = board.Board.of_string(test_string)
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)
        bd_string = test_board.to_string()

        # ASSERT
        self.assertEqual(bd_string, test_string)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/n7/8/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 1 3"
        )
        test_move = move.encode_move(0x00, 0x10)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_black_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppppppp/p7/P7/8/8/1PPPPPPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x70, 0x60)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/n7/8/7P/8/PPPPPPP1/RNBQKBNR w KQkq - 1 3"
        )
        test_move = move.encode_move(0x07, 0x17)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_black_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppppppp1/7p/7P/8/8/PPPPPPP1/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x77, 0x67)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_king_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pppppppp/n7/8/8/4P3/PPPP1PPP/RNBQKBNR w KQkq - 1 3"
        )
        test_move = move.encode_move(0x04, 0x14)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_black_king_move(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 4"
        )
        test_move = move.encode_move(0x74, 0x64)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_does_not_restore_castling_rights_for_rook_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/p1pppppp/n7/1p6/7P/8/PPPPPPP1/RNBQKBNR w Qkq - 0 7"
        )
        test_move = move.encode_move(0x07, 0x17)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1101)

    def test_unmake_move_does_not_restore_castling_rights_for_king_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/1ppppppp/8/8/p7/4P3/PPPP1PPP/RNBQKBNR w kq - 0 7"
        )
        test_move = move.encode_move(0x04, 0x14)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1100)

    def test_unmake_move_restores_castling_rights_for_captured_rook(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rn1qkbn1/ppp1ppp1/3p3r/P7/6b1/3P4/1PP1PPP1/RN1QKBNR b KQq - 0 12"
        )
        test_move = move.encode_move(0x57, 0x07, capture=True)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0111)

    def test_unmake_move_unmakes_a_series_of_moves(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        moves = [
            move.encode_move(0x13, 0x23),
            move.encode_move(0x67, 0x57),
            move.encode_move(0x02, 0x57, capture=True),
            move.encode_move(0x77, 0x57, capture=True),
            move.encode_move(0x17, 0x27),
            move.encode_move(0x63, 0x53),
        ]

        for m in moves:
            move.make_move(m, test_board_1)

        # ACT
        for m in reversed(moves):
            move.unmake_move(m, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)
