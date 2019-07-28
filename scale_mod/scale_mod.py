#!/usr/bin/env python3

import sys


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

    valid_scales = {
        'major':        [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        'ionian':       [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        'dorian':       [0, 1, 0.5, 1, 1, 1, 0.5, 1],
        'phrygian':     [0, 0.5, 1, 1, 1, 0.5, 1, 1],
        'lydian':       [0, 1, 1, 1, 0.5, 1, 1, 0.5],
        'mixolydian':   [0, 1, 1, 0.5, 1, 1, 0.5, 1],
        'aeolian':      [0, 1, 0.5, 1, 1, 0.5, 1, 1],
        'minor':        [0, 1, 0.5, 1, 1, 0.5, 1, 1],
        'locrian':      [0, 0.5, 1, 1, 0.5, 1, 1, 1],
        }

    class _Note:
        """
        An individual note.
        """

        sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
                       'A', 'A#', 'B']

        flat_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab',
                      'A', 'Bb', 'B']

        __slots__ = '_name', '_flat', '_next'

        def __init__(self, name, next):
            self._name = name
            self._flat = self.flat_notes(self.sharp_notes.index(name))
            self._next = next

    def __init__(self, **kwargs):
        "verify args, run methods to get scale"
        if 'root' in kwargs.keys():
            self.root = self.verify_input_root(kwargs['root'])
        if 'scale_name' in kwargs.keys():
            self.scale_name = self.verify_input_scale(kwargs['scale_name'])
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        head = self._tail._next
        return head._name

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        oldhead = self._tail._next
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = oldhead._next
            self._size -= 1
            return oldhead._name

    def enqueue(self, e):
        newest = self._Note(e, None)
        if self.is_empty():
            newest._next = newest
        else:
            newest._next = self._tail._next
            self._tail._next = newest
        self._tail = newest
        self._size += 1

    def rotate(self):
        if self._size > 0:
            self._tail = self._tail._next

    def verify_input_root(self, root):
        "verify that root specified is valid"
        root = root.upper()
        if root not in self.all_notes:
            raise BadRootError(root)
        else:
            return root

    def verify_input_scale(self, scale_name):
        "make sure input is valid, set variables to object"
        scale_name = scale_name.lower()
        if scale_name in self.valid_scales.keys():
            self.scale_name = scale_name
            self.scale = self.valid_scales[scale_name]
        else:
            raise BadScaleError(scale_name)

    def get_chromatic_scale(self):
        "returns a chromatic scale with all twelve semi-tones"
        x = self.all_notes.index(self.root)
        new_notes = self.all_notes[x:]
        for note in self.all_notes[:x]:
            new_notes.append(note)
        # new_notes.append(self.all_notes[x])
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
