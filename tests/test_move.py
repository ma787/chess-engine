import unittest

from chess_engine.board import Board
from chess_engine.attributes import Castling
from chess_engine.move import Move
from chess_engine.pieces import Queen


class TestMove(unittest.TestCase):
    def test_pseudo_legal_returns_true_for_valid_move(self):
        # ARRANGE
        test_board = Board()
        test_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0))

        # ACT
        valid = test_move.pseudo_legal()

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_move(self):
        # ARRANGE
        test_board = Board()
        test_move = Move(test_board.array[0][0], test_board, (0, 0), (5, 2))

        # ACT
        valid = test_move.pseudo_legal()

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_move_with_scale(self):
        # ARRANGE
        test_board = Board()
        test_move_1 = Move(test_board.array[1][3], test_board, (1, 3), (2, 3))
        test_move_2 = Move(test_board.array[6][0], test_board, (6, 0), (5, 0))
        test_move_3 = Move(test_board.array[0][2], test_board, (0, 2), (5, 7))

        test_move_1.make_move()
        test_move_2.make_move()

        # ACT
        valid = test_move_3.pseudo_legal()

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_true_for_pawn_move(self):
        # ARRANGE
        test_board = Board()
        test_move = Move(test_board.array[1][0], test_board, (1, 0), (3, 0))

        # ACT
        valid = test_move.pseudo_legal()

        # ASSERT
        self.assertTrue(valid)

    def test_pseudo_legal_returns_false_for_invalid_pawn_move(self):
        # ARRANGE
        test_board = Board()
        test_move_1 = Move(test_board.array[1][0], test_board, (1, 0), (3, 0))
        test_move_1.make_move()
        test_move_2 = Move(test_board.array[3][0], test_board, (3, 0), (5, 0))

        # ACT
        valid = test_move_2.pseudo_legal()

        # ASSERT
        self.assertFalse(valid)

    def test_pseudo_legal_returns_true_for_en_passant_capture(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[3][3], test_board, (3, 3), (4, 3)).make_move()
        Move(test_board.array[6][4], test_board, (6, 4), (4, 4)).make_move()
        test_move = Move(test_board.array[4][3], test_board, (4, 3), (5, 4), capture=True)

        # ACT
        valid = test_move.pseudo_legal()

        # ASSERT
        self.assertTrue(valid)

    def test_make_move_moves_pawn(self):
        # ARRANGE
        test_board = Board()
        test_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_move.piece.position, (2, 0))

    def test_make_move_capture(self):
        # ARRANGE
        test_board = Board()
        piece_to_capture = test_board.array[6][3]
        Move(test_board.array[1][4], test_board, (1, 4), (3, 4)).make_move()
        Move(test_board.array[6][3], test_board, (6, 3), (4, 3)).make_move()
        test_move = Move(test_board.array[3][4], test_board, (3, 4), (4, 3), capture=True)

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.captured_pieces[-1], piece_to_capture)
        self.assertEqual(test_move.piece.position, piece_to_capture.position)

    def test_make_move_castling_queen_side(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][2], test_board, (0, 2), (2, 4)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[0][3], test_board, (0, 3), (2, 3)).make_move()
        Move(test_board.array[6][2], test_board, (6, 2), (5, 2)).make_move()
        Move(test_board.array[0][1], test_board, (0, 1), (2, 2)).make_move()
        Move(test_board.array[6][3], test_board, (6, 3), (5, 3)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 2), castling=Castling.QUEEN_SIDE)

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.array[0][2].symbol, "k")
        self.assertEqual(test_board.array[0][3].symbol, "r")

    def test_make_move_castling_king_side(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][5], test_board, (0, 5), (2, 3)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[0][6], test_board, (0, 6), (2, 7)).make_move()
        Move(test_board.array[6][2], test_board, (6, 2), (5, 2)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 6), castling=Castling.KING_SIDE)

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.array[0][6].symbol, "k")
        self.assertEqual(test_board.array[0][5].symbol, "r")

    def test_make_move_marks_en_passant_file(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[3][3], test_board, (3, 3), (4, 3)).make_move()
        test_move = Move(test_board.array[6][4], test_board, (6, 4), (4, 4))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.en_passant_file, 4)

    def test_make_move_promotes_pawn(self):
        test_board = Board()
        Move(test_board.array[1][1], test_board, (1, 1), (3, 1)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 2)).make_move()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][7], test_board, (6, 7), (5, 7)).make_move()
        Move(test_board.array[0][5], test_board, (0, 5), (5, 0)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 0), capture=True).make_move()
        Move(test_board.array[3][1], test_board, (3, 1), (4, 1)).make_move()
        Move(test_board.array[5][7], test_board, (5, 7), (4, 7)).make_move()
        Move(test_board.array[4][1], test_board, (4, 1), (5, 1)).make_move()
        Move(test_board.array[6][6], test_board, (6, 6), (5, 6)).make_move()
        Move(test_board.array[5][1], test_board, (5, 1), (6, 1)).make_move()
        Move(test_board.array[5][6], test_board, (5, 6), (4, 6)).make_move()
        test_move = Move(test_board.array[6][1], test_board, (6, 1), (7, 1), promotion=Queen)

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual((test_board.array[7][1].symbol, test_board.array[7][1].colour.value), ("q", 0))

    def test_make_move_en_passant_capture(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[3][3], test_board, (3, 3), (4, 3)).make_move()
        Move(test_board.array[6][4], test_board, (6, 4), (4, 4)).make_move()
        captured_piece = test_board.array[4][4]
        test_move = Move(test_board.array[4][3], test_board, (4, 3), (5, 4), capture=True)

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_move.piece.position, (5, 4))
        self.assertEqual(test_board.captured_pieces[-1], captured_piece)

    def test_make_move_removes_queen_side_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][0], test_board, (1, 0), (3, 0)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        test_move = Move(test_board.array[0][0], test_board, (0, 0), (1, 0))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, True, True, True])

    def test_make_move_removes_queen_side_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][0], test_board, (1, 0), (3, 0)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[3][0], test_board, (3, 0), (4, 0)).make_move()
        test_move = Move(test_board.array[7][0], test_board, (7, 0), (6, 0))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, False, True])

    def test_make_move_removes_king_side_castling_rights_after_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][7], test_board, (1, 7), (3, 7)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        test_move = Move(test_board.array[0][7], test_board, (0, 7), (1, 7))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, False, True, True])

    def test_make_move_removes_king_side_castling_rights_after_black_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][7], test_board, (1, 7), (3, 7)).make_move()
        Move(test_board.array[6][7], test_board, (6, 7), (5, 7)).make_move()
        Move(test_board.array[3][7], test_board, (3, 7), (4, 7)).make_move()
        test_move = Move(test_board.array[7][7], test_board, (7, 7), (6, 7))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, False])

    def test_make_move_removes_castling_rights_after_king_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (1, 4))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, False, True, True])

    def test_make_move_removes_castling_rights_after_black_king_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][4], test_board, (6, 4), (5, 4)).make_move()
        Move(test_board.array[2][4], test_board, (2, 4), (3, 4)).make_move()
        test_move = Move(test_board.array[7][4], test_board, (7, 4), (6, 4))

        # ACT
        test_move.make_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, False, False])

    def test_unmake_move(self):
        # ARRANGE
        test_board = Board()
        test_board_attributes_1 = (test_board.to_string(), test_board.side_to_move, test_board.castling_rights,
                                   test_board.en_passant_file, test_board.half_move_clock, test_board.captured_pieces)

        test_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0))
        test_move.make_move()

        # ACT
        test_move.unmake_move()
        test_board_attributes_2 = (test_board.to_string(), test_board.side_to_move, test_board.castling_rights,
                                   test_board.en_passant_file, test_board.half_move_clock, test_board.captured_pieces)

        # ASSERT
        self.assertEqual(test_board_attributes_1, test_board_attributes_2)

    def test_unmake_move_unmakes_castling_queen_side(self):
        # ARRANGE
        test_board = Board()

        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][2], test_board, (0, 2), (2, 4)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[0][3], test_board, (0, 3), (2, 3)).make_move()
        Move(test_board.array[6][2], test_board, (6, 2), (5, 2)).make_move()
        Move(test_board.array[0][1], test_board, (0, 1), (2, 2)).make_move()
        Move(test_board.array[6][3], test_board, (6, 3), (5, 3)).make_move()

        test_board_attributes_1 = (test_board.to_string(), test_board.side_to_move, test_board.castling_rights,
                                   test_board.en_passant_file, test_board.half_move_clock, test_board.captured_pieces)

        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 2), castling=Castling.QUEEN_SIDE)
        test_move.make_move()

        # ACT
        test_move.unmake_move()
        test_board_attributes_2 = (test_board.to_string(), test_board.side_to_move, test_board.castling_rights,
                                   test_board.en_passant_file, test_board.half_move_clock, test_board.captured_pieces)

        # ASSERT
        self.assertEqual(test_board_attributes_1, test_board_attributes_2)
        self.assertTrue(test_move.piece.move_count == 0)
        self.assertTrue(test_board.array[0][0].move_count == 0)

    def test_unmake_move_unmakes_castling_king_side(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][5], test_board, (0, 5), (2, 3)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[0][6], test_board, (0, 6), (2, 7)).make_move()
        Move(test_board.array[6][2], test_board, (6, 2), (5, 2)).make_move()
        test_board_attributes_1 = (test_board.to_string(), test_board.side_to_move, test_board.castling_rights,
                                   test_board.en_passant_file, test_board.half_move_clock, test_board.captured_pieces)

        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 6), castling=Castling.KING_SIDE)
        test_move.make_move()

        # ACT
        test_move.unmake_move()
        test_board_attributes_2 = (test_board.to_string(), test_board.side_to_move, test_board.castling_rights,
                                   test_board.en_passant_file, test_board.half_move_clock, test_board.captured_pieces)

        # ASSERT
        self.assertEqual(test_board_attributes_1, test_board_attributes_2)
        self.assertTrue(test_move.piece.move_count == 0)
        self.assertTrue(test_board.array[0][7].move_count == 0)

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][0], test_board, (1, 0), (3, 0)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        test_move = Move(test_board.array[0][0], test_board, (0, 0), (1, 0))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_queen_side_castling_rights_after_unmaking_black_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][0], test_board, (1, 0), (3, 0)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[3][0], test_board, (3, 0), (4, 0)).make_move()
        test_move = Move(test_board.array[7][0], test_board, (7, 0), (6, 0))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][7], test_board, (1, 7), (3, 7)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        test_move = Move(test_board.array[0][7], test_board, (0, 7), (1, 7))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_king_side_castling_rights_after_unmaking_black_rook_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][7], test_board, (1, 7), (3, 7)).make_move()
        Move(test_board.array[6][7], test_board, (6, 7), (5, 7)).make_move()
        Move(test_board.array[3][7], test_board, (3, 7), (4, 7)).make_move()
        test_move = Move(test_board.array[7][7], test_board, (7, 7), (6, 7))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_castling_rights_after_unmaking_king_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (1, 4))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_restores_castling_rights_after_unmaking_black_king_move(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][4], test_board, (6, 4), (5, 4)).make_move()
        Move(test_board.array[2][4], test_board, (2, 4), (3, 4)).make_move()
        test_move = Move(test_board.array[7][4], test_board, (7, 4), (6, 4))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, True])

    def test_unmake_move_does_not_restore_castling_rights_for_rook_that_returns_to_original_position(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][7], test_board, (1, 7), (3, 7)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        Move(test_board.array[0][7], test_board, (0, 7), (1, 7)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[1][7], test_board, (1, 7), (0, 7)).make_move()
        Move(test_board.array[5][1], test_board, (5, 1), (4, 1)).make_move()
        test_move = Move(test_board.array[0][7], test_board, (0, 7), (1, 7))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, False, True, True])

    def test_unmake_move_does_not_restore_castling_rights_for_king_that_returns_to_original_position(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][4], test_board, (0, 4), (1, 4)).make_move()
        Move(test_board.array[5][0], test_board, (5, 0), (4, 0)).make_move()
        Move(test_board.array[1][4], test_board, (1, 4), (0, 4)).make_move()
        Move(test_board.array[4][0], test_board, (4, 0), (3, 0)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (1, 4))
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [False, False, True, True])

    def test_unmake_move_restores_castling_rights_for_captured_rook(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][3], test_board, (1, 3), (2, 3)).make_move()
        Move(test_board.array[6][7], test_board, (6, 7), (5, 7)).make_move()
        Move(test_board.array[0][2], test_board, (0, 2), (5, 7), capture=True).make_move()
        Move(test_board.array[7][7], test_board, (7, 7), (5, 7), capture=True).make_move()
        Move(test_board.array[1][7], test_board, (1, 7), (2, 7)).make_move()
        Move(test_board.array[6][3], test_board, (6, 3), (5, 3)).make_move()
        Move(test_board.array[1][0], test_board, (1, 0), (2, 0)).make_move()
        Move(test_board.array[7][2], test_board, (7, 2), (2, 7), capture=True).make_move()
        Move(test_board.array[2][0], test_board, (2, 0), (3, 0)).make_move()
        Move(test_board.array[2][7], test_board, (2, 7), (3, 6)).make_move()
        Move(test_board.array[3][0], test_board, (3, 0), (4, 0)).make_move()
        test_move = Move(test_board.array[5][7], test_board, (5, 7), (0, 7), capture=True)
        test_move.make_move()

        # ACT
        test_move.unmake_move()

        # ASSERT
        self.assertEqual(test_board.castling_rights, [True, True, True, False])

    def test_legal_returns_true_for_legal_pawn_move(self):
        # ARRANGE
        test_board = Board()
        test_move = Move(test_board.array[1][3], test_board, (1, 3), (2, 3))

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_capture(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][3], test_board, (1, 3), (2, 3)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 2)).make_move()
        Move(test_board.array[2][3], test_board, (2, 3), (3, 3)).make_move()
        test_move = Move(test_board.array[5][2], test_board, (5, 2), (3, 3), capture=True)

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_move_in_check(self):
        # ARRANGE
        test_board = Board()
        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][4], test_board, (6, 4), (4, 4)).make_move()
        Move(test_board.array[1][5], test_board, (1, 5), (2, 5)).make_move()
        Move(test_board.array[4][4], test_board, (4, 4), (3, 4)).make_move()
        Move(test_board.array[1][6], test_board, (1, 6), (3, 6)).make_move()
        Move(test_board.array[7][3], test_board, (7, 3), (3, 7)).make_move()
        test_move = Move(test_board.array[2][5], test_board, (2, 5), (3, 4), capture=True)

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_true_for_legal_king_side_castle(self):
        # ARRANGE
        test_board = Board()

        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][5], test_board, (0, 5), (2, 3)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[0][6], test_board, (0, 6), (2, 7)).make_move()
        Move(test_board.array[6][2], test_board, (6, 2), (5, 2)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 2), castling=Castling.KING_SIDE)

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_true_for_legal_queen_side_castle(self):
        # ARRANGE
        test_board = Board()

        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        Move(test_board.array[0][2], test_board, (0, 2), (2, 4)).make_move()
        Move(test_board.array[6][1], test_board, (6, 1), (5, 1)).make_move()
        Move(test_board.array[0][3], test_board, (0, 3), (2, 3)).make_move()
        Move(test_board.array[6][2], test_board, (6, 2), (5, 2)).make_move()
        Move(test_board.array[0][1], test_board, (0, 1), (2, 2)).make_move()
        Move(test_board.array[6][3], test_board, (6, 3), (5, 3)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 6), castling=Castling.QUEEN_SIDE)

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertTrue(valid)

    def test_legal_returns_false_for_illegal_king_side_castle(self):
        # ARRANGE
        test_board = Board()

        Move(test_board.array[1][4], test_board, (1, 4), (2, 4)).make_move()
        Move(test_board.array[7][6], test_board, (7, 6), (5, 5)).make_move()
        Move(test_board.array[0][5], test_board, (0, 5), (2, 3)).make_move()
        Move(test_board.array[5][5], test_board, (5, 5), (3, 6)).make_move()
        Move(test_board.array[0][6], test_board, (0, 6), (2, 7)).make_move()
        Move(test_board.array[3][6], test_board, (3, 6), (2, 4), capture=True).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 2), castling=Castling.KING_SIDE)

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertFalse(valid)

    def test_legal_returns_false_for_illegal_queen_side_castle(self):
        # ARRANGE
        test_board = Board()

        Move(test_board.array[1][3], test_board, (1, 3), (3, 3)).make_move()
        Move(test_board.array[7][1], test_board, (7, 1), (5, 0)).make_move()
        Move(test_board.array[0][2], test_board, (0, 2), (2, 4)).make_move()
        Move(test_board.array[5][0], test_board, (5, 0), (3, 1)).make_move()
        Move(test_board.array[0][3], test_board, (0, 3), (2, 3)).make_move()
        Move(test_board.array[3][1], test_board, (3, 1), (2, 3), capture=True).make_move()
        Move(test_board.array[0][1], test_board, (0, 1), (2, 2)).make_move()
        Move(test_board.array[6][0], test_board, (6, 0), (5, 0)).make_move()
        test_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 6), castling=Castling.QUEEN_SIDE)

        # ACT
        valid = test_move.legal()

        # ASSERT
        self.assertFalse(valid)
