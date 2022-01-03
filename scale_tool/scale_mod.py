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
    Doing a rethink. A scale is chromatic, made up of note objects.
    Some notes are considered to be members of a diatonic scale.

    Using 'scale', we will create a chromatic scale,
    with notes that have diatonic flags within. The type of
    diatonic scale is specified when we create the new Scale Object.
    """
    class _Chromatic:
        """
        Create a scale a round-robin sequence of chromatic notes, given
        """

        intervals = [
            ['P1', 'd2'],  # Perfect unison   Diminished second
            ['m2', 'A1'],  # Minor second     Augmented unison
            ['M2', 'd3'],  # Major second     Diminished third
            ['m3', 'A2'],  # Minor third      Augmented second
            ['M3', 'd4'],  # Major third      Diminished fourth
            ['P4', 'A3'],  # Perfect fourth   Augmented third
            ['d5', 'A4'],  # Diminished fifth Augmented fourth
            ['P5', 'd6'],  # Perfect fifth    Diminished sixth
            ['m6', 'A5'],  # Minor sixth      Augmented fifth
            ['M6', 'd7'],  # Major sixth      Diminished seventh
            ['m7', 'A6'],  # Minor seventh    Augmented sixth
            ['M7', 'd8'],  # Major seventh    Diminished octave
            ['P8', 'A7'],  # Perfect octave   Augmented seventh
        ]

        def __init__(self, root):
            use_flats = False
            self._notes = []
            root_note, root_acc = Scale._Note.parsestring(root)
            if root_acc < 0:  # if the root note is flat
                root_note, root_acc = (
                    Scale._Note.step_down((root_note,
                                           root_acc)))
                use_flats = True
            accs = (0, 1)  # otherwise use sharps
            exclude = ('B', 'E')  # ie. E-sharp is just F
            for n in range(ord('A'), ord('H')):
                for acc in accs:
                    if chr(n) not in exclude or acc == 0:
                        self._notes.append(Scale._Note(chr(n), acc, use_flats))
                    if (root_note == chr(n)
                        and acc == root_acc):  # if this our start,
                        self.pointer = len(self._notes) - 1
            self.set_intervals()

        def set_intervals(self):
            "apply intervals to the chromatic scale"
            notes = self._notes[self.pointer:] + self._notes[:self.pointer]
            for n, i in zip(notes, self.intervals):
                n.set_interval(i)

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
        Dialing back the complexity of this object.
        Notes are composed of a 'name' (A-G) as well
        as an 'accidental' (number of sharps and flats).
        A note can be identified in different ways: E-flat is the
        same as D-sharp. A note can't be changed
        once created, but will have its other 'names'
        recorded internally as aliases.
        A note also has its relationship inside the
        chromatic scale recorded, so that a note D
        inside of a C chromatic scale will 'know'
        that it is a Major second / diminished minor third.
        From this we can derive diatonic scales/chords.
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
            self._accidental = accidental  # + for sharps, - for flats
            self.dia_role = []  # its role in forming a diatonic scale
            # self._use_flats = use_flats  # When notes are printed, use flats
            self._flat_alias = self.step_up((self._note_name,
                                             self._accidental))
            self._sharp_alias = self.step_down((self._note_name,
                                                self._accidental))
            " pref repr used to define how the note is named."
            " if the root is flat, we use the flat alias"
            if use_flats and self._accidental != 0:
                self._pref_repr = self._flat_alias
            else:
                self._pref_repr = (self._note_name, self._accidental)

        def letter_up(self):
            "changes pref repr so C#->Db"
            self._pref_repr = self._flat_alias

        def letter_down(self):
            "changes pref repr so Db->C#"
            self._pref_repr = self._sharp_alias

        def set_interval(self, intervals):
            "intervals here are a list of two"
            "for example, maj 3rd, dim 4th"
            self.dia_role = intervals

        def get_interval(self, alt=False):
            "return first interval, unless specified"
            if alt:
                return self.dia_role[1]
            else:
                return self.dia_role[0]

        # not sure if this is the right approach
        def __contains__(self, interval):
            "sees if an interval is in the note"
            for i in self.dia_role:
                if i == interval:
                    return interval
            return None

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
            name, acc = self._pref_repr
            suffix = ''
            if acc < 0:
                suffix = '\u266d' * abs(acc)
            elif acc > 0:
                suffix = '\u266f' * acc
            return name + suffix

        def return_tuple(self):
            return (self._note_name, self._accidental)

# this way of defining intervals sucks, actually.
    scales = {  # key: P: perfect, M: major, m: minor
        'major': ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7'],
        'minor': ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'm7'],
        'melodic_minor': ['P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'M7'],
        'harmonic_minor': ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'M7'],
        'major_blues': ['P1', 'M2', 'm3', 'M3', 'P5', 'M6'],
        'minor_blues': ['P1', 'm3', 'P4', 'd5', 'P5', 'm7'],
        'pentatonic_major': ['P1', 'M2', 'M3', 'P5', 'M6'],
        'pentatonic_minor': ['P1', 'm3', 'P4', 'P5', 'm7'],
        'pentatonic_blues': ['P1', 'm3', 'P4', 'd5', 'P5', 'm7']
    }

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
        try:
            self.root = kwargs['root']
        except KeyError:
            raise NoRootError()
            return 0

        self._chr_scale = Scale._Chromatic(self.root)

        try:
            self.dia_name = kwargs['scale']
            assert self.dia_name in self.scales.keys()
            self.dia_scale = self.create_diatonic()
        except (KeyError, AssertionError):
            raise BadScaleError(self.dia_name)

    def create_diatonic(self, placeholder=False):
        "build a diatonic list. placeholder creates an empty item for notes not in scale"
        output = []
        intervals = self.scales[self.dia_name]
        note_gen = (n for n in self._chr_scale)  # creates a generator
        first = True
        prev = 0
        for step in intervals:
            while True:
                note = next(note_gen)  # get next note in sequence
                if step in note:
                    let = ord(note.return_tuple()[0])  # 65 from A#
                    if let == 65 and prev != 65:  # if current is A
                        prev = 64  # G becomes 1 before A
                    if let - prev > 1 and not first:  # eg: A - C = 2
                        note.letter_down()
                    elif let - prev < 1 and not first:  # eg: Eb - E = 0
                        note.letter_up()
                    output.append(note)
                    prev = ord(str(note)[0])  # grab '65' from 'A#'
                    first = False
                    break
                elif placeholder is not False:
                    output.append(placeholder)
                    # TODO make sure that no notenames repeat.
        return output

    def index(self, note):
        "return the position of note"
        return self.dia_scale.index(note)

    def __len__(self):
        return len(self.dia_scale)

    def __getitem__(self, position):
        return self.dia_scale[position]

    def __repr__(self):
        return str(self.dia_scale)

    @classmethod
    def get_scales(cls):
        "return the keys of the valid scales dict"
        return cls.scales.keys()

    @classmethod
    def get_all_notes(cls):
        "return all possible notes of the Western scale"
        return cls.all_notes


if __name__ == "__main__":
    for i in ['C', 'C#', 'Db', 'D', 'Gb', 'G']:
        c = Scale(root=i, scale='minor')
        print(c)
    x = c.index('D')
    print(x)
