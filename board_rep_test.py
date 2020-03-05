import unittest
from board_rep import *


class TestMoveMaking(unittest.TestCase):
    def test_parse_string(self):
        self.assertEqual(parse_string("a1b2"), [21, 32])
        self.assertEqual(parse_string("move1"), [])
        self.assertEqual(parse_string("a9b3"), [])
        self.assertEqual(parse_string("a3h9"), [])
        self.assertEqual(parse_string("t3b2"), [])

    def test_check_location(self):
        self.assertEqual(check_location([47, 57]), None)
        self.assertEqual(check_location([31, 41]), white_pawn)

    def test_check_move_distance(self):
        self.assertEqual(white_bishop, [23, 68])
