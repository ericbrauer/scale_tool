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
            use_flats = False
            self._notes = []
            root_note, root_acc = Scale._Note.parsestring(root)
            if root_acc < 0:  # if the root note is flat
                root_note, root_acc = Scale._Note.step_down((root_note, root_acc))
                use_flats = True
            accs = (0, 1)  # otherwise use sharps
            exclude = ('B', 'E')  # ie. E-sharp is just F
            for n in range(ord('A'), ord('H')):
                for acc in accs:
                    if chr(n) not in exclude or acc == 0:
                        self._notes.append(Scale._Note(chr(n), acc, use_flats))
                    if (root_note == chr(n) and acc == root_acc):  # if this our start,
                        self.pointer = len(self._notes) - 1

        def __len__(self):
            return len(self._notes)

        def __getitem__(self, position):
            position += self.pointer
            if position >= len(self._notes):
                position %= len(self._notes)
            return self._notes[position]

        def __repr__(self):
            return str(self._notes[self.pointer:] + self._notes[:self.pointer])

        def start_at(self, note):
            try:
                self.pointer = self._notes.index(note)
            except ValueError:
                print("Problem!")

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

        @classmethod
        def step_down(cls, note_tup):
            "eg. changes a D-flat into a C-sharp"
            notename, acc = note_tup
            n = ord(notename) - 1
            if n == 64:  # changes an A to a G
                n = 71
            new_nname = chr(n)
            if new_nname in ('B', 'E'):  # only one half-step btwn B and C.
                acc += 1
            else:
                acc += 2
            return (new_nname, acc)

        @classmethod
        def step_up(cls, note_tup):
            "eg. changes a C-sharp into D-flat"
            notename, acc = note_tup
            n = ord(notename) + 1
            if n == 72:  # changes a G to an A
                n = 65
            new_nname = chr(n)
            if new_nname in ('C', 'F'):  # only one half-step btwn B and C.
                acc -= 1
            else:
                acc -= 2
            return (new_nname, acc)

        def __init__(self, note_name, accidental, use_flats=False):
            self._note_name = note_name  # A-G
            self._next = next  # ?
            self._accidental = accidental  # + for sharps, - for flats
            self.dia_role = False  # its role in forming a diatonic scale
            self._use_flats = use_flats  # When notes are printed, use flat alias
            self._flat_alias = self.step_up((self._note_name, self._accidental))
            self._sharp_alias = self.step_down((self._note_name, self._accidental))

        def __eq__(self, other):
            "compare two notes"
            if isinstance(other, str):
                on, oa = self.parsestring(other)
                o = Scale._Note(on, oa)
            if isinstance(other, tuple):
                on, oa = other
                o = Scale._Note(on, oa)
            elif isinstance(other, Scale._Note):
                o = other
            ot = o.return_tuple()
            if ot == self.return_tuple():
                return True
            elif ot == self._sharp_alias:
                return True
            elif ot == self._flat_alias:
                return True
            else:
                return False

        def __repr__(self):
            if self._use_flats and self._accidental != 0:
                name, acc = self._flat_alias
            else:
                name = self._note_name
                acc = self._accidental
            suffix = ''
            if acc < 0:
                suffix = '\u266d' * abs(acc)
            elif acc > 0:
                suffix = '\u266f' * acc
            return name + suffix
        
        def return_tuple(self):
            return (self._note_name, self._accidental)

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
        s = Scale._Chromatic('C')
        # s = Scale._Chromatic('C#')
        # print(s)
        # print(s[-1])
        # print(s[4])
        # print(s[-12])
        # for note in s:
        #     print(note)



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

