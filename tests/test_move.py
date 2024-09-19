import unittest

from chess_engine import board, attributes as attrs, move, pieces


class TestMove(unittest.TestCase):
    def test_pseudo_legal_returns_true_for_valid_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.Move((1, 0), (2, 0), pieces.Pawn)

        # ACT
        valid = test_move.pseudo_legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.Move((0, 0), (5, 2), pieces.Rook)

        # ACT
        valid = test_move.pseudo_legal(test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_move_with_scale(self):
        # ARRANGE
        test_board = board.Board()
        test_move_1 = move.Move((1, 3), (2, 3), pieces.Pawn)
        test_move_2 = move.Move((6, 0), (5, 0), pieces.Pawn)
        test_move_3 = move.Move((0, 2), (5, 7), pieces.Bishop)

        test_move_1.make_move(test_board)
        test_move_2.make_move(test_board)

        # ACT
        valid = test_move_3.pseudo_legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_true_for_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.Move((1, 0), (3, 0), pieces.Pawn)

        # ACT
        valid = test_move.pseudo_legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move_1 = move.Move((1, 0), (3, 0), pieces.Pawn)
        test_move_1.make_move(test_board)
        test_move_2 = move.Move((3, 0), (5, 0), pieces.Pawn)

        # ACT
        valid = test_move_2.pseudo_legal(test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 3), (3, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((3, 3), (4, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 4), (4, 4), pieces.Pawn).make_move(test_board)
        test_move = move.Move((4, 3), (5, 4), pieces.Pawn, capture=True)

        # ACT
        valid = test_move.pseudo_legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_make_move_moves_pawn(self):
        # ARRANGE
        test_board = board.Board()
        piece = test_board.array[1][0]
        test_move = move.Move((1, 0), (2, 0), pieces.Pawn)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(piece.position, (2, 0))

    def test_make_move_capture(self):
        # ARRANGE
        test_board = board.Board()
        piece = test_board.array[1][4]
        piece_to_capture = test_board.array[6][3]
        move.Move((1, 4), (3, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 3), (4, 3), pieces.Pawn).make_move(test_board)
        test_move = move.Move((3, 4), (4, 3), pieces.Pawn, capture=True)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.prev_state[0], piece_to_capture)
        self.assertEqual(piece.position, piece_to_capture.position)

    def test_make_move_castling_queen_side(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 3), (3, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((0, 2), (2, 4), pieces.Bishop).make_move(test_board)
        move.Move((6, 1), (5, 1), pieces.Pawn).make_move(test_board)
        move.Move((0, 3), (2, 3), pieces.Queen).make_move(test_board)
        move.Move((6, 2), (5, 2), pieces.Pawn).make_move(test_board)
        move.Move((0, 1), (2, 2), pieces.Knight).make_move(test_board)
        move.Move((6, 3), (5, 3), pieces.Pawn).make_move(test_board)
        test_move = move.Move(
            (0, 4), (0, 2), pieces.King, castling=attrs.Castling.QUEEN_SIDE
        )

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.array[0][2].symbol, "k")
        self.assertEqual(test_board.array[0][3].symbol, "r")

    def test_make_move_castling_king_side(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((0, 5), (2, 3), pieces.Bishop).make_move(test_board)
        move.Move((6, 1), (5, 1), pieces.Pawn).make_move(test_board)
        move.Move((0, 6), (2, 7), pieces.Knight).make_move(test_board)
        move.Move((6, 2), (5, 2), pieces.Pawn).make_move(test_board)
        test_move = move.Move(
            (0, 4), (0, 6), pieces.King, castling=attrs.Castling.KING_SIDE
        )

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.array[0][6].symbol, "k")
        self.assertEqual(test_board.array[0][5].symbol, "r")

    def test_make_move_marks_en_passant_square(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 3), (3, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((3, 3), (4, 3), pieces.Pawn).make_move(test_board)
        test_move = move.Move((6, 4), (4, 4), pieces.Pawn)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.en_passant_square, (4, 4))

    def test_make_move_promotes_pawn(self):
        test_board = board.Board()
        move.Move((1, 1), (3, 1), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 2), pieces.Knight).make_move(test_board)
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 7), (5, 7), pieces.Pawn).make_move(test_board)
        move.Move((0, 5), (5, 0), pieces.Bishop).make_move(test_board)
        move.Move((6, 1), (5, 0), pieces.Pawn, capture=True).make_move(test_board)
        move.Move((3, 1), (4, 1), pieces.Pawn).make_move(test_board)
        move.Move((5, 7), (4, 7), pieces.Pawn).make_move(test_board)
        move.Move((4, 1), (5, 1), pieces.Pawn).make_move(test_board)
        move.Move((6, 6), (5, 6), pieces.Pawn).make_move(test_board)
        move.Move((5, 1), (6, 1), pieces.Pawn).make_move(test_board)
        move.Move((5, 6), (4, 6), pieces.Pawn).make_move(test_board)
        test_move = move.Move((6, 1), (7, 1), pieces.Pawn, promotion=pieces.Queen)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(
            (test_board.array[7][1].symbol, test_board.array[7][1].colour),
            ("q", attrs.Colour.WHITE),
        )

    def test_make_move_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 3), (3, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((3, 3), (4, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 4), (4, 4), pieces.Pawn).make_move(test_board)
        piece = test_board.array[4][3]
        captured_piece = test_board.array[4][4]
        test_move = move.Move((4, 3), (5, 4), pieces.Pawn, capture=True)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(piece.position, (5, 4))
        self.assertEqual(test_board.prev_state[0], captured_piece)

    def test_make_move_removes_queen_side_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 0), (3, 0), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        test_move = move.Move((0, 0), (1, 0), pieces.Rook)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0111)

    def test_make_move_removes_queen_side_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 0), (3, 0), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((3, 0), (4, 0), pieces.Pawn).make_move(test_board)
        test_move = move.Move((7, 0), (6, 0), pieces.Rook)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1101)

    def test_make_move_removes_king_side_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 7), (3, 7), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        test_move = move.Move((0, 7), (1, 7), pieces.Rook)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1011)

    def test_make_move_removes_king_side_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 7), (3, 7), pieces.Pawn).make_move(test_board)
        move.Move((6, 7), (5, 7), pieces.Pawn).make_move(test_board)
        move.Move((3, 7), (4, 7), pieces.Pawn).make_move(test_board)
        test_move = move.Move((7, 7), (6, 7), pieces.Rook)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1110)

    def test_make_move_removes_castling_rights_after_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        test_move = move.Move((0, 4), (1, 4), pieces.King)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0011)

    def test_make_move_removes_castling_rights_after_black_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 4), (5, 4), pieces.Pawn).make_move(test_board)
        move.Move((2, 4), (3, 4), pieces.Pawn).make_move(test_board)
        test_move = move.Move((7, 4), (6, 4), pieces.King)

        # ACT
        test_move.make_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1100)

    def test_unmake_move(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        test_move = move.Move((1, 0), (2, 0), pieces.Pawn)
        test_move.make_move(test_board_1)

        # ACT
        test_move.unmake_move(test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_unmakes_castling_queen_side(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        for bd in (test_board_1, test_board_2):
            move.Move((1, 3), (3, 3), pieces.Pawn).make_move(bd)
            move.Move((6, 0), (5, 0), pieces.Pawn).make_move(bd)
            move.Move((0, 2), (2, 4), pieces.Bishop).make_move(bd)
            move.Move((6, 1), (5, 1), pieces.Pawn).make_move(bd)
            move.Move((0, 3), (2, 3), pieces.Queen).make_move(bd)
            move.Move((6, 2), (5, 2), pieces.Pawn).make_move(bd)
            move.Move((0, 1), (2, 2), pieces.Knight).make_move(bd)
            move.Move((6, 3), (5, 3), pieces.Pawn).make_move(bd)

        test_move = move.Move(
            (0, 4), (0, 2), pieces.King, castling=attrs.Castling.QUEEN_SIDE
        )
        test_move.make_move(test_board_1)

        # ACT
        test_move.unmake_move(test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_unmakes_castling_king_side(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        for bd in (test_board_1, test_board_2):
            move.Move((1, 4), (2, 4), pieces.Pawn).make_move(bd)
            move.Move((6, 0), (5, 0), pieces.Pawn).make_move(bd)
            move.Move((0, 5), (2, 3), pieces.Bishop).make_move(bd)
            move.Move((6, 1), (5, 1), pieces.Pawn).make_move(bd)
            move.Move((0, 6), (2, 7), pieces.Knight).make_move(bd)
            move.Move((6, 2), (5, 2), pieces.Pawn).make_move(bd)

        test_move = move.Move(
            (0, 4), (0, 6), pieces.King, castling=attrs.Castling.KING_SIDE
        )
        test_move.make_move(test_board_1)

        # ACT
        test_move.unmake_move(test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 0), (3, 0), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        test_move = move.Move((0, 0), (1, 0), pieces.Rook)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_black_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 0), (3, 0), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((3, 0), (4, 0), pieces.Pawn).make_move(test_board)
        test_move = move.Move((7, 0), (6, 0), pieces.Rook)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 7), (3, 7), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        test_move = move.Move((0, 7), (1, 7), pieces.Rook)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_black_rook_move(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 7), (3, 7), pieces.Pawn).make_move(test_board)
        move.Move((6, 7), (5, 7), pieces.Pawn).make_move(test_board)
        move.Move((3, 7), (4, 7), pieces.Pawn).make_move(test_board)
        test_move = move.Move((7, 7), (6, 7), pieces.Rook)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        test_move = move.Move((0, 4), (1, 4), pieces.King)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_black_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 4), (5, 4), pieces.Pawn).make_move(test_board)
        move.Move((2, 4), (3, 4), pieces.Pawn).make_move(test_board)
        test_move = move.Move((7, 4), (6, 4), pieces.King)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_does_not_restore_castling_rights_for_rook_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 7), (3, 7), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        move.Move((0, 7), (1, 7), pieces.Rook).make_move(test_board)
        move.Move((6, 1), (5, 1), pieces.Pawn).make_move(test_board)
        move.Move((1, 7), (0, 7), pieces.Rook).make_move(test_board)
        move.Move((5, 1), (4, 1), pieces.Pawn).make_move(test_board)
        test_move = move.Move((0, 7), (1, 7), pieces.Rook)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1011)

    def test_unmake_move_does_not_restore_castling_rights_for_king_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((0, 4), (1, 4), pieces.King).make_move(test_board)
        move.Move((5, 0), (4, 0), pieces.Pawn).make_move(test_board)
        move.Move((1, 4), (0, 4), pieces.King).make_move(test_board)
        move.Move((4, 0), (3, 0), pieces.Pawn).make_move(test_board)
        test_move = move.Move((0, 4), (1, 4), pieces.King)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0011)

    def test_unmake_move_restores_castling_rights_for_captured_rook(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 3), (2, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 7), (5, 7), pieces.Pawn).make_move(test_board)
        move.Move((0, 2), (5, 7), pieces.Bishop, capture=True).make_move(test_board)
        move.Move((7, 7), (5, 7), pieces.Rook, capture=True).make_move(test_board)
        move.Move((1, 7), (2, 7), pieces.Pawn).make_move(test_board)
        move.Move((6, 3), (5, 3), pieces.Pawn).make_move(test_board)
        move.Move((1, 0), (2, 0), pieces.Pawn).make_move(test_board)
        move.Move((7, 2), (2, 7), pieces.Bishop, capture=True).make_move(test_board)
        move.Move((2, 0), (3, 0), pieces.Pawn).make_move(test_board)
        move.Move((2, 7), (3, 6), pieces.Bishop).make_move(test_board)
        move.Move((3, 0), (4, 0), pieces.Pawn).make_move(test_board)
        test_move = move.Move((5, 7), (0, 7), pieces.Rook, capture=True)
        test_move.make_move(test_board)

        # ACT
        test_move.unmake_move(test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1110)

    def test_legal_returns_true_for_legal_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.Move((1, 3), (2, 3), pieces.Pawn)

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 3), (2, 3), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 2), pieces.Knight).make_move(test_board)
        move.Move((2, 3), (3, 3), pieces.Pawn).make_move(test_board)
        test_move = move.Move((5, 2), (3, 3), pieces.Knight, capture=True)

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_move_in_check(self):
        # ARRANGE
        test_board = board.Board()
        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 4), (4, 4), pieces.Pawn).make_move(test_board)
        move.Move((1, 5), (2, 5), pieces.Pawn).make_move(test_board)
        move.Move((4, 4), (3, 4), pieces.Pawn).make_move(test_board)
        move.Move((1, 6), (3, 6), pieces.Pawn).make_move(test_board)
        move.Move((7, 3), (3, 7), pieces.Queen).make_move(test_board)
        test_move = move.Move((2, 5), (3, 4), pieces.Pawn, capture=True)

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_true_for_legal_king_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((0, 5), (2, 3), pieces.Bishop).make_move(test_board)
        move.Move((6, 1), (5, 1), pieces.Pawn).make_move(test_board)
        move.Move((0, 6), (2, 7), pieces.Knight).make_move(test_board)
        move.Move((6, 2), (5, 2), pieces.Pawn).make_move(test_board)
        test_move = move.Move(
            (0, 4), (0, 2), pieces.King, castling=attrs.Castling.KING_SIDE
        )

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_queen_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.Move((1, 3), (3, 3), pieces.Pawn).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        move.Move((0, 2), (2, 4), pieces.Bishop).make_move(test_board)
        move.Move((6, 1), (5, 1), pieces.Pawn).make_move(test_board)
        move.Move((0, 3), (2, 3), pieces.Rook).make_move(test_board)
        move.Move((6, 2), (5, 2), pieces.Pawn).make_move(test_board)
        move.Move((0, 1), (2, 2), pieces.Knight).make_move(test_board)
        move.Move((6, 3), (5, 3), pieces.Pawn).make_move(test_board)
        test_move = move.Move(
            (0, 4), (0, 6), pieces.King, castling=attrs.Castling.QUEEN_SIDE
        )

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_king_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.Move((1, 4), (2, 4), pieces.Pawn).make_move(test_board)
        move.Move((7, 6), (5, 5), pieces.Knight).make_move(test_board)
        move.Move((0, 5), (2, 3), pieces.Bishop).make_move(test_board)
        move.Move((5, 5), (3, 6), pieces.Knight).make_move(test_board)
        move.Move((0, 6), (2, 7), pieces.Knight).make_move(test_board)
        move.Move((3, 6), (2, 4), pieces.Knight, capture=True).make_move(test_board)
        test_move = move.Move(
            (0, 4), (0, 2), pieces.King, castling=attrs.Castling.KING_SIDE
        )

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_false_for_illegal_queen_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.Move((1, 3), (3, 3), pieces.Pawn).make_move(test_board)
        move.Move((7, 1), (5, 0), pieces.Knight).make_move(test_board)
        move.Move((0, 2), (2, 4), pieces.Bishop).make_move(test_board)
        move.Move((5, 0), (3, 1), pieces.Knight).make_move(test_board)
        move.Move((0, 3), (2, 3), pieces.Queen).make_move(test_board)
        move.Move((3, 1), (2, 3), pieces.Knight, capture=True).make_move(test_board)
        move.Move((0, 1), (2, 2), pieces.Knight).make_move(test_board)
        move.Move((6, 0), (5, 0), pieces.Pawn).make_move(test_board)
        test_move = move.Move(
            (0, 4), (0, 6), pieces.King, castling=attrs.Castling.QUEEN_SIDE
        )

        # ACT
        valid = test_move.legal(test_board)

        # ASSERT
        self.assertFalse(valid)
