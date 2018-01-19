#!/usr/bin/python3
import sys
import unittest as unittest
sys.path.append('../')
from scale_mod import Scale


class Test(unittest.TestCase):

    def test_c_maj(self):
        s = Scale()
        self.assertEquals(s.scale, ['C', 'D', 'E', 'F', 'G', 'A', 'B'])

    def test_roots(self):
        key_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        for key in key_list:
            s = Scale(key)
            self.assertEquals(s.root, key)

    def test_intervals(self):
        key_list = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        s = Scale('c')
        for key in key_list:
            self.assertEquals(s.get_interval(key_list.index(key)+1), key)

    # TODO test the keyError exceptions for root and scales

    # TODO test intervals, want to extend up to twelve?

    # TODO test minor

if __name__ == '__main__':
    unittest.main()
