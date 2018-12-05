#!/usr/bin/python3
import getopt
import sys


def usage():
    print('Use -h or --help to read this message')
    print('Use -r or --root= to set a root note for the scale')
    print('Use -n or --scale_note= to set a type of scale to return')


def main(argv):
    "here's where we handle system arguments in case people wish to use this"
    "module as a standalone cli tool"
    try:
        opts, args = getopt.getopt(argv, "hr:n:", ["help", "root=", "scale_name="])
        if opts is None:  # this  is not working
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
