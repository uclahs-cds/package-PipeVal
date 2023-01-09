''' Console script main entrance '''
import argparse
import sys
from validate import __version__

def validate(args):
    print(args)

def parse_args():
    """ Parse arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='one or more paths of files to validate', type=str, nargs='+')
    parser.add_argument('-t', '--type', help='input data type',
        choices=['file-input', 'file-bam', 'file-vcf', 'file-fasta', 'file-fastq',
        'file-bed', 'file-py', 'directory-rw', 'directory-r', 'md5-gen', 'sha512-gen'],
        default='file-input')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    parser.set_defaults(func=validate)

    return parser.parse_args()

def main():
    ''' Main entrance '''
    args = parse_args()
    args.func(args)

if __name__=='__main__':
    main()
