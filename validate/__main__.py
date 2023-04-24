''' Console script main entrance '''
import argparse
from validate import __version__
from validate.validate import run_validate

def _parse_args():
    """ Parse arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='one or more paths of files to validate', type=str, nargs='+')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-r', '--cram-reference', default=None, \
        help='Path to reference file for CRAM')

    parser.set_defaults(func=run_validate)

    return parser.parse_args()

def main():
    ''' Main entrance '''
    args = _parse_args()
    args.func(args)

if __name__=='__main__':
    main()
