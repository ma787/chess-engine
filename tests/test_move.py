import unittest

from chess_engine import board, move


class TestMove(unittest.TestCase):
    def test_pseudo_legal_returns_true_for_valid_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move((1, 0), (2, 0))

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move((0, 0), (5, 2))

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_move_with_scale(self):
        # ARRANGE
        test_board = board.Board()
        test_move_1 = move.encode_move((1, 3), (2, 3))
        test_move_2 = move.encode_move((6, 0), (5, 0))
        test_move_3 = move.encode_move((0, 2), (5, 7))

        move.make_move(test_move_1, test_board)
        move.make_move(test_move_2, test_board)

        # ACT
        valid = move.pseudo_legal(test_move_3, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_true_for_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move((1, 0), (3, 0))

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move_1 = move.encode_move((1, 0), (3, 0))
        move.make_move(test_move_1, test_board)
        test_move_2 = move.encode_move((3, 0), (5, 0))

        # ACT
        valid = move.pseudo_legal(test_move_2, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 3), (3, 3)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((3, 3), (4, 3)), test_board)
        move.make_move(move.encode_move((6, 4), (4, 4)), test_board)
        test_move = move.encode_move((4, 3), (5, 4), capture=True)

        # ACT
        valid = move.pseudo_legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_make_move_moves_pawn(self):
        # ARRANGE
        test_board = board.Board()
        piece = test_board.array[1][0]
        test_move = move.encode_move((1, 0), (2, 0))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[2][0], piece)

    def test_make_move_capture(self):
        # ARRANGE
        test_board = board.Board()
        piece = test_board.array[1][4]
        move.make_move(move.encode_move((1, 4), (3, 4)), test_board)
        move.make_move(move.encode_move((6, 3), (4, 3)), test_board)
        test_move = move.encode_move((3, 4), (4, 3), capture=True)

        # ACT
        move.make_move(test_move, test_board)
        new_piece = test_board.array[4][3]

        # ASSERT
        self.assertEqual(piece, new_piece)

    def test_make_move_castling_queen_side(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 3), (3, 3)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 2), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 1), (5, 1)), test_board)
        move.make_move(move.encode_move((0, 3), (2, 3)), test_board)
        move.make_move(move.encode_move((6, 2), (5, 2)), test_board)
        move.make_move(move.encode_move((0, 1), (2, 2)), test_board)
        move.make_move(move.encode_move((6, 3), (5, 3)), test_board)
        test_move = move.encode_move((0, 4), (0, 2), castling=2)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(abs(test_board.array[0][2]), 2)
        self.assertEqual(abs(test_board.array[0][3]), 6)

    def test_make_move_castling_king_side(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 5), (2, 3)), test_board)
        move.make_move(move.encode_move((6, 1), (5, 1)), test_board)
        move.make_move(move.encode_move((0, 6), (2, 7)), test_board)
        move.make_move(move.encode_move((6, 2), (5, 2)), test_board)
        test_move = move.encode_move((0, 4), (0, 6), castling=1)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(abs(test_board.array[0][6]), 2)
        self.assertEqual(abs(test_board.array[0][5]), 6)

    def test_make_move_marks_en_passant_square(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 3), (3, 3)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((3, 3), (4, 3)), test_board)
        test_move = move.encode_move((6, 4), (4, 4))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.en_passant_square, (4, 4))

    def test_make_move_promotes_pawn(self):
        test_board = board.Board()
        move.make_move(move.encode_move((1, 1), (3, 1)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 2)), test_board)
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 7), (5, 7)), test_board)
        move.make_move(move.encode_move((0, 5), (5, 0)), test_board)
        move.make_move(move.encode_move((6, 1), (5, 0), capture=True), test_board)
        move.make_move(move.encode_move((3, 1), (4, 1)), test_board)
        move.make_move(move.encode_move((5, 7), (4, 7)), test_board)
        move.make_move(move.encode_move((4, 1), (5, 1)), test_board)
        move.make_move(move.encode_move((6, 6), (5, 6)), test_board)
        move.make_move(move.encode_move((5, 1), (6, 1)), test_board)
        move.make_move(move.encode_move((5, 6), (4, 6)), test_board)
        test_move = move.encode_move((6, 1), (7, 1), promotion=5)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[7][1], 5)

    def test_make_move_en_passant_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 3), (3, 3)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((3, 3), (4, 3)), test_board)
        move.make_move(move.encode_move((6, 4), (4, 4)), test_board)
        piece = test_board.array[4][3]
        test_move = move.encode_move((4, 3), (5, 4), capture=True)

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.array[5][4], piece)
        self.assertEqual(test_board.array[4][4], 0)

    def test_make_move_removes_queen_side_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 0), (3, 0)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        test_move = move.encode_move((0, 0), (1, 0))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0111)

    def test_make_move_removes_queen_side_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 0), (3, 0)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((3, 0), (4, 0)), test_board)
        test_move = move.encode_move((7, 0), (6, 0))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1101)

    def test_make_move_removes_king_side_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 7), (3, 7)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        test_move = move.encode_move((0, 7), (1, 7))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1011)

    def test_make_move_removes_king_side_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 7), (3, 7)), test_board)
        move.make_move(move.encode_move((6, 7), (5, 7)), test_board)
        move.make_move(move.encode_move((3, 7), (4, 7)), test_board)
        test_move = move.encode_move((7, 7), (6, 7))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1110)

    def test_make_move_removes_castling_rights_after_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        test_move = move.encode_move((0, 4), (1, 4))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0011)

    def test_make_move_removes_castling_rights_after_black_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 4), (5, 4)), test_board)
        move.make_move(move.encode_move((2, 4), (3, 4)), test_board)
        test_move = move.encode_move((7, 4), (6, 4))

        # ACT
        move.make_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1100)

    def test_unmake_move(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        test_move = move.encode_move((1, 0), (2, 0))
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
            move.make_move(move.encode_move((1, 3), (3, 3)), bd)
            move.make_move(move.encode_move((6, 0), (5, 0)), bd)
            move.make_move(move.encode_move((0, 2), (2, 4)), bd)
            move.make_move(move.encode_move((6, 1), (5, 1)), bd)
            move.make_move(move.encode_move((0, 3), (2, 3)), bd)
            move.make_move(move.encode_move((6, 2), (5, 2)), bd)
            move.make_move(move.encode_move((0, 1), (2, 2)), bd)
            move.make_move(move.encode_move((6, 3), (5, 3)), bd)

        test_move = move.encode_move((0, 4), (0, 2), castling=2)
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
            move.make_move(move.encode_move((1, 4), (2, 4)), bd)
            move.make_move(move.encode_move((6, 0), (5, 0)), bd)
            move.make_move(move.encode_move((0, 5), (2, 3)), bd)
            move.make_move(move.encode_move((6, 1), (5, 1)), bd)
            move.make_move(move.encode_move((0, 6), (2, 7)), bd)
            move.make_move(move.encode_move((6, 2), (5, 2)), bd)

        test_move = move.encode_move((0, 4), (0, 6), castling=1)
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
        move.make_move(move.encode_move((1, 0), (3, 0)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        test_move = move.encode_move((0, 0), (1, 0))
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
        move.make_move(move.encode_move((1, 0), (3, 0)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((3, 0), (4, 0)), test_board)
        test_move = move.encode_move((7, 0), (6, 0))
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
        move.make_move(move.encode_move((1, 7), (3, 7)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        test_move = move.encode_move((0, 7), (1, 7))
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
        move.make_move(move.encode_move((1, 7), (3, 7)), test_board)
        move.make_move(move.encode_move((6, 7), (5, 7)), test_board)
        move.make_move(move.encode_move((3, 7), (4, 7)), test_board)
        test_move = move.encode_move((7, 7), (6, 7))
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        test_move = move.encode_move((0, 4), (1, 4))
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1111)

    def test_unmake_move_restores_castling_rights_after_unmaking_black_king_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 4), (5, 4)), test_board)
        move.make_move(move.encode_move((2, 4), (3, 4)), test_board)
        test_move = move.encode_move((7, 4), (6, 4))
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
        move.make_move(move.encode_move((1, 7), (3, 7)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 7), (1, 7)), test_board)
        move.make_move(move.encode_move((6, 1), (5, 1)), test_board)
        move.make_move(move.encode_move((1, 7), (0, 7)), test_board)
        move.make_move(move.encode_move((5, 1), (4, 1)), test_board)
        test_move = move.encode_move((0, 7), (1, 7))
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1011)

    def test_unmake_move_does_not_restore_castling_rights_for_king_that_returns_to_original_position(
        self,
    ):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 4), (1, 4)), test_board)
        move.make_move(move.encode_move((5, 0), (4, 0)), test_board)
        move.make_move(move.encode_move((1, 4), (0, 4)), test_board)
        move.make_move(move.encode_move((4, 0), (3, 0)), test_board)
        test_move = move.encode_move((0, 4), (1, 4))
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b0011)

    def test_unmake_move_restores_castling_rights_for_captured_rook(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 3), (2, 3)), test_board)
        move.make_move(move.encode_move((6, 7), (5, 7)), test_board)
        move.make_move(move.encode_move((0, 2), (5, 7), capture=True), test_board)
        move.make_move(move.encode_move((7, 7), (5, 7), capture=True), test_board)
        move.make_move(move.encode_move((1, 7), (2, 7)), test_board)
        move.make_move(move.encode_move((6, 3), (5, 3)), test_board)
        move.make_move(move.encode_move((1, 0), (2, 0)), test_board)
        move.make_move(move.encode_move((7, 2), (2, 7), capture=True), test_board)
        move.make_move(move.encode_move((2, 0), (3, 0)), test_board)
        move.make_move(move.encode_move((2, 7), (3, 6)), test_board)
        move.make_move(move.encode_move((3, 0), (4, 0)), test_board)
        test_move = move.encode_move((5, 7), (0, 7), capture=True)
        move.make_move(test_move, test_board)

        # ACT
        move.unmake_move(test_move, test_board)

        # ASSERT
        self.assertEqual(test_board.castling_rights, 0b1110)

    def test_unmake_move_unmakes_two_moves(self):
        # ARRANGE
        test_board_1 = board.Board()
        test_board_2 = board.Board()

        moves = [move.encode_move((1, 3), (2, 3)), move.encode_move((6, 7), (5, 7))]

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
            move.encode_move((1, 3), (2, 3)),
            move.encode_move((6, 7), (5, 7)),
            move.encode_move((0, 2), (5, 7), capture=True),
            move.encode_move((7, 7), (5, 7), capture=True),
            move.encode_move((1, 7), (2, 7)),
            move.encode_move((6, 3), (5, 3)),
        ]

        for m in moves:
            move.make_move(m, test_board_1)

        # ACT
        for m in reversed(moves):
            move.unmake_move(m, test_board_1)

        # ASSERT
        self.assertEqual(test_board_1, test_board_2)

    def test_legal_returns_true_for_legal_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move((1, 3), (2, 3))

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 3), (2, 3)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 2)), test_board)
        move.make_move(move.encode_move((2, 3), (3, 3)), test_board)
        test_move = move.encode_move((5, 2), (3, 3), capture=True)

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_move_in_check(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 4), (4, 4)), test_board)
        move.make_move(move.encode_move((1, 5), (2, 5)), test_board)
        move.make_move(move.encode_move((4, 4), (3, 4)), test_board)
        move.make_move(move.encode_move((1, 6), (3, 6)), test_board)
        move.make_move(move.encode_move((7, 3), (3, 7)), test_board)
        test_move = move.encode_move((2, 5), (3, 4), capture=True)

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_true_for_legal_king_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 5), (2, 3)), test_board)
        move.make_move(move.encode_move((6, 1), (5, 1)), test_board)
        move.make_move(move.encode_move((0, 6), (2, 7)), test_board)
        move.make_move(move.encode_move((6, 2), (5, 2)), test_board)
        test_move = move.encode_move((0, 4), (0, 2), castling=1)

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_queen_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move((1, 3), (3, 3)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 2), (2, 4)), test_board)
        move.make_move(move.encode_move((6, 1), (5, 1)), test_board)
        move.make_move(move.encode_move((0, 3), (2, 3)), test_board)
        move.make_move(move.encode_move((6, 2), (5, 2)), test_board)
        move.make_move(move.encode_move((0, 1), (2, 2)), test_board)
        move.make_move(move.encode_move((6, 3), (5, 3)), test_board)
        test_move = move.encode_move((0, 4), (0, 6), castling=2)

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_king_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move((1, 4), (2, 4)), test_board)
        move.make_move(move.encode_move((7, 6), (5, 5)), test_board)
        move.make_move(move.encode_move((0, 5), (2, 3)), test_board)
        move.make_move(move.encode_move((5, 5), (3, 6)), test_board)
        move.make_move(move.encode_move((0, 6), (2, 7)), test_board)
        move.make_move(move.encode_move((3, 6), (2, 4), capture=True), test_board)
        test_move = move.encode_move((0, 4), (0, 2), castling=1)

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_false_for_illegal_queen_side_castle(self):
        # ARRANGE
        test_board = board.Board()

        move.make_move(move.encode_move((1, 3), (3, 3)), test_board)
        move.make_move(move.encode_move((7, 1), (5, 0)), test_board)
        move.make_move(move.encode_move((0, 2), (2, 4)), test_board)
        move.make_move(move.encode_move((5, 0), (3, 1)), test_board)
        move.make_move(move.encode_move((0, 3), (2, 3)), test_board)
        move.make_move(move.encode_move((3, 1), (2, 3), capture=True), test_board)
        move.make_move(move.encode_move((0, 1), (2, 2)), test_board)
        move.make_move(move.encode_move((6, 0), (5, 0)), test_board)
        test_move = move.encode_move((0, 4), (0, 6), castling=2)

        # ACT
        valid = move.legal(test_move, test_board)

        # ASSERT
        self.assertFalse(valid)
