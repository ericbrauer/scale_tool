#!/usr/bin/python3
import sys
import unittest as unittest
sys.path.append('../')
from scale_mod import Scale, BadRootError, BadScaleError


class Test(unittest.TestCase):

    def test_chromatic_scale(self):
        s = Scale()
        self.assertEqual(s.get_chromatic_scale('C'), ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
                     'A', 'A#', 'B'])

    def test_c_maj(self):
        s = Scale()
        self.assertEqual(s.scale, ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])

    def test_roots(self):
        key_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'D#', 'C']
        for key in key_list:
            s = Scale(root = key)
            self.assertEqual(s.root, key)

    def test_intervals(self):
        key_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
        s = Scale(root = 'c')
        for key in key_list:
            self.assertEqual(s.get_interval(key_list.index(key)+1), key)

    # @unittest.skip('check that previsou test succeeds')
    def test_bad_interval(self):
        s = Scale()
        with self.assertRaises(AssertionError):
            s.get_interval(9)

    def test_bad_root(self):
        # s = Scale('2')
        with self.assertRaises(BadRootError):
            s = Scale(root='2')

    def test_bad_scale(self):
        with self.assertRaises(BadScaleError):
            s = Scale(root='c', scale_name = 'garbage')

    def test_minor(self):
        correct = ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#', 'C']
        s = Scale(root='c', scale_name='minor')
        self.assertEqual(s.scale, correct)

    def test_minor_e(self):
        correct = ['E', 'F#', 'G', 'A', 'B', 'C', 'D', 'E']
        s = Scale(root='e', scale_name='minor')
        self.assertEqual(s.scale, correct)

    def test_locrian(self):
        correct = ['D', 'D#', 'F', 'G', 'G#', 'A#', 'C', 'D']
        s = Scale(root='d', scale_name='LOCRIAN')
        self.assertEqual(s.scale, correct)

    @unittest.skip('this is not implemented yet')
    def test_finer_adjustment(self):
        "the concept behind is to be able to set dominant, diminished, natural intervals"
        "in this example, we set a diminished third"
        correct = ['C', 'D', 'D#', 'F', 'G', 'A', 'B']
        s = Scale(ROOT='c', degree={3, -0.5})

if __name__ == '__main__':
    unittest.main()
