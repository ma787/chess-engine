import unittest

from chess_engine import attributes as attrs, board, lan_parser, move, pieces


class TestLanParser(unittest.TestCase):
    def test_convert_lan_to_move_converts_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_string = "a2-a3"
        expected_move = move.Move((1, 0), (2, 0), pieces.Pawn)

        # ACT
        test_move = lan_parser.convert_lan_to_move(test_string, test_board.side_to_move)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_piece_move(self):
        # ARRANGE
        test_board = board.Board()
        lan_parser.convert_lan_to_move("d2-d3", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("b7-b6", test_board.side_to_move).make_move(
            test_board
        )
        test_string = "Bc1-f4"
        expected_move = move.Move((0, 2), (3, 5), pieces.Bishop)

        # ACT
        test_move = lan_parser.convert_lan_to_move(test_string, test_board.side_to_move)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_capture(self):
        # ARRANGE
        test_board = board.Board()
        lan_parser.convert_lan_to_move("e2-e4", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("d7-d5", test_board.side_to_move).make_move(
            test_board
        )
        test_string = "e4xd5"
        expected_move = move.Move((3, 4), (4, 3), pieces.Pawn, capture=True)

        # ACT
        test_move = lan_parser.convert_lan_to_move(test_string, test_board.side_to_move)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_piece_capture(self):
        # ARRANGE
        test_board = board.Board()
        lan_parser.convert_lan_to_move("c2-c4", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("h7-h6", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("c4-c5", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("h6-h5", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("c5-c6", test_board.side_to_move).make_move(
            test_board
        )
        test_string = "Nb8xc6"
        expected_move = move.Move((7, 1), (5, 2), pieces.Knight, capture=True)

        # ACT
        test_move = lan_parser.convert_lan_to_move(test_string, test_board.side_to_move)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_promotion(self):
        # ARRANGE
        test_board = board.Board()
        test_string = "a2-a3Q"
        expected_move = move.Move((1, 0), (2, 0), pieces.Pawn, promotion=pieces.Queen)

        # ACT
        test_move = lan_parser.convert_lan_to_move(test_string, test_board.side_to_move)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_lan_to_move_converts_castling_queenside_move(self):
        # ARRANGE
        test_board = board.Board()
        lan_parser.convert_lan_to_move("d2-d4", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("a7-a6", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("Bc1-e3", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("b7-b6", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("Qd1-d3", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("c7-c6", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("Nb1-c3", test_board.side_to_move).make_move(
            test_board
        )
        lan_parser.convert_lan_to_move("d7-d6", test_board.side_to_move).make_move(
            test_board
        )
        test_string = "0-0-0"
        expected_move = move.Move(
            (0, 4), (0, 2), pieces.King, castling=attrs.Castling.QUEEN_SIDE
        )

        # ACT
        test_move = lan_parser.convert_lan_to_move(test_string, test_board.side_to_move)

        # ASSERT
        self.assertEqual(test_move, expected_move)

    def test_convert_move_to_lan_converts_pawn_move(self):
        # ARRANGE
        test_move = move.Move((1, 0), (2, 0), pieces.Pawn)

        # ACT
        test_string = lan_parser.convert_move_to_lan(test_move)

        # ASSERT
        self.assertEqual(test_string, "a2-a3")