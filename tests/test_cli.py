#!/usr/bin/python3
import sys
import unittest as unittest
sys.path.append('../scale_tool')
from cli import Fretboard 


class Test(unittest.TestCase):

    def test_no_tuning(self):
        with self.assertRaises(ValueError):
            guitar = Fretboard()

    def test_no_length(self):
        with self.assertRaises(ValueError):
            guitar = Fretboard(tuning=['E', 'A', 'D', 'G', 'B', 'E'])
        
    def test_drawing(self):
        guitar = Fretboard(tuning=['E', 'A', 'D', 'G', 'B', 'E'], scale_length=12)
        guitar.draw_fretboard()

if __name__ == '__main__':
    unittest.main()