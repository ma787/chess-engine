import unittest
import board_rep as b

game_board = b.ChessBoard()
v_board = b.ChessBoard()
new_game = b.Game(game_board, v_board)


class TestMoveMaking(unittest.TestCase):
    def test_convert_lan_to_move(self):
        """Checks that the function correctly converts user strings to move details."""

        self.assertIsNone(new_game.convert_lan_to_move("gedfvfew"))
        self.assertIsNone(new_game.convert_lan_to_move("Pe4xe5Q"))
        self.assertIsNone(new_game.convert_lan_to_move("e4-e5"))

        test_class_2 = new_game.convert_lan_to_move("0-0")
        test_attributes_2 = [test_class_2.piece, test_class_2.piece_class, test_class_2.colour, test_class_2.start,
                             test_class_2.destination, test_class_2.castling, test_class_2.is_capture,
                             test_class_2.en_passant, test_class_2.promotion]
        self.assertEqual(test_attributes_2, [game_board.array[0][4], b.King, b.Colour.WHITE, (0, 4), (0, 6),
                                             b.Castling.KING_SIDE, False, False, None])

        test_class_3 = new_game.convert_lan_to_move("d2-d8Q")
        test_attributes_3 = [test_class_3.piece, test_class_3.piece_class, test_class_3.colour, test_class_3.start,
                             test_class_3.destination, test_class_3.castling, test_class_3.is_capture,
                             test_class_3.en_passant, test_class_3.promotion]
        self.assertEqual(test_attributes_3, [game_board.array[1][3], b.Pawn, b.Colour.WHITE, (1, 3), (7, 3), None,
                                             False, False, b.Queen])

        test_class_4 = new_game.convert_lan_to_move("0-0-0")
        test_attributes_4 = [test_class_4.piece, test_class_4.piece_class, test_class_4.colour, test_class_4.start,
                             test_class_4.destination, test_class_4.castling, test_class_4.is_capture,
                             test_class_4.en_passant, test_class_4.promotion]
        self.assertEqual(test_attributes_4, [game_board.array[0][4], b.King, b.Colour.WHITE, (0, 4), (0, 2),
                                             b.Castling.QUEEN_SIDE, False, False, None])


if __name__ == '__main__':
    unittest.main()
