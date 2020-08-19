from pathlib import Path
import argparse
import hashlib
import os
import sys

# currently supported data types
dir_types = ['directory-r', 'directory-rw']
file_types_dict = {'file-bam': ['.bam', '.cram', '.sam'], 'file-vcf': ['.vcf'],
    'file-fasta': ['.fasta', '.fastq'], 'file-bed': ['.bed'], 'file-py': ['.py']}

# main function and command line tool
def validate_main():
    args = parse_args(sys.argv[1:])
    path = Path(args.path)
    input_type = args.type

    try:
        path_exists(path)
    except IOError as e:
        sys.exit("Error: " + args.path + " " + str(e))

    try:
        if input_type in file_types_dict:
            validate_file(path, input_type)
        elif input_type in dir_types:
            validate_dir(path, input_type)
        else:
            path_readable(path) # TODO: expand case when no type is given
    except TypeError as e:
        sys.exit("Error: " + args.path + " " + str(e)) # raise errors, has implicit exit code
    except ValueError as e:
        sys.exit("Error: " + args.path + " " + str(e))
    except IOError as e:
        sys.exit("Error: " + args.path + " " + str(e))

    print("Input " + args.path + " is valid")
    sys.exit(0)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of file to validate', type=str)
    parser.add_argument('-t', '--type', help='input data type',
        choices=['file-input', 'file-bam', 'file-vcf', 'file-fasta',
        'file-bed', 'file-py', 'directory-rw', 'directory-r'])

    return parser.parse_args()

# type validation
def validate_file(path, file_type):
    file_extension = path.suffix

    # TODO: Fix handling of no-extension files
    if not file_extension:
        raise TypeError('File does not have a valid extension.')
    if not file_extension in file_types_dict.get(file_type):
        raise ValueError('File type does not match extension')

    # TODO: Add more detailed file validation
    return True

def validate_dir(path, dir_type):
    try:
        path_readable(path)
        if dir_type == 'directory-rw':
            path_writable(path)
    except IOError:
        raise

    return True

def path_exists(path):
    if path.exists():
        return True
    else:
        raise IOError('File or directory does not exist.')

def path_readable(path):
    if os.access(path, os.R_OK):
        return True
    else:
        raise IOError('File or directory is not readable.')

def path_writable(path):
    if os.access(path, os.W_OK):
        return True
    else:
        raise IOError('File or directory is not writable.')

# checksum methods
def generate_md5_for_file(path):
    md5_hash = hashlib.md5()

    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
    except OSError:
        raise

    return md5_hash.hexdigest() # returns string

def generate_sha512_for_file(path):
    sha512_hash = hashlib.sha512()

    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha512_hash.update(byte_block)
    except OSError:
        raise

    return sha512_hash.hexdigest() # returns string