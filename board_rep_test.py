import unittest
import board_rep as b


class TestMoveMaking(unittest.TestCase):
    def test_convert_lan_to_move(self):
        """Checks that the function correctly converts user strings to move details."""
        self.assertIsNone(b.new_game.convert_lan_to_move("gedfvfew")[0])
        self.assertIsNone(b.new_game.convert_lan_to_move("Pe4xe5Q")[0])

        test_class_1 = b.new_game.convert_lan_to_move("e4-e5")[0]
        test_attributes_1 = [test_class_1.piece, test_class_1.piece_class, test_class_1.colour, test_class_1.start,
                             test_class_1.destination, test_class_1.castling, test_class_1.is_capture,
                             test_class_1.en_passant, test_class_1.promotion]
        self.assertEqual(test_attributes_1, [None, b.Pawn, b.Colour.WHITE, (3, 4), (4, 4), None, False, False, None])

        test_class_2 = b.new_game.convert_lan_to_move("0-0")[0]
        test_attributes_2 = [test_class_2.piece, test_class_2.piece_class, test_class_2.colour, test_class_2.start,
                             test_class_2.destination, test_class_2.castling, test_class_2.is_capture,
                             test_class_2.en_passant, test_class_2.promotion]
        self.assertEqual(test_attributes_2, [b.game_board.array[0][4], b.King, b.Colour.WHITE, (0, 4), (0, 6),
                                             b.Castling.KING_SIDE, False, False, None])

        test_class_3 = b.new_game.convert_lan_to_move("d2-d8Q")[0]
        test_attributes_3 = [test_class_3.piece, test_class_3.piece_class, test_class_3.colour, test_class_3.start,
                             test_class_3.destination, test_class_3.castling, test_class_3.is_capture,
                             test_class_3.en_passant, test_class_3.promotion]
        self.assertEqual(test_attributes_3, [b.game_board.array[1][3], b.Pawn, b.Colour.WHITE, (1, 3), (7, 3), None,
                                             False, False, b.Queen])


if __name__ == '__main__':
    unittest.main()
