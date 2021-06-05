#!/usr/bin/env python3
from scale_mod import Scale


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
        self.scale_name = "major"


    def draw_fretboard(self):
        print('    ', end="")
        strings = []
        sc_obj = Scale(root="C", scale_name=self.scale_name)
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


if __name__ == '__main__':
    guitar = Fretboard(tuning=['E', 'A', 'D', 'G', 'B', 'E'], scale_length=13)  # haha, flats cause bad root error!
    guitar.draw_fretboard()