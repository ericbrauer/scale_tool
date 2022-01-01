#!/usr/bin/env python3


'''
Found https://www.mvanga.com/blog/basic-music-theory-in-200-lines-of-python
'''


class NoRootError(ValueError):
    def __init__(self, *args):
        self.message = 'please define a root note to start from.'
        super(NoRootError, self).__init__(self.message, *args)


class BadRootError(ValueError):
    """the note you defined is not part of the Western Scale"""
    def __init__(self, root, *args):
        self.message = 'the note you defined is not part of the Western Scale'
        self.root = root
        super(BadRootError, self).__init__(self.message, self.root, *args)


class BadScaleError(ValueError):
    """the scale you defined isn't one that has been implemented yet"""
    def __init__(self, scale, *args):
        self.message = "the scale you defined isn't one that has been "\
                        + "implemented yet"
        self.scale = scale
        super(BadScaleError, self).__init__(self.message, self.scale, *args)


class Scale:
    """
    Doing a rethink. A scale is chromatic, made up of note objects. Some notes are considered to be members of a diatonic scale.

    Using 'scale', we will create a chromatic scale, with notes that have diatonic flags within. The type of diatonic scale is specified when we 
    create the new Scale Object.
    """

    class Note:
        """
        Dialing back the complexity of this object. Notes are composed of a
        'name' (A-G) as well as an 'accidental' (number of sharps and flats).
        A note can be identified in different ways: E-flat is the same as D-sharp. A note can't be changed once created, but will have its other 
        'names' recorded internally. 
        A note also has its relationship inside the scale recorded, so that a 
        note D inside of a C major scale will 'know' that it is a second.
        Let's gooo
        """


        def __str__(self):
            suffix = ''
            if self.accidental < 0:
                suffix = 'b' * abs(self.accidental)
            elif self.accidental > 0:
                suffix = '#' * abs(self.accidental)
            return self.note_name + suffix.replace('b', '\u266d') \
                .replace('#', '\u266f')

        def __repr__(self):
            suffix = ''
            if self.accidental < 0:
                suffix = 'b' * abs(self.accidental)
            elif self.accidental > 0:
                suffix = '#' * self.accidental
            return self.note_name + suffix.replace('b', '\u266d') \
                .replace('#', '\u266f')


    notes = [chr(n) for n in range(ord('A'), ord('H'))]

# this way of defining intervals sucks, actually.
    scales = {
        'major': ['1', '2', '3', '4', '5', '6', '7'],
        'minor': ['1', '2', 'b3', '4', '5', 'b6', 'b7'],
        'melodic_minor': ['1', '2', 'b3', '4', '5', '6', '7'],
        'harmonic_minor': ['1', '2', 'b3', '4', '5', 'b6', '7'],
        'major_blues': ['1', '2', 'b3', '3', '5', '6'],
        'minor_blues': ['1', 'b3', '4', 'b5', '5', 'b7'],
        'pentatonic_major': ['1', '2', '3', '5', '6'],
        'pentatonic_minor': ['1', 'b3', '4', '5', 'b7'],
        'pentatonic_blues': ['1', 'b3', '4', 'b5', '5', 'b7']
    }

    maj_formula = [2, 2, 1, 2, 2, 2, 1]

    modes = {
        'ionian':       [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        'dorian':       [0, 1, 0.5, 1, 1, 1, 0.5, 1],
        'phrygian':     [0, 0.5, 1, 1, 1, 0.5, 1, 1],
        'lydian':       [0, 1, 1, 1, 0.5, 1, 1, 0.5],
        'mixolydian':   [0, 1, 1, 0.5, 1, 1, 0.5, 1],
        'aeolian':      [0, 1, 0.5, 1, 1, 0.5, 1, 1],
        'locrian':      [0, 0.5, 1, 1, 0.5, 1, 1, 1]
    }

    def __init__(self, **kwargs):


    @classmethod
    def get_scales(cls):
        "return the keys of the valid scales dict"
        return cls.scales.keys()

    @classmethod
    def get_all_notes(cls):
        "return all possible notes of the Western scale"
        return cls.all_notes



