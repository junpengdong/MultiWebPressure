from lib import ClearImage
import sys
import getopt

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "t:d:", ['-t', '--type', '-d', '--day'])
    c_type = 'all'
    day = 7
    if sys.argv[1] in ('-t', '--type', '-d', '--day'):
        for opt, arg in opts:
            if opt in ('-t', '--type'):
                c_type = arg
            if opt in ('-d', '--day'):
                day = int(arg)
    clear_image = ClearImage()
    clear_image.do_clear(c_type, day)
