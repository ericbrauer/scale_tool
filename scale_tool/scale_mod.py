#!/usr/bin/env python3

import sys
import getopt
from typing import get_args

# TODO: interval should return only index int
# TODO: so what if we implemented a dict, where the key is the interval (1,2,5, etc.) and the value is the note?

'''
Found later: https://www.mvanga.com/blog/basic-music-theory-in-200-lines-of-python
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
            self.note_name = note[0]  # just the letter
            self.index = self.notes.index(self.note_name)  # still needed?
            self.accidental = 0
            acci = note[1:]
            for char in acci:
                if char == '#':
                    self.accidental += 1
                elif char == 'b':
                    self.accidental -= 1

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
            if self.note_name + self.accidental == other:
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


    sharp_notes_str = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
                   'A', 'A#', 'B']

    flat_notes_str = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 
                  'A', 'Bb', 'B']

    scale_notes = []

    notes = [chr(n) for n in range(ord('A'), ord('H'))]

# this way of defining intervals sucks, actually.
    scales = {
        'major': ['1', '2', '3', '4', '5', '6', '7'],
        'minor': ['1', '2', 'b3', '4', '5', 'b6', 'b7']
    }

    maj_formula = [2, 2, 1, 2, 2, 2, 1] 

    maj_scale = []


    old_scales = {
        'major':        [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        'minor':        [0, 1, 0.5, 1, 1, 0.5, 1, 1],
        'melodic_minor': [0, 1, 0.5, 0.5, 1, 1, 1, 0.5],
        'harmonic_minor': [0, 1, 0.5, 0.5, 1, 1, 0.5, 0.5],
        'major_blues': [0, 1, 0.5, 0.5, 1.5, 1, 1.5],
        #'minor_blues':
        'pentatonic_major': [0, 1, 1, 0.5, 1.5, 1, 1.5]
        #'pentatonic_minor':
        # 'pentatonic_blues': 
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
        "verify args, run methods to get scale"
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
        note_index = self.notes.index(kwargs['root'][0])
        self.notes = self.notes[note_index:] + self.notes[:note_index]
        #self.set_chromatic_scales()
        self.create_major_scale()
        self.scale_notes = self.create_specified_scale_from_maj()
        print(self.scale_notes)

    def create_major_scale(self):
        "this will always create a major scale, that can then be modified"
        score = self.root.acc()  # if root note has accidental, set it here
        for i, note in enumerate(self.notes):
            to_add = Scale.Note(note)  # create C
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
        for step in formula:
            sharps = 0
            flats = 0
            for char in step:
                if not char.isdigit():
                    if char == 'b':
                        flats += 1
                    elif char == '#':
                        sharps += 1
                    step = step.replace(char, '')
            index = int(step) - 1
            if index >= len(maj):  # this should convert 9 to 2 for example
                index %= len(maj)
            tf = int(sharps) - int(flats)
            if tf > 0:
                note = maj[index] + tf
            elif tf < 0:
                note = maj[index] - tf
            else:
                note = maj[index]
            scale.append(note)
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
            return self.chr_sc_sharps[first_note_ind:] + self.chr_sc_sharps[:first_note_ind]
        else:
            return self.chr_sc_flats[first_note_ind:] + self.chr_sc_flats[:first_note_ind]

    def create_chromatic_scale(self, first_note=None, fl_sh='sharp'):
        if fl_sh == 'sharp':
            allnotes = self.sharp_notes
        else:
            allnotes = self.flat_notes
        if first_note is None:
            first_note = self.root
        x = allnotes.index(first_note)
        new_notes = allnotes[x:]
        for index, note in enumerate(allnotes[:x]):
            new_notes.append(Scale.Note(note, index))
        # new_notes.append(Scale.Note(allnotes[x]))
        return new_notes

    def get_scale_notes(self):
        "returns a list of notes in the defined scale"
        element = 0
        chr = self.get_chromatic_scale()
        scale_notes = []
        for index in range(len(self.scale)-1):
            element = int(element + (self.scale[index] * 2))
            # chr[element].set_index(index)  # set the index to its position in the scale
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
        opts, args = getopt.getopt(argv, "hr:n:", ["help", "root=", "scale_name="])
        if opts is None: # this  is not working
            raise getopt.GetoptError
    except getopt.GetoptError:
        usage()
        # Scale.get_scales()
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
    # except BadRootError:
    # TODO: no catch of no root variable here.

    try:
        # ok, problem here. if root is set in options, I want it passed to init.
        # But if not, it shouldn't be passed.
        # this is... overloading? Check the old C++ book maybe.
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
    #print(c.get_scale_notes())
    #print(c.get_sc_notes_with_blanks())
