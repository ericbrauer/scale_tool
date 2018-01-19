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

    def __init__(self, root='C', scale='major'):
        try:
            root = root.upper()
            scale = scale.lower()
            if root in self.all_notes:
                self.root = root
            else:
                raise BadRootError(root)
            if scale in self.valid_scales.keys():
                self.scale = self.valid_scales[scale]
            else:
                raise BadScaleError(scale)
        except (BadRootError, BadScaleError):
            print("something is wrong")
            raise  # fucking creates a C major scale anyway
        self.scale_notes = []



    def calculate_scale_notes(self):
        element = 0
        for index in range(len(self.scale)):
            print('index: '+str(index))
            element = int(element + (self.scale[index] * 2))
            print('element: '+str(element))
            self.scale_notes.append(self.all_notes[element])
            print(self.scale_notes)
        # assert len(self.scale_notes) == 7

    def return_scale_notes(self):
        return self.scale_notes
