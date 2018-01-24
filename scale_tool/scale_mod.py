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
                self.scale = self.get_scale_notes(self.valid_scales[scale_name])
            else:
                raise BadScaleError(scale_name)
        except (BadRootError, BadScaleError):
            print("something is wrong")
            raise

    def get_chromatic_scale(self, root):
        "returns a chromatic scale with all twelve semi-tones"
        x = self.all_notes.index(root)
        new_notes = self.all_notes[x:]
        for note in self.all_notes[:x]:
            new_notes.append(note)
        new_notes.append(self.all_notes[x])
        return new_notes

    def get_scale_notes(self, scale):
        "returns a list of notes in the defined scale"
        element = 0
        scale_notes = []
        for index in range(len(scale)):
            element = int(element + (scale[index] * 2))
            scale_notes.append(self.chromatic_scale[element])
        print(scale_notes)
        return scale_notes

    @staticmethod
    def get_valid_scales(self):
        "return the keys of the valid scales dict"
        print(self.valid_scales.keys())
        return self.valid_scales.keys()

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
