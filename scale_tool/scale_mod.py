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

    root = 'C'  # let's start with C as our root
    all_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
                 'A', 'A#', 'B']
    valid_scales = {
        'major': [0, 1, 1, 0.5, 1, 1, 1],
        'minor': [0, 1, 0.5, 1, 1, 0.5, 1]
        }
    # valid_scales = [self.major, self.minor]

    def __init__(self, root='C', scale_name='major'):
        try:
            root = root.upper()
            scale_name = scale_name.lower()
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
        "returns a chromatic scale with all twelve semi-tones with root as first element"
        x = self.all_notes.index(root)
        new_notes = self.all_notes[(x):]
        for note in self.all_notes[:x]:
            new_notes.append(note)
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

    def get_valid_scales(self):
        print(self.valid_scales.keys())
        return self.valid_scales.keys()

    def get_interval(self, interval):
        "returns an interval, like fifth"
        try:
            assert interval < len(self.chromatic_scale)
        except AssertionError:
            print('your interval is bad')
        interval_note = self.scale[(interval-1)]
        print('The {} of the {} - {} scale is {}.'.format(interval,
                                                          self.root,
                                                          self.scale_name,
                                                          interval_note))
        return interval_note
