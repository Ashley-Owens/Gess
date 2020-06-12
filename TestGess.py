# Author: Ashley Owens
# Date: 6/4/2020
# Description: CS 162, Portfolio Project Test File

from GessGame import GessGame, GessBoard
import unittest


class GessGameTester(unittest.TestCase):
    """
    Contains unit tests for the GessGame file.
    """
    def setUp(self):
        self.game = GessGame()
        self.board = GessBoard()
        self.board.set_positions()

    def test_turn(self):
        """
        Tests initial attributes and changes made to self._turn via set_turn method.
        :return:
        """
        self.assertEqual('BLACK', self.game.get_turn())
        self.game.set_turn()
        self.assertEqual('WHITE', self.game.get_turn())
        self.game.set_turn()
        self.assertEqual('BLACK', self.game.get_turn())

    def test_game_state(self):
        """
        Tests initial attributes and changes made to game_state via resign_game method.
        """
        self.assertEqual('UNFINISHED', self.game.get_game_state())
        self.assertEqual(self.game.resign_game(), 'WHITE_WON')

        # Starts a new game and changes player turn to 'WHITE'.
        self.game = GessGame()
        self.game.set_turn()
        self.assertEqual(self.game.resign_game(), 'BLACK_WON')

    def test_positions_dict(self):
        """
        Tests both GessGame instantiation of positions dict and GessBoard positions dict.
        """
        self.game.make_move('b7', 'c7')

        # Tests GessGame instantiation of positions dict.
        for i in range(1, 20):
            self.assertIn('A'+str(i), self.game._positions)
            self.assertIn('J'+str(i), self.game._positions)
            self.assertIn('T'+str(i), self.game._positions)
            self.assertNotIn('U'+str(i), self.game._positions)
            self.assertNotIn('A'+str(21), self.game._positions)
            self.assertNotIn('@'+str(i), self.game._positions)

        # Positions change in instantiated object dict.
        self.assertEqual(self.game._positions['C7'], " ")
        self.assertEqual(self.game._positions['D7'], "B")

        # Tests GessBoard positions dict.
        for i in range(1, 20):
            self.assertIn('A'+str(i), self.board._positions)
            self.assertIn('J'+str(i), self.board._positions)
            self.assertIn('T'+str(i), self.board._positions)
            self.assertNotIn('U'+str(i), self.board._positions)
            self.assertNotIn('A'+str(21), self.board._positions)
            self.assertNotIn('@'+str(i), self.board._positions)

        # No changes are made to GessBoard dictionary from make_move call.
        self.assertEqual(self.board._positions['C7'], "B")
        self.assertEqual(self.board._positions['D7'], " ")

    def test_make_move(self):
        """
        Tests make_move method including player ability to move in all directions with or without center stone.
        Tests invalid movement attempts, player attempts to destroy own ring, and game winning scenarios.
        """

        # Tests both players ability to make moves in cardinal directions,
        # regardless of distance, while capturing or not capturing stones.
        self.assertTrue(self.game.make_move('c3', 'c5'))
        self.assertTrue(self.game.make_move('c18', 'C16'))
        self.assertTrue(self.game.make_move('r3', 's3'))
        self.assertTrue(self.game.make_move('R18', 's18'))
        self.assertTrue(self.game.make_move('l8', 'l6'))
        self.assertTrue(self.game.make_move('l13', 'L15'))
        self.assertTrue(self.game.make_move('s3', 'r3'))
        self.assertTrue(self.game.make_move('S18', 'r18'))
        self.assertTrue(self.game.make_move('C6', 'C13'))
        self.assertTrue(self.game.make_move('q18', 'S18'))
        self.assertTrue(self.game.make_move('C12', 'r12'))
        self.assertTrue(self.game.make_move('C16', 'b16'))
        self.assertTrue(self.game.make_move('r12', 'C12'))
        self.assertTrue(self.game.make_move('b16', 'b15'))
        self.assertTrue(self.game.make_move('D4', 'b4'))
        self.assertTrue(self.game.make_move('r15', 'r14'))
        self.assertTrue(self.game.make_move('c12', 'Q12'))
        self.assertTrue(self.game.make_move('b15', 'b14'))
        self.assertTrue(self.game.make_move('q12', 'c12'))
        self.assertTrue(self.game.make_move('g14', 'e14'))

        # Tests both players ability to make moves in diagonal directions,
        # regardless of distance, while capturing or not capturing stones.
        self.game = GessGame()
        self.assertTrue(self.game.make_move('c3', 'b3'))
        self.assertTrue(self.game.make_move('c18', 'b18'))
        self.assertTrue(self.game.make_move('f3', 'c6'))
        self.assertTrue(self.game.make_move('F18', 'c15'))
        self.assertTrue(self.game.make_move('f8', 'f5'))
        self.assertTrue(self.game.make_move('f13', 'f15'))
        self.assertTrue(self.game.make_move('c6', 'J13'))
        self.assertTrue(self.game.make_move('c15', 'j8'))
        self.assertTrue(self.game.make_move('J13', 'o8'))
        self.assertTrue(self.game.make_move('j8', 'g5'))
        self.assertTrue(self.game.make_move('o8', 'g16'))
        self.assertTrue(self.game.make_move('g5', 'O13'))
        self.assertTrue(self.game.make_move('g16', 'l11'))
        self.assertTrue(self.game.make_move('o13', 'p12'))
        self.assertTrue(self.game.make_move('L11', 'd3'))
        self.assertTrue(self.game.make_move('p12', 'M15'))

        # Tests attempts to destroy player's own ring.
        self.game = GessGame()
        self.assertFalse(self.game.make_move('n3', 'm3'))
        self.assertFalse(self.game.make_move('n18', 'm18'))

        # Tests invalid movement attempts.
        self.assertFalse(self.game.make_move('b5', 'a5'))
        self.assertFalse(self.game.make_move('I18', 'i20'))
        self.assertFalse(self.game.make_move('r3', 'r1'))
        self.assertFalse(self.game.make_move('r18', 't18'))
        self.assertFalse(self.game.make_move('p1', 'p2'))
        self.assertFalse(self.game.make_move('r20', 'R19'))
        self.assertFalse(self.game.make_move('t3', 's3'))
        self.assertFalse(self.game.make_move('a16', 'b16'))
        self.assertFalse(self.game.make_move('c6', 'd7'))
        self.assertFalse(self.game.make_move('C15', 'd14'))
        self.assertFalse(self.game.make_move('r3', 'q4'))
        self.assertFalse(self.game.make_move('r18', 'q17'))
        self.assertFalse(self.game.make_move('f3', 'F6'))
        self.assertFalse(self.game.make_move('f18', 'f15'))
        self.assertFalse(self.game.make_move('f3', 'd3'))
        self.assertFalse(self.game.make_move('f18', 'G18'))
        self.assertFalse(self.game.make_move('h3', 'h12'))
        self.assertFalse(self.game.make_move('h14', 'n14'))
        self.assertFalse(self.game.make_move('Z6', 's7'))
        self.assertFalse(self.game.make_move('c!', 'd17'))
        self.assertFalse(self.game.make_move('c3', 'c3'))
        self.assertFalse(self.game.make_move('=@6', 'd7'))
        self.assertFalse(self.game.make_move('c6', '=====+1'))
        self.assertFalse(self.game.make_move('c15', 'c12'))
        self.assertFalse(self.game.make_move('c10', 'c11'))
        self.assertFalse(self.game.make_move('c7', 'c8'))

        # Tests destruction of WHITE player's ring.
        self.game = GessGame()
        self.game.make_move('m7', 'k7')
        self.game.make_move('m14', 'K14')
        self.game.make_move('l3', 'l6')
        self.game.make_move('l18', 'l15')
        self.game.make_move('l6', 'l9')
        self.game.make_move('l15', 'l13')
        self.assertTrue(self.game.make_move('L9', 'l11'))
        self.assertEqual(self.game.get_game_state(), 'BLACK_WON')
        self.assertFalse(self.game.make_move('c18', 'c16'))

        # Tests destruction of BLACK player's ring.
        self.game = GessGame()
        self.game.make_move('m7', 'k7')
        self.game.make_move('m14', 'k14')
        self.game.make_move('l3', 'l6')
        self.game.make_move('l18', 'l15')
        self.game.make_move('l6', 'l9')
        self.game.make_move('l15', 'l13')
        self.game.make_move('l9', 'l10')
        self.assertTrue(self.game.make_move('l13', 'l12'))
        self.assertEqual(self.game.get_game_state(), 'WHITE_WON')
        self.assertFalse(self.game.make_move('c3', 'c5'))