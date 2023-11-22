''' Console script main entrance '''
import argparse
from pipeval.generate_checksum.checksum import generate_checksum

def add_subparser_generate_checksum(subparsers:argparse._SubParsersAction):
    """ Parse arguments """
    parser = subparsers.add_parser(
        name = 'generate_checksum',
        help = 'Generate checksums for one or more file(s)',
        description = 'Generate checksums for one or more file(s)',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('path', help='one or more paths of files to validate', type=str, nargs='+')
    parser.add_argument('-t', '--type', help='Checksum type',
        choices=['md5', 'sha512'],
        default='sha512')

    parser.set_defaults(func=generate_checksum)
