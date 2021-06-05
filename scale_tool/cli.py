#!/usr/bin/env python3
from scale_mod import Scale
import argparse


class Fretboard:
    """
    Draws a fretboard based on number of strings, and scale length in frets.
    This will be written to the terminal for now. Maybe graphics eventually.
    """

    zero_fret = ['┍', '━', '┯', '┑']
    normal_fret = ['├', '─', '┼', '┤', '│']

    def __init__(self, **kwargs):
        try:
            assert 'tuning' in kwargs.keys()
        except:
            raise ValueError("Please specify tuning, in a list, from lowest to highest.")
        try:
            assert 'scale_length' in kwargs.keys()
        except:
            raise ValueError("Please specify a length of the fretboard in number of frets.")
        self.tuning = kwargs['tuning']
        self.scale_length = kwargs['scale_length']
        self.root = kwargs['root']
        self.scale_name = kwargs['scale']


    def draw_fretboard(self):
        print('    ', end="")
        strings = []
        sc_obj = Scale(root=self.root, scale_name=self.scale_name)
        for note in self.tuning:
            strings.append(sc_obj.get_next(note))  # this is a generator
# TODO: We haven't built a way to start on a certain non-root note!!
        for note in strings:
            out = next(note)
            if out is None:
                out = " "
            print("{0:^4}".format(str(out)), end="")
        print()
        for y in range(self.scale_length):
            if y in [0, 3, 5, 7, 9, 12]:
                marker = y
            else:
                marker = " "
            if y == 0:
                for x, note in enumerate(strings):
                    if x == 0:
                        print("{0:>4}\u250d".format(marker), end="")
                    if x == (len(self.tuning)-1):
                        print('{:\u2501>4}'.format(self.zero_fret[3]))
                    else:
                        print('{:\u2501>4}'.format(self.zero_fret[2]), end="")
            else:
                # create space
                for x, note in enumerate(strings):
                    if x == 0:
                        print("{0:>4}│".format(" "), end="")
                    if x == (len(strings)-1):
                        print('{:>4}'.format(self.normal_fret[4]))
                    else:
                        print('{:>4}'.format(self.normal_fret[4]), end="")
                # create note 
                for x, note in enumerate(strings):
                    if x == 0:
                        print("{0:>4}│".format(marker), end="")
                    if x == (len(strings)-1):
                        out = next(note)
                        if out is None:
                            out = " "
                        print('{:^3}{}'.format(str(out), self.normal_fret[4]))
                    else:
                        out = next(note)
                        if out is None:
                            out = " "
                        print('{:^3}{}'.format(str(out), self.normal_fret[4]), end="")
                # create fret
                for x, note in enumerate(strings):
                    if x == 0:
                        print("{0:>4}├".format(" "), end="")
                    if x == (len(strings)-1):
                        print('{:─>4}'.format(self.normal_fret[3]))
                    else:
                        print('{:─>4}'.format(self.normal_fret[2]), end="")


def argparse_setup():
    "invoke argparse, passes to obj in global scope"
    parser = argparse.ArgumentParser(description="Creates a fretboard for learning scales and chords",epilog="Copyright 2021 - Eric Brauer")
    parser.add_argument("-r", "--root", default='C', help="Root note of the scale you are defining.")
    parser.add_argument("-s", "--scale", choices=list(Scale.get_scales()),  default='major', help="Name of the scale.")  # get possibles from Scale_mod
    parser.add_argument("-t", "--tuning", default='EADGBE', help="The tuning of the instrument.")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = argparse_setup()
    # scale_options = Scale.get_scales()
    print(args)
    guitar = Fretboard(tuning=['Eb', 'Ab', 'Db', 'Gb', 'Bb', 'Eb'], scale_length=13, root=args.root, scale=args.scale)  # haha, flats cause bad root error!
    guitar.draw_fretboard()