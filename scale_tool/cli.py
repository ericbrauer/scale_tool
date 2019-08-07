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

    