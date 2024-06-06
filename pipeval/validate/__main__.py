''' Console script main entrance '''
import argparse
from pipeval.validate.validate import run_validate

def positive_integer(arg):
    """ Type and value check for positive integers """
    try:
        i = int(arg)
    except ValueError as value_exception:
        raise argparse.ArgumentTypeError("Must be an integer.") from value_exception

    if i < 1:
        raise argparse.ArgumentTypeError("Must be an integer greater than 0.")

    return i

def add_subparser_validate(subparsers:argparse._SubParsersAction):
    """ Parse arguments """
    parser:argparse.ArgumentParser = subparsers.add_parser(
        name = 'validate',
        help = 'Validate one or more file(s)',
        description = 'Validate one or more file(s)',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('path', help='One or more paths of files to validate', type=str, nargs='+')
    parser.add_argument('-r', '--cram-reference', default=None, \
        help='Path to reference file for CRAM')
    parser.add_argument('-u', '--unmapped-bam', action='store_true',
        help='Input is unmmapped BAM.')
    parser.add_argument('-p', '--processes', type=positive_integer, default=1, \
        help='Number of processes to run in parallel when validating multiple files')
    parser.add_argument('-t', '--test-integrity', action='store_true', \
        help='Whether to perform a full integrity test on compressed files')

    parser.set_defaults(func=run_validate)
