#!/usr/bin/env python3

import sys
import getopt

# TODO: Could we use a generator for something?
# TODO: function that returns a repeating set on notes, specified in args
# TODO: interval should return only index int
# TODO: so what if we implemented a dict, where the key is the interval (1,2,5, etc.) and the value is the note?

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

    all_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
                 'A', 'A#', 'B']

    flat_notes = {'C': 'C', 'C#': 'Db', 'D': 'D', 'D#':'Eb', 'E':'E',
                  'F':'F', 'F#':'Gb', 'G':'G', 'G#':'Ab', 'A':'A', 'A#':'Bb', 'B':'B'}

    scale_notes = []

    valid_scales = {
        'major':        [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        'ionian':       [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        'dorian':       [0, 1, 0.5, 1, 1, 1, 0.5, 1],
        'phrygian':     [0, 0.5, 1, 1, 1, 0.5, 1, 1],
        'lydian':       [0, 1, 1, 1, 0.5, 1, 1, 0.5],
        'mixolydian':   [0, 1, 1, 0.5, 1, 1, 0.5, 1],
        'aeolian':      [0, 1, 0.5, 1, 1, 0.5, 1, 1],
        'minor':        [0, 1, 0.5, 1, 1, 0.5, 1, 1],
        'locrian':      [0, 0.5, 1, 1, 0.5, 1, 1, 1]
        }

    def __init__(self, **kwargs):
        "verify args, run methods to get scale"
        try:
            assert 'root' in kwargs.keys()
        except:
            raise NoRootError
        try:
            self.root = kwargs['root'].upper()
            assert self.root in self.all_notes
        except:
            raise BadRootError(self.root)
        if 'scale_name' not in kwargs.keys():
            raise BadScaleError('You must specify a scale name to proceed')
        try:
            self.scale_name = kwargs['scale_name'].lower()
            assert self.scale_name in self.valid_scales.keys()
            self.scale = self.valid_scales[self.scale_name]
        except:
            raise BadScaleError(self.scale_name)
        self.set_chromatic_scale(self.root)

    def set_chromatic_scale(self, root):
        "returns a chromatic scale with all twelve semi-tones"
        x = self.all_notes.index(root)
        new_notes = self.all_notes[x:]
        for note in self.all_notes[:x]:
            new_notes.append(note)
        new_notes.append(self.all_notes[x])
        self.chromatic_scale = new_notes

    def get_chromatic_scale(self):
        return self.chromatic_scale


    def get_scale_notes(self):
        "returns a list of notes in the defined scale"
        element = 0
        scale_notes = []
        for index in range(len(self.scale)):
            element = int(element + (self.scale[index] * 2))
            scale_notes.append(self.chromatic_scale[element])
        return scale_notes

    def get_flat_note(self, note):
        return self.flat_notes[note]

    def get_flat_scale(self):
        flat_scale = []
        for element in self.get_scale_notes():
            flat_scale.append(self.get_flat_note(element))
        return flat_scale

    @classmethod
    def get_valid_scales(cls):
        "return the keys of the valid scales dict"
        return cls.valid_scales.keys()

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
        # Scale.get_valid_scales()
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
        for scale in Scale.get_valid_scales():
            print(scale)
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
