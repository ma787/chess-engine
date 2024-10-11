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

    def test_pseudo_legal_returns_true_for_move_with_scale(self):
        # ARRANGE
        test_board = board.Board()
        test_move_1 = move.encode_move(0x13, 0x23)
        test_move_2 = move.encode_move(0x60, 0x50)
        test_move_3 = move.encode_move(0x02, 0x57)

        move.make_move(test_move_1, test_board)
        move.make_move(test_move_2, test_board)

        # ACT
        valid = move.pseudo_legal(test_move_3, test_board)

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

    def test_pseudo_legal_returns_true_for_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x13, 0x33), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x33, 0x43), test_board)
        move.make_move(move.encode_move(0x64, 0x44), test_board)
        test_move = move.encode_move(0x43, 0x54, capture=True)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

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
        test_board = board.Board()
        piece = test_board.array[0x14]
        move.make_move(move.encode_move(0x14, 0x34), test_board)
        move.make_move(move.encode_move(0x63, 0x43), test_board)
        test_move = move.encode_move(0x34, 0x43, capture=True)

        # ACT
        move.make_move(test_move, test_board)
        new_piece = test_board.array[0x43]

        # ASSERT
        self.assertEqual(piece, new_piece)

    def test_make_move_castling_queen_side(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x13, 0x33), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x02, 0x24), test_board)
        move.make_move(move.encode_move(0x61, 0x51), test_board)
        move.make_move(move.encode_move(0x03, 0x23), test_board)
        move.make_move(move.encode_move(0x62, 0x52), test_board)
        move.make_move(move.encode_move(0x01, 0x22), test_board)
        move.make_move(move.encode_move(0x63, 0x53), test_board)
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x02], 2)
        self.assertEqual(test_board.array[0x03], 6)

    def test_make_move_castling_king_side(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x05, 0x23), test_board)
        move.make_move(move.encode_move(0x61, 0x51), test_board)
        move.make_move(move.encode_move(0x06, 0x27), test_board)
        move.make_move(move.encode_move(0x62, 0x52), test_board)
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(abs(test_board.array[0x06]), 2)
        self.assertEqual(abs(test_board.array[0x05]), 6)

    def test_make_move_marks_en_passant_square(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x13, 0x33), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x33, 0x43), test_board)
        test_move = move.encode_move(0x64, 0x44)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.ep_square, 0x44)

    def test_make_move_promotes_pawn(self):
        test_board = board.Board()
        move.make_move(move.encode_move(0x11, 0x31), test_board)
        move.make_move(move.encode_move(0x71, 0x52), test_board)
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x67, 0x57), test_board)
        move.make_move(move.encode_move(0x05, 0x50), test_board)
        move.make_move(move.encode_move(0x61, 0x50, capture=True), test_board)
        move.make_move(move.encode_move(0x31, 0x41), test_board)
        move.make_move(move.encode_move(0x57, 0x47), test_board)
        move.make_move(move.encode_move(0x41, 0x51), test_board)
        move.make_move(move.encode_move(0x66, 0x56), test_board)
        move.make_move(move.encode_move(0x51, 0x61), test_board)
        move.make_move(move.encode_move(0x56, 0x46), test_board)
        test_move = move.encode_move(0x61, 0x71, promotion=5)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x71], 5)

    def test_make_move_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x13, 0x33), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x33, 0x43), test_board)
        move.make_move(move.encode_move(0x64, 0x44), test_board)
        piece = test_board.array[0x43]
        test_move = move.encode_move(0x43, 0x54, capture=True)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[0x54], piece)
        self.assertEqual(test_board.array[0x44], 0)

    def test_make_move_removes_queenside_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x10, 0x30), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
        test_move = move.encode_move(0x00, 0x10)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1110)

    def test_make_move_removes_queenside_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x10, 0x30), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x30, 0x40), test_board)
        test_move = move.encode_move(0x70, 0x60)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1011)

    def test_make_move_removes_kingside_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x17, 0x37), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
        test_move = move.encode_move(0x07, 0x17)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1101)

    def test_make_move_removes_kingside_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x17, 0x37), test_board)
        move.make_move(move.encode_move(0x67, 0x57), test_board)
        move.make_move(move.encode_move(0x37, 0x47), test_board)
        test_move = move.encode_move(0x77, 0x67)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0111)

    def test_make_move_removes_castling_rights_after_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
        test_move = move.encode_move(0x04, 0x14)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1100)

    def test_make_move_removes_castling_rights_after_black_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x64, 0x54), test_board)
        move.make_move(move.encode_move(0x24, 0x34), test_board)
        test_move = move.encode_move(0x74, 0x64)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0011)

    def test_unmake_move(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        test_move = move.encode_move(0x10, 0x20)
        move.make_move(test_move, test_board_1)

        # ACT
        move.unmake_move(test_move, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_unmakes_castling_queen_side(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        for bd in (test_board_1, test_board_2):
            move.make_move(move.encode_move(0x13, 0x33), bd)
            move.make_move(move.encode_move(0x60, 0x50), bd)
            move.make_move(move.encode_move(0x02, 0x24), bd)
            move.make_move(move.encode_move(0x61, 0x51), bd)
            move.make_move(move.encode_move(0x03, 0x23), bd)
            move.make_move(move.encode_move(0x62, 0x52), bd)
            move.make_move(move.encode_move(0x01, 0x22), bd)
            move.make_move(move.encode_move(0x63, 0x53), bd)

        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)
        move.make_move(test_move, test_board_1)

        # ACT
        move.unmake_move(test_move, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_unmakes_castling_king_side(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        for bd in (test_board_1, test_board_2):
            move.make_move(move.encode_move(0x14, 0x24), bd)
            move.make_move(move.encode_move(0x60, 0x50), bd)
            move.make_move(move.encode_move(0x05, 0x23), bd)
            move.make_move(move.encode_move(0x61, 0x51), bd)
            move.make_move(move.encode_move(0x06, 0x27), bd)
            move.make_move(move.encode_move(0x62, 0x52), bd)

        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)
        move.make_move(test_move, test_board_1)

        # ACT
        move.unmake_move(test_move, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x10, 0x30), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
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
        test_board = board.Board()
        move.make_move(move.encode_move(0x10, 0x30), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x30, 0x40), test_board)
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
        test_board = board.Board()
        move.make_move(move.encode_move(0x17, 0x37), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
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
        test_board = board.Board()
        move.make_move(move.encode_move(0x17, 0x37), test_board)
        move.make_move(move.encode_move(0x67, 0x57), test_board)
        move.make_move(move.encode_move(0x37, 0x47), test_board)
        test_move = move.encode_move(0x77, 0x67)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
        test_move = move.encode_move(0x04, 0x14)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_black_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x64, 0x54), test_board)
        move.make_move(move.encode_move(0x24, 0x34), test_board)
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
        test_board = board.Board()
        move.make_move(move.encode_move(0x17, 0x37), test_board)
        move.make_move(move.encode_move(0x71, 0x50), test_board)
        move.make_move(move.encode_move(0x07, 0x17), test_board)
        move.make_move(move.encode_move(0x61, 0x51), test_board)
        move.make_move(move.encode_move(0x17, 0x07), test_board)
        move.make_move(move.encode_move(0x51, 0x41), test_board)
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
        test_board = board.Board()
        move.make_move(move.encode_move(0x14, 0x24), test_board)
        move.make_move(move.encode_move(0x60, 0x50), test_board)
        move.make_move(move.encode_move(0x04, 0x14), test_board)
        move.make_move(move.encode_move(0x50, 0x40), test_board)
        move.make_move(move.encode_move(0x14, 0x04), test_board)
        move.make_move(move.encode_move(0x40, 0x30), test_board)
        test_move = move.encode_move(0x04, 0x14)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1100)

    def test_unmake_move_restores_castling_rights_for_captured_rook(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move(0x13, 0x23), test_board)
        move.make_move(move.encode_move(0x67, 0x57), test_board)
        move.make_move(move.encode_move(0x02, 0x57, capture=True), test_board)
        move.make_move(move.encode_move(0x77, 0x57, capture=True), test_board)
        move.make_move(move.encode_move(0x17, 0x27), test_board)
        move.make_move(move.encode_move(0x63, 0x53), test_board)
        move.make_move(move.encode_move(0x10, 0x20), test_board)
        move.make_move(move.encode_move(0x72, 0x27, capture=True), test_board)
        move.make_move(move.encode_move(0x20, 0x30), test_board)
        move.make_move(move.encode_move(0x27, 0x36), test_board)
        move.make_move(move.encode_move(0x30, 0x40), test_board)
        test_move = move.encode_move(0x57, 0x07, capture=True)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0111)

    def test_unmake_move_unmakes_two_moves(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        moves = [move.encode_move(0x13, 0x23), move.encode_move(0x67, 0x57)]

        for m in moves:
            move.make_move(m, test_board_1)

        # ACT
        for m in reversed(moves):
            move.unmake_move(m, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

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
