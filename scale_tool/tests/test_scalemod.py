#!/usr/bin/python3
import sys
import unittest as unittest
sys.path.append('../')
from scale_mod import Scale, BadRootError, BadScaleError


class Test(unittest.TestCase):

    def test_c_maj(self):
        s = Scale()
        self.assertEqual(s.scale, ['C', 'D', 'E', 'F', 'G', 'A', 'B'])

    def test_roots(self):
        key_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'D#']
        for key in key_list:
            s = Scale(root = key)
            self.assertEqual(s.root, key)

    def test_intervals(self):
        key_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        s = Scale(root = 'c')
        for key in key_list:
            self.assertEqual(s.get_interval(key_list.index(key)+1), key)

    # @unittest.skip('check that previsou test succeeds')
    def test_bad_interval(self):
        s = Scale()
        with self.assertRaises(AssertionError):
            s.get_interval(8)

    def test_bad_root(self):
        # s = Scale('2')
        with self.assertRaises(BadRootError):
            s = Scale(root='2')

    def test_bad_scale(self):
        with self.assertRaises(BadScaleError):
            s = Scale(root='c', scale_name = 'garbage')


    def test_minor(self):
        correct = ['E', 'F#', 'G', 'A', 'B', 'C', 'D']
        s = Scale(root='e', scale_name='minor')
        self.assertEqual(s.scale, correct)

if __name__ == '__main__':
    unittest.main()
