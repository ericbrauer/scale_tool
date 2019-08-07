#!/usr/bin/env python3


class Fretboard:
    """
    Draws a fretboard based on number of strings, and scale length in frets.
    This will be written to the terminal for now. Maybe graphics eventually.
    """

    zero_fret = ['┍', '━', '┯', '┑']
    normal_fret = ['├', '─', '┼', '┤']

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

    def draw_fretboard(self):
        print('    ', end="")
        for note in (self.tuning):
            print("{0:^4}".format(note), end="")
        print()
        for y in range(self.scale_length):
            if y in [0, 3, 5, 7, 9, 12]:
                marker = y
            else:
                marker = " "
            if y == 0:
                for x, note in enumerate(self.tuning):
                    if x == 0:
                        print("{0:>4}\u250d".format(marker), end="")
                    if x == (len(self.tuning)-1):
                        print('{:\u2501>4}'.format(self.zero_fret[3]))
                    else:
                        print('{:\u2501>4}'.format(self.zero_fret[2]), end="")
            else:
                for x, note in enumerate(self.tuning):
                    if x == 0:
                        print("{0:>4}├".format(marker), end="")
                    if x == (len(self.tuning)-1):
                        print('{:─>4}'.format(self.normal_fret[3]))
                    else:
                        print('{:─>4}'.format(self.normal_fret[2]), end="")

        

if __name__ == '__main__':
    guitar = Fretboard(tuning=['Eb', 'A', 'D', 'G', 'B', 'E'], scale_length=12)
    guitar.draw_fretboard()