#!/usr/bin/python3
import sys
import unittest as unittest
sys.path.append('../scale_tool')

from scale_tool.scale_mod import (BadNoteError,
                                  Scale, BadScaleError, NoRootError)


class TestNote(unittest.TestCase):
    "tests for Note's class methods"

    def test_note_parsestring(self):
        "test the class method for Note"
        input = ['D', 'C', 'F', 'E', 'Eb', 'G#']
        output = [('D', 0),
                  ('C', 0),
                  ('F', 0),
                  ('E', 0),
                  ('E', -1),
                  ('G', 1)]
        for i, o in zip(input, output):
            self.assertEqual(Scale._Note.parsestring(i), o)

    def test_note_error(self):
        input = ['H', 'a', 'B%', 'bb']
        for i in input:
            with self.assertRaises(BadNoteError):
                Scale._Note.parsestring(i)

    def test_note_valid(self):
        input1 = ['H', 'a', 'B%', 'bb']
        input2 = ['C#', 'Bbb', 'E#', 'G\u266d']
        for i in input1:
            self.assertFalse(Scale._Note.isvalid(i))
        for i in input2:
            self.assertTrue(Scale._Note.isvalid(i))

    def test_down(self):
        input = [('D', 0),
                 ('C', 0),
                 ('F', 1),
                 ('E', -1),
                 ('A', -1)]
        output = [('C', 2),
                  ('B', 1),
                  ('E', 2),
                  ('D', 1),
                  ('G', 1)]
        for i, o in zip(input, output):
            self.assertEqual(Scale._Note.step_down(i), o)

    def test_up(self):
        input = [('C', 2),
                 ('B', 1),
                 ('E', 2),
                 ('D', 1),
                 ('G', 1)]
        output = [('D', 0),
                  ('C', 0),
                  ('F', 1),
                  ('E', -1),
                  ('A', -1)]
        for i, o in zip(input, output):
            self.assertEqual(Scale._Note.step_up(i), o)

    def test_eq(self):
        s = Scale._Note('C', 1)
        si = Scale._Note('D', -1)
        input = ('C#', 'Db', 'B##', si, ('C', 1))
        for i in input:
            self.assertTrue(s == i)
        input2 = ('C', 'F', ('D', 2))
        for i in input2:
            self.assertFalse(s == i)


class TestChromaticC(unittest.TestCase):

    def setUp(self) -> None:
        self.s = Scale._Chromatic("C")

    def test_scale(self):
        expected = "[C, C\u266f, D, D\u266f, E, F, F\u266f, G, G\u266f, A, A\u266f, B]"
        self.assertEqual(str(self.s), expected)

    def test_items(self):
        data = {
                 0: 'C',
                 1: 'C\u266f',
                 4: 'E',
                 -1: 'B',
                 12: 'C',
                 -12: 'C',
                 -3: 'A'
                }
        for k, v in data.items():
            self.assertEqual(str(self.s[k]), v)


class TestChromaticCSharp(unittest.TestCase):

    def setUp(self) -> None:
        self.s = Scale._Chromatic("C#")

    def test_scale(self):
        expected = "[C\u266f, D, D\u266f, E, F, F\u266f, G, G\u266f, A, A\u266f, B, C]"
        self.assertEqual(str(self.s), expected)

    def test_items(self):
        data = {
                 0: 'C\u266f',
                 1: 'D',
                 4: 'F',
                 -1: 'C',
                 12: 'C\u266f',
                 -12: 'C\u266f',
                 -5: 'G\u266f'
                }
        for k, v in data.items():
            self.assertEqual(str(self.s[k]), v)


class TestChromaticDFlat(unittest.TestCase):

    def setUp(self) -> None:
        self.s = Scale._Chromatic("Db")

    def test_scale(self):
        expected = "[D\u266d, D, E\u266d, E, F, G\u266d, G, A\u266d, A, B\u266d, B, C]"
        self.assertEqual(str(self.s), expected)

    def test_items(self):
        data = {
                 0: 'D\u266d',
                 1: 'D',
                 5: 'G\u266d',
                 -1: 'C',
                 12: 'D\u266d',
                 -12: 'D\u266d',
                 -4: 'A'
                }
        for k, v in data.items():
            self.assertEqual(str(self.s[k]), v)


class TestScale(unittest.TestCase):
    "diatonic scale tests"

    def test_c_maj(self):
        s = Scale(root='C', scale='major')
        self.assertEqual(str(s), '[C, D, E, F, G, A, B]')

    def test_majors(self):
        "there should be one note name per scale"
        input = ['C', 'C#', 'Db', 'D', 'Gb', 'G']
        output = [
            '[C, D, E, F, G, A, B]',
            '[C♯, D♯, E♯, F♯, G♯, A♯, B♭]',
            '[D♭, E♭, F, G♭, A♭, B♭, C]',
            '[D, E, F♯, G, A, B, C♯]',
            '[G♭, A♭, B♭, C♭, D♭, E♭, F]',
            '[G, A, B, C, D, E, F♯]'
            ]
        for i, o in zip(input, output):
            s = Scale(root=i, scale='major')
            self.assertEqual(str(s), o)

    def test_bad_root(self):
        # s = Scale('2')
        with self.assertRaises(BadNoteError):
            s = Scale(root='2')

    def test_bad_scale(self):
        with self.assertRaises(BadScaleError):
            s = Scale(root='C', scale='garbage')

    # def test_minor(self):
    #     correct = ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#', 'C']
    #     s = Scale(root='c', scale_name='minor')
    #     self.assertEqual(s.get_scale_notes(), correct)

    # def test_minor_e(self):
    #     correct = ['E', 'F#', 'G', 'A', 'B', 'C', 'D', 'E']
    #     s = Scale(root='e', scale_name='minor')
    #     self.assertEqual(s.get_scale_notes(), correct)

    # def test_flat_scale(self):
    #     correct = ['D', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']
    #     s = Scale(root='d', scale_name='LOCRIAN')
    #     self.assertEqual(s.get_flat_scale(), correct)


if __name__ == '__main__':
    unittest.main()
