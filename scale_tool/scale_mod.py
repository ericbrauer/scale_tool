#!/usr/bin/env python3

import sys
import getopt

# TODO: Coming back to it months later.. tried to run cli.py. Move getopts stuff to cli.py
# TODO: Could we use a generator for something?
# TODO: btw, all tests failed.
# TODO: put unit tests here, in if __main__ etc. Refer to data structs book for guidance
# TODO: look into linked list for a possible data structure, instead appending a piece at a time

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
        if 'root' in kwargs.keys():
            root = kwargs['root'].upper()
        else:
            root = 'C'
        if 'scale_name' in kwargs.keys():
            scale_name = kwargs['scale_name'].lower()
        else:
            scale_name = 'major'
        self.verify_input(root, scale_name)

    def verify_input(self, root, scale_name):
        "make sure input is valid, set variables to object"
        try:
            if root in self.all_notes:
                    self.root = root
                    self.chromatic_scale = self.get_chromatic_scale(root)
            else:
                raise BadRootError(root)
            if scale_name in self.valid_scales.keys():
                self.scale_name = scale_name
                self.scale = self.valid_scales[scale_name]
                self.get_scale_notes()
            else:
                raise BadScaleError(scale_name)
        except (BadRootError, BadScaleError):
            # print("something is wrong")
            raise

    def get_chromatic_scale(self, root='c'):
        "returns a chromatic scale with all twelve semi-tones"
        x = self.all_notes.index(root)
        new_notes = self.all_notes[x:]
        for note in self.all_notes[:x]:
            new_notes.append(note)
        new_notes.append(self.all_notes[x])
        return new_notes

    def get_scale_notes(self):
        "returns a list of notes in the defined scale"
        element = 0
        scale_notes = []
        for index in range(len(self.scale)):
            element = int(element + (self.scale[index] * 2))
            scale_notes.append(self.chromatic_scale[element])
        return scale_notes

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
