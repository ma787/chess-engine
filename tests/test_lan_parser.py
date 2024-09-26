import unittest

from chess_engine import board, lan_parser as lp, move


class TestLanParser(unittest.TestCase):
    def test_convert_lan_to_move_converts_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_string = "a2-a3"
        expected_move = move.encode_move((1, 0), (2, 0))

        # ACT
        test_move = lp.convert_lan_to_move(test_string, test_board)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_piece_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(lp.convert_lan_to_move("d2-d3", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("b7-b6", test_board), test_board)
        test_string = "Bc1-f4"
        expected_move = move.encode_move((0, 2), (3, 5))

        # ACT
        test_move = lp.convert_lan_to_move(test_string, test_board)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(lp.convert_lan_to_move("e2-e4", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("d7-d5", test_board), test_board)
        test_string = "e4xd5"
        expected_move = move.encode_move((3, 4), (4, 3), capture=True)

        # ACT
        test_move = lp.convert_lan_to_move(test_string, test_board)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_piece_capture(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(lp.convert_lan_to_move("c2-c4", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("h7-h6", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("c4-c5", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("h6-h5", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("c5-c6", test_board), test_board)
        test_string = "Nb8xc6"
        expected_move = move.encode_move((7, 1), (5, 2), capture=True)

        # ACT
        test_move = lp.convert_lan_to_move(test_string, test_board)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_promotion(self):
        # ARRANGE
        test_board = board.Board()
        test_string = "a2-a3Q"
        expected_move = move.encode_move((1, 0), (2, 0), promotion=5)

        # ACT
        test_move = lp.convert_lan_to_move(test_string, test_board)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_castling_queenside_move(self):
        # ARRANGE
        test_board = board.Board()
        move.make_move(lp.convert_lan_to_move("d2-d4", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("a7-a6", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("Bc1-e3", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("b7-b6", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("Qd1-d3", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("c7-c6", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("Nb1-c3", test_board), test_board)
        move.make_move(lp.convert_lan_to_move("d7-d6", test_board), test_board)
        test_string = "0-0-0"
        expected_move = move.encode_move((0, 4), (0, 2), castling=2)

        # ACT
        test_move = lp.convert_lan_to_move(test_string, test_board)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_move_to_lan_converts_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move((1, 0), (2, 0))

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "a2-a3")
