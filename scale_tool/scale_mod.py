#!/usr/bin/env python3

import sys
import getopt
from typing import get_args

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
    A class to define a musical scale based on two arguments: the root notes
    and the scale name. Not defining these arguments will create a C Major
    scale. Defining a scale that hasn't been implemented (or a root note that
    isn't between A and G#) will raise custom exceptions defined above.
    """

    class Note:
        """
        This note object should be able to contain its sharp/flat 'aliases'
        and hopefully allow more functionality (octaves, interval id?, pitch)
        in the future.
        """

        sharps = ['C#', 'D#', 'F#', 'G#', 'A#']
        flats = ['Db', 'Eb', 'Gb', 'Ab', 'Bb']
        notes = [chr(n) for n in range(ord('A'), ord('H'))]

        def __init__(self, note):
            self.note_name = note[0]  # first char is the letter
            self.index = self.notes.index(self.note_name)  # still needed?
            self.accidental = 0  # integer indicating sharp/flat
            acci = note[1:]  # for all other chars, set accidental
            for char in acci:
                if char == '#':
                    self.accidental += 1  # each sharp = 1.
                elif char == 'b':
                    self.accidental -= 1

        def simplify(self):
            "will return a simpler note name reducing accidentals"
            acc = self.accidental
            if acc == 0:
                return self
            new_n = self
            while True:
                if new_n.accidental >= 1 and new_n.note_name in ['B', 'E']:
                    new_n.next_note()  # so that a B sharp becomes C
                if new_n.accidental <= -1 and new_n.note_name in ['C', 'F']:
                    new_n.prev_note()  # so that a C flat becomes B
                if abs(new_n.accidental) > 1:
                    while new_n.accidental > 1:
                        new_n.next_note()  # so that a G sharp-sharp becomes A
                    while new_n.accidental < -1:
                        new_n.prev_note()
                else:
                    return new_n

        def replace(self, new_note):
            "changes note name to new_note without changing tone"
            origin = self.note_name  # make sure just the name
            target = new_note.note_name
            # need to see if it's simpler to go up or down the scale
            fwd = self.notes.index(target) - self.notes.index(origin)
            if fwd > 0:
                while self.note_name != new_note:
                    self.next_note()
            elif fwd < 0:
                while self.note_name != new_note:
                    self.prev_note()
            else:
                pass
            return self

        def next_note(self):
            "change Note name without affecting its tone"
            try:
                self.index += 1  # basic way to get next letter in sequence
                self.note_name = self.notes[self.index]
            except IndexError:  # when we reach the end and loop to beginning
                self.index = 0
                self.note_name = self.notes[self.index]
            if self.note_name in ['F', 'C']:
                self.accidental -= 1
            else:
                self.accidental -= 2
            return self

        def prev_note(self):
            try:
                self.index -= 1
                self.note_name = self.notes[self.index]
            except IndexError:
                self.index = -1
                self.note_name = self.notes[self.index]
            if self.note_name in ['E', 'B']:
                self.accidental += 1
            else:
                self.accidental += 2
            return self

        def acc(self):
            return self.accidental

        def __add__(self, value):
            "this will increase accidentals to make more sharp"
            "1 = a semi-tone"
            self.accidental += value
            return self

        def __sub__(self, value):
            "this will increase accidentals to make more flat"
            "1 = a semi-tone"
            self.accidental -= abs(value)
            return self

        def __eq__(self, other):
            "the either the flat or sharp will return True"
            if isinstance(other, str):  # if the other is a string,
                return str(self.simplify()) == other  # simplify self
            if self.simplify() == other.simplify():
                return True
            else:
                return False

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

        # def __index__(self):
        #     return self.index

        # def set_index(self, num):
        #     self.index = int(num)

    sharp_notes_str = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯',
                       'A', 'A♯', 'B']

    flat_notes_str = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭',
                      'A', 'B♭', 'B']

    scale_notes = []

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
        self.maj_scale = []
        self.start = kwargs["root"]  # where do we start
        try:
            self.chromatic = kwargs["chromatic"]  # will create sharps
        except KeyError:
            self.chromatic = False
        note_index = self.notes.index(str(self.start)[0])
        self.notenames = self.notes[note_index:] + self.notes[:note_index]
        self.notes = [Scale.Note(n) for n in self.notenames]
        try:
            assert 'root' in kwargs.keys()
        except AssertionError:
            raise NoRootError
        try:
            self.root = Scale.Note(kwargs['root'])
        except AssertionError:
            raise BadRootError(self.root)
        if 'scale_name' not in kwargs.keys():
            raise BadScaleError('You must specify a scale name to proceed')
        try:
            self.scale = kwargs['scale_name']
            assert self.scale in self.scales.keys()
        except AssertionError:
            raise BadScaleError(self.scale)
        self.set_chromatic_scales()
        self.create_major_scale()
        self.scale_notes = self.create_specified_scale_from_maj()

    def __repr__(self):
        return self.notes

    def __iter__(self):
        "create iterable"
        self.n = 0
        return self

    def __next__(self):
        try:
            rtrn = self.scale_notes[self.n]
            self.n += 1
            return rtrn
        except IndexError:
            self.n = 0
            return self.scale_notes[self.n]

    def __getitem__(self, position):
        return self.scale_notes[position]

    def create_major_scale(self):
        "this will always create a major scale, that can then be modified"
        score = self.root.acc()  # if root note has accidental, set it here
        for i, note in enumerate(self.notes):
            to_add = note
            if score > 0:
                to_add = to_add + score  # create C# if needed
            elif score < 0:
                to_add = to_add - score  # create Cb if needed
            self.maj_scale.append(to_add)
            score += self.maj_formula[i]
            try:
                next_val = self.notes[i+1]
            except IndexError:
                next_val = self.notes[0]
            if next_val in ['C', 'F']:  # going from B to C is only a half step
                score -= 1
            else:
                score -= 2

    def create_specified_scale_from_maj(self):
        "use formulas to adapt given maj scale"
        formula = self.scales[self.scale]
        maj = self.maj_scale
        scale = []
        maj_ind = 0  # used to get next letter in maj for naming
        for step in formula:  # we will step through 1, 2, flat 3, etc.
            sharps = 0
            flats = 0
            tf = 0
            for char in step:  # distinguishes between b/# symbols and numbers
                if not char.isdigit():
                    if char == 'b':
                        flats += 1
                    elif char == '#':
                        sharps += 1
                    step = step.replace(char, '')  # remove flats/sharps
            index = int(step) - 1  # index starts at zero!
            if index >= len(maj):  # this should convert 9 to 2 for example
                index %= len(maj)
            tf = int(sharps) - int(flats)  # tf will set accidental
            note = Scale.Note(str(maj[index]))  # important we create new notes
            if tf > 0:
                note + tf
            elif tf < 0:
                note - tf
            turn_into = self.maj_scale[maj_ind]  # turn into used because a scale shouldn't contain two E's, for instance.
            scale.append(note.replace(turn_into))  # will set a note to a new letter without changing its tone
            maj_ind += 1
        return scale

    def set_chromatic_scales(self):
        self.chr_sc_flats = self.create_chromatic_scale(self.root, 'flat')
        self.chr_sc_sharps = self.create_chromatic_scale(self.root, 'sharp')

    def get_chromatic_scale(self, first_note=None, fl_sh='sharp'):
        "returns either flat or sharp variation"
        if first_note is None:
            first_note = self.root
        first_note_ind = self.chr_sc_sharps.index(first_note)
        if fl_sh == 'sharp':
            return self.chr_sc_sharps[first_note_ind:] + \
                   self.chr_sc_sharps[:first_note_ind]
        else:
            return self.chr_sc_flats[first_note_ind:] + \
                   self.chr_sc_flats[:first_note_ind]

    def create_chromatic_scale(self, first_note=None, fl_sh='sharp'):
        if fl_sh == 'sharp':
            allnotes = self.sharp_notes_str
        else:
            allnotes = self.flat_notes_str
        if first_note is None:
            first_note = str(self.root)
        x = allnotes.index(first_note)
        new_notes = allnotes[x:]
        for index, note in enumerate(allnotes[:x]):
            new_notes.append(Scale.Note(note))
        # new_notes.append(Scale.Note(allnotes[x]))
        return new_notes

    def get_scale_notes(self):
        "returns a list of notes in the defined scale"
        element = 0
        chr = self.get_chromatic_scale()
        scale_notes = []
        for index in range(len(self.scale)-1):
            element = int(element + (self.scale[index] * 2))
            scale_notes.append(chr[element])
        return scale_notes

    def get_sc_notes_with_blanks(self):
        "same as get_sc_notes_but has empty elements for notes not in scale"
        sc_notes = self.get_scale_notes()
        chr_notes = self.get_chromatic_scale()
        rtrn = []
        for i in chr_notes:
            if i in sc_notes:
                rtrn.append(i)
            else:
                rtrn.append(None)
        return rtrn

    def get_next(self, first_note=None):
        "generator. first arg sets where we start, not root"
        if first_note is None:
            first_note = self.root
        sc_notes = self.get_scale_notes()
        chr_notes = self.get_chromatic_scale(first_note)
        while True:
            for i in chr_notes:
                if i in sc_notes:
                    yield i
                else:
                    yield None

    def get_flat_note(self, note):
        return self.flat_notes[note]

    def get_flat_scale(self):
        flat_scale = []
        for element in self.get_scale_notes():
            flat_scale.append(self.get_flat_note(element))
        return flat_scale

    @classmethod
    def get_scales(cls):
        "return the keys of the valid scales dict"
        return cls.scales.keys()

    @classmethod
    def get_all_notes(cls):
        "return all possible notes of the Western scale"
        return cls.all_notes

    def get_interval(self, interval):
        "returns an interval, like fifth"
        try:
            assert interval < (len(self.scale)+1)
        except AssertionError:
            print('your interval is bad')
            raise
        interval_note = self.scale[(interval-1)]
        print('The {} of the {} - {} scale is {}.'.format(interval,
                                                          self.root,
                                                          self.scale_name,
                                                          interval_note))
        return interval_note


def usage():
    print('Use -h or --help to read this message')
    print('Use -r or --root= to set a root note for the scale')
    print('Use -n or --scale_note= to set a type of scale to return')


def main(argv):
    "here's where we handle system arguments in case people wish to use this"
    "module as a standalone cli tool"
    try:
        opts, args = getopt.getopt(argv,
                                   "hr:n:",
                                   ["help",
                                    "root=",
                                    "scale_name="])
        if opts is None:  # this  is not working
            raise getopt.GetoptError
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    # try:
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-r", "--root"):
            root = str(arg)
        elif opt in ("-n", "--scale_name"):
            scale_name = str(arg)
        else:
            print('use -h for help')
            sys.exit(1)

    try:
        s = Scale(root=root, scale_name=scale_name)
        print(s.get_scale_notes())
        sys.exit(0)
    except BadRootError:
        print('Error: the root you entered was not valid.')
        print('Acceptable root notes are any of the following: ')
        for note in Scale.get_all_notes():
            print(note)
        sys.exit(2)
    except BadScaleError:
        print('Error: we didn\'t recognize the scale you specified.')
        print('Acceptable scales include any of the following: ')
        for scale in Scale.get_scales():
            print(scale)
        sys.exit(2)


if __name__ == '__main__':
    c = Scale(root="Db", scale_name="minor")
    # i = iter(c)
    # print(next(i))
    # print(next(i))
    # print(next(i))
    # print(next(i))
    # print(next(i))
    # print(next(i))
    # print(next(i))
    # print(next(i))
    b = Scale(root="C", scale_name="major_blues")
    print(b.get_chromatic_scale())
    print(c.get_scale_notes())
    print(c.get_sc_notes_with_blanks())
