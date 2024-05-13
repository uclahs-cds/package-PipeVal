''' Console script main entrance '''
import argparse
from pipeval import __version__

from pipeval.validate.__main__ import add_subparser_validate
from pipeval.generate_checksum.__main__ import add_subparser_generate_checksum

def _parse_args():
    """ Parse arguments """
    parser = argparse.ArgumentParser(
        prog = 'pipeval'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers(dest = 'command')
    add_subparser_validate(subparsers)
    add_subparser_generate_checksum(subparsers)

    return parser.parse_args()

def main():
    ''' Main entrance '''
    args = _parse_args()
    args.func(args)

if __name__=='__main__':
    main()
