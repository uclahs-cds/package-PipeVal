''' Console script main entrance '''
import argparse
from generate_checksum import __version__
from generate_checksum.checksum import generate_checksum

def _parse_args():
    """ Parse arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='one or more paths of files to validate', type=str, nargs='+')
    parser.add_argument('-t', '--type', help='Checksum type',
        choices=['md5', 'sha512'],
        default='sha512')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    parser.set_defaults(func=generate_checksum)

    return parser.parse_args()

def main():
    ''' Main entrance '''
    args = _parse_args()
    args.func(args)

if __name__=='__main__':
    main()
