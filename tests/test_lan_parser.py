import unittest

from chess_engine.board import Board
from chess_engine.attributes import Castling
from chess_engine.lan_parser import convert_lan_to_move, convert_move_to_lan
from chess_engine.move import Move
from chess_engine.pieces import Queen



class TestLanParser(unittest.TestCase):
    def test_convert_lan_to_move_converts_pawn_move(self):
        # ARRANGE
        test_board = Board()
        test_string = "a2-a3"

        # ACT
        test_move = convert_lan_to_move(test_string, test_board)
        expected_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0))

        # ASSERT
        self.assertEqual(test_move.__dict__, expected_move.__dict__)

    def test_convert_lan_to_move_converts_piece_move(self):
        # ARRANGE
        test_board = Board()
        convert_lan_to_move("d2-d3", test_board).make_move()
        convert_lan_to_move("b7-b6", test_board).make_move()
        test_string = "Bc1-f4"

        # ACT
        test_move = convert_lan_to_move(test_string, test_board)
        expected_move = Move(test_board.array[0][2], test_board, (0, 2), (3, 5))

        # ASSERT
        self.assertEqual(test_move.__dict__, expected_move.__dict__)

    def test_convert_lan_to_move_converts_capture(self):
        # ARRANGE
        test_board = Board()
        convert_lan_to_move("e2-e4", test_board).make_move()
        convert_lan_to_move("d7-d5", test_board).make_move()
        test_string = "e4xd5"

        # ACT
        test_move = convert_lan_to_move(test_string, test_board)
        expected_move = Move(test_board.array[3][4], test_board, (3, 4), (4, 3), capture=True)

        # ASSERT
        self.assertEqual(test_move.__dict__, expected_move.__dict__)

    def test_convert_lan_to_move_converts_piece_capture(self):
        # ARRANGE
        test_board = Board()
        convert_lan_to_move("c2-c4", test_board).make_move()
        convert_lan_to_move("h7-h6", test_board).make_move()
        convert_lan_to_move("c4-c5", test_board).make_move()
        convert_lan_to_move("h6-h5", test_board).make_move()
        convert_lan_to_move("c5-c6", test_board).make_move()
        test_string = "Nb8xc6"

        # ACT
        test_move = convert_lan_to_move(test_string, test_board)
        expected_move = Move(test_board.array[7][1], test_board, (7, 1), (5, 2), capture=True)

        # ASSERT
        self.assertEqual(test_move.__dict__, expected_move.__dict__)

    def test_convert_lan_to_move_converts_promotion(self):
        # ARRANGE
        test_board = Board()
        test_string = "a2-a3Q"

        # ACT
        test_move = convert_lan_to_move(test_string, test_board)
        expected_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0), promotion=Queen)

        # ASSERT
        self.assertEqual(test_move.__dict__, expected_move.__dict__)

    def test_convert_lan_to_move_converts_castling_queenside_move(self):
        # ARRANGE
        test_board = Board()
        convert_lan_to_move("d2-d4", test_board).make_move()
        convert_lan_to_move("a7-a6", test_board).make_move()
        convert_lan_to_move("Bc1-e3", test_board).make_move()
        convert_lan_to_move("b7-b6", test_board).make_move()
        convert_lan_to_move("Qd1-d3", test_board).make_move()
        convert_lan_to_move("c7-c6", test_board).make_move()
        convert_lan_to_move("Nb1-c3", test_board).make_move()
        convert_lan_to_move("d7-d6", test_board).make_move()
        test_string = "0-0-0"

        # ACT
        test_move = convert_lan_to_move(test_string, test_board)
        expected_move = Move(test_board.array[0][4], test_board, (0, 4), (0, 2), castling=Castling.QUEEN_SIDE)

        # ASSERT
        self.assertEqual(test_move.__dict__, expected_move.__dict__)

    def test_convert_move_to_lan_converts_pawn_move(self):
        # ARRANGE
        test_board = Board()
        test_move = Move(test_board.array[1][0], test_board, (1, 0), (2, 0))

        # ACT
        test_string = convert_move_to_lan(test_move)

        # ASSERT
        self.assertEqual(test_string, "a2-a3")
