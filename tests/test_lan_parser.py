import unittest

from chess_engine import board, constants as cs, lan_parser as lp, move


class TestLanParser(unittest.TestCase):
    def test_convert_move_to_lan_converts_pawn_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x10, 0x20)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "a2-a3")

    def test_convert_move_to_lan_converts_piece_move(self):
        # ARRANGE
        test_board = board.Board()
        test_move = move.encode_move(0x01, 0x20)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "Nb1-a3")

    def test_convert_move_to_lan_converts_capture(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d5 0 3"
        )
        test_move = move.encode_move(0x34, 0x43, capture=True)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "e4xd5")

    def test_convert_move_to_lan_converts_castling_queenside(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/4pppp/pppp4/8/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 9"
        )
        test_move = move.encode_move(0x04, 0x02, castling=cs.QUEENSIDE)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "0-0-0")

    def test_convert_move_to_lan_converts_castling_kingside(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "rnbqkbnr/3ppppp/ppp5/8/8/3BP2N/PPPP1PPP/RNBQK2R w KQkq - 0 7"
        )
        test_move = move.encode_move(0x04, 0x06, castling=cs.KINGSIDE)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "0-0")

    def test_convert_move_to_lan_converts_promotion(self):
        # ARRANGE
        test_board = board.Board.of_string(
            "r1bqkbnr/pPpppp2/p1n5/6pp/8/4P3/P1PP1PPP/RNBQK1NR w KQkq - 0 13"
        )
        test_move = move.encode_move(0x61, 0x71, promotion=cs.QUEEN)

        # ACT
        test_string = lp.convert_move_to_lan(test_move, test_board)

        # ASSERT
        self.assertEqual(test_string, "b7-b8Q")
