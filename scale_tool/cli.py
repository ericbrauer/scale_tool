#!/usr/bin/env python3


class Fretboard:
    """
    Draws a fretboard based on number of strings, and scale length in frets.
    This will be written to the terminal for now. Maybe graphics eventually.
    """

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
        marker=" "
        for i, note in enumerate(self.tuning):
            if i == 0:
                print("{0:4}\u250d".format(marker), end="")
            if i == (len(self.tuning)-1):
                print('\u2501\u2501\u2501\u2511')
            else:
                print('\u2501\u2501\u2501\u252f', end="")
        

if __name__ == '__main__':
    guitar = Fretboard(tuning=['Eb', 'A', 'D', 'G', 'B', 'E'], scale_length=12)
    guitar.draw_fretboard()