from pathlib import Path
import argparse
import hashlib
import os
import sys

# currently supported data types
dir_types = ['directory-r', 'directory-rw']
file_types_dict = {'file-bam': ['.bam', '.cram', '.sam'], 'file-vcf': ['.vcf'],
    'file-fasta': ['.fasta', '.fastq'], 'file-bed': ['.bed'], 'file-py': ['.py']}
generic_input_type = 'file-input'

# main function and command line tool
def validate_main():
    args = parse_args(sys.argv[1:])
    path = Path(args.path)
    input_type = args.type
    file_type = input_type

    try:
        path_exists(path)
    except IOError as e:
        sys.exit("Error: " + args.path + " " + str(e))

    try:
        if input_type in file_types_dict:
            validate_file(path, input_type)
        elif input_type == generic_input_type:
            file_type = detect_file_type(path)
            validate_file(path, file_type)
        elif input_type in dir_types:
            validate_dir(path, input_type)
    except TypeError as e:
        sys.exit("Error: " + args.path + " " + str(e)) # raise errors, has implicit exit code
    except ValueError as e:
        sys.exit("Error: " + args.path + " " + str(e))
    except IOError as e:
        sys.exit("Error: " + args.path + " " + str(e))
    except OSError as e:
        sys.exit("Error: " + args.path + " " + str(e))

    print("Input " + args.path + " is a valid " + file_type)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of file to validate', type=str)
    parser.add_argument('-t', '--type', help='input data type',
        choices=['file-input', 'file-bam', 'file-vcf', 'file-fasta',
        'file-bed', 'file-py', 'directory-rw', 'directory-r'])

    return parser.parse_args()

# file validation
def validate_file(path, file_type):
    file_extension = path.suffix

    # TODO: Check handling of no-extension files
    if not file_extension:
        raise TypeError('File does not have a valid extension.')
    if not file_extension in file_types_dict.get(file_type):
        raise ValueError('File type does not match extension')

    # Check hashes
    md5_file_path = path.with_suffix(path.suffix + '.md5')
    if md5_file_path.exists():
        try:
            if not compare_hash('md5', path, md5_file_path):
                raise IOError('File is corrupted, md5 checksum failed.')
        except IOError:
            raise
        except OSError:
            raise

    sha512_file_path = path.with_suffix(path.suffix + '.sha512')
    if sha512_file_path.exists():
        try:
            if not compare_hash('sha512', path, sha512_file_path):
                raise IOError('File is corrupted, sha512 checksum failed.')
        except IOError:
            raise
        except OSError:
            raise

    # TODO: Add file level validation

    return True

# detect file type for generic 'file-input'
def detect_file_type(path):
    extension = path.suffix

    for file_type in file_types_dict:
        if extension in file_types_dict.get(file_type):
            return file_type

    return ""
    # TODO: raise error if file-type not found

# directory validation
def validate_dir(path, dir_type):
    try:
        path_readable(path)
        if dir_type == 'directory-rw':
            path_writable(path)
    except IOError:
        raise

    return True

# path methods
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
def compare_hash(hash_type, path, hash_path):
    existing_hash = hash_path.read_text().strip()

    if hash_type == 'md5':
        return existing_hash == generate_md5(path)
    if hash_type == 'sha512':
        return existing_hash == generate_sha512(path)
    else:
        raise IOError('Incorrect hash parameters')

def generate_md5(path):
    md5_hash = hashlib.md5()

    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
    except OSError:
        raise

    return md5_hash.hexdigest() # returns string

def generate_sha512(path):
    sha512_hash = hashlib.sha512()

    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha512_hash.update(byte_block)
    except OSError:
        raise

    return sha512_hash.hexdigest() # returns string

# specific type validation
def validate_bam_file(path):
    # TODO: decide what type validation
    return True

def validate_vcf_file(path):
    # TODO: decide what type validation
    return True