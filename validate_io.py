from pathlib import Path
from supported import dir_types
from supported import file_types_dict
import argparse
import os
import sys

# main function and command line tool
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of file to validate', type=str)
    parser.add_argument('-t', '--type', help='input data type',
        choices=['file-input', 'file-bam', 'file-vcf', 'file-fasta',
        'file-bed', 'file-py', 'directory-rw', 'directory-r'])

    args = parser.parse_args()
    path = Path(args.path)
    input_type = args.type

    try:
        path_exists(path)
    except IOError as e:
        parser.exit(1, "Error: " + args.path + " " + str(e))

    try:
        if input_type in file_types_dict:
            validate_file(path, input_type)
        elif input_type in dir_types:
            validate_dir(path, input_type)
        else:
            path_readable(path)
    except TypeError as e:
        parser.exit(1, "Error: " + args.path + " " + str(e))
    except ValueError as e:
        parser.exit(1, "Error: " + args.path + " " + str(e))
    except IOError as e:
        parser.exit(1, "Error: " + args.path + " " + str(e))

    print("Input " + args.path + " is valid")
    sys.exit(0)

# type validation
def validate_file(path, file_type):
    file_extension = path.suffix

    if not file_extension:
        raise TypeError('File does not have a valid extension.')

    if not file_extension in file_types_dict.get(file_type):
        raise ValueError('File type does not match extension')

    # TODO: Add type specific validation
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

if __name__ == '__main__':
    main()