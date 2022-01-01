#!/usr/bin/env python3


'''
Found https://www.mvanga.com/blog/basic-music-theory-in-200-lines-of-python
'''


class NoRootError(ValueError):
    def __init__(self, *args):
        self.message = 'please define a root note to start from.'
        super(NoRootError, self).__init__(self.message, *args)


class BadNoteError(ValueError):
    """the note you defined is not part of the Western Scale"""
    def __init__(self, root=None, *args):
        self.message = 'the note you defined is not part of the Western Scale'
        self.root = root
        super(BadNoteError, self).__init__(self.message, self.root, *args)


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
    class _Chromatic:
        """
        Create a scale a round-robin sequence of chromatic notes, given 
        """

        def __init__(self, root):
            self._notes = []
            root_note, root_acc = Scale._Note.parsestring(root)
            if root_acc < 0:  # if the root note is flat
                accs = (-1, 0)  # use flats in the chromatic scale
                exclude = ('C', 'F')  # ie. C-flat is just B
            else:
                accs = (0, 1)  # otherwise use sharps
                exclude = ('B', 'E')  # ie. E-sharp is just F
            for n in range(ord('A'), ord('H')):
                for acc in accs:
                    if chr(n) not in exclude or acc == 0:
                        self._notes.append(Scale._Note(chr(n), acc))
                    if (root_note == chr(n) and acc == root_acc):  # if this our start,
                        self.pointer = len(self._notes) - 1

        def __len__(self):
            return len(self._notes)

        def __getitem__(self, position):
            position += self.pointer
            if position >= len(self._notes):
                position %= len(self._notes)
            return self._notes[position]

        def is_empty(self):
            return self._size == 0

    class _Note:
        """
        Dialing back the complexity of this object. Notes are composed of a
        'name' (A-G) as well as an 'accidental' (number of sharps and flats).
        A note can be identified in different ways: E-flat is the same as D-sharp. A note can't be changed once created, but will have its other 
        'names' recorded internally. 
        A note also has its relationship inside the scale recorded, so that a 
        note D inside of a C major scale will 'know' that it is a second.
        Let's gooo
        """

        @classmethod
        def parsestring(cls, note):
            "will attempt to create a tuple of name/accidental, given a string"
            try:
                note_name, *acc = [char for char in note]  # split up a string
                assert note_name in [chr(n) for n in range(ord('A'), ord('H'))]
            except AssertionError:
                raise BadNoteError(note)
            x = 0
            for char in acc:
                if char in ('#', '\u266f'):  # final all sharps
                    x += 1
                elif char in ('b', '\u266d'):  # find all flats
                    x -= 1
                else:
                    raise BadNoteError(note)
            return (note_name, x)  # return as tuple

        @classmethod
        def isvalid(cls, note):
            "check if a note is valid or not"
            try:
                cls.parsestring(note)
            except BadNoteError:
                return False
            return True

        def __init__(self, note_name, accidental, focused=False):
            self._note_name = note_name  # A-G
            self._next = next  # ?
            self._accidental = accidental  # + for sharps, - for flats
            self.dia_role = False  # its role in forming a diatonic scale
            self._focused = focused  # is considered to be the root/start of sequence

        # def __str__(self):
        #     suffix = ''
        #     if self.accidental < 0:
        #         suffix = 'b' * abs(self.accidental)
        #     elif self.accidental > 0:
        #         suffix = '#' * abs(self.accidental)
        #     return self.note_name + suffix.replace('b', '\u266d') \
        #         .replace('#', '\u266f')

        def __repr__(self):
            suffix = ''
            if self._accidental < 0:
                suffix = '\u266d' * abs(self._accidental)
            elif self._accidental > 0:
                suffix = '\u266f' * self._accidental
            return self._note_name + suffix


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
        Scale._Note.parsestring('D')
        Scale._Note.parsestring('Ab')
        Scale._Note.parsestring('F#')
        Scale._Note.isvalid('G#')
        Scale._Note.isvalid('T')
        Scale._Note.isvalid('B%')
        s = Scale._Chromatic('Db')
        print(s[0])
        print(s[-1])
        print(s[4])
        print(s[-12])



    @classmethod
    def get_scales(cls):
        "return the keys of the valid scales dict"
        return cls.scales.keys()

    @classmethod
    def get_all_notes(cls):
        "return all possible notes of the Western scale"
        return cls.all_notes

if __name__ == "__main__":
    c = Scale()

