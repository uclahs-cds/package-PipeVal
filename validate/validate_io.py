# Main validation script

from pathlib import Path
import argparse
import hashlib
import os
import sys
import warnings

from validate.validators import bam
from validate.validators import vcf

# Currently supported data types
DIR_TYPES = ['directory-r', 'directory-rw']
FILE_TYPES_DICT = {'file-bam': ['.bam', '.cram', '.sam'], 'file-vcf': ['.vcf', '.vcf.gz'],
    'file-fasta': ['.fasta', '.fa'], 'file-fastq':['.fastq', '.fq.gz', '.fq', '.fastq.gz'], 'file-bed': ['.bed', '.bed.gz'], 'file-py': ['.py']}
GENERIC_FILE_TYPE = 'file-input' # file type needs to be detected
UNKNOWN_FILE_TYPE = 'file-unknown' # file type is unlisted
CHECKSUM_GEN_TYPES = ['md5-gen', 'sha512-gen']

# Main function and CLI tool
def validate_main():
    args = parse_args(sys.argv[1:])
    path = Path(args.path)
    input_type = args.type
    file_type = input_type

    try:
        path_exists(path)
    except IOError as e:
        sys.exit(f"Error: {args.path} {str(e)}")

    try:
        if input_type in FILE_TYPES_DICT:
            validate_file(path, input_type)
        elif input_type == GENERIC_FILE_TYPE:
            file_type = detect_file_type(path)
            validate_file(path, file_type)
        elif input_type in DIR_TYPES:
            validate_dir(path, input_type)
        elif input_type in CHECKSUM_GEN_TYPES:
            create_checksum_file(path, input_type)
    except TypeError as e:
        sys.exit(f"Error: {args.path} {str(e)}") # raise errors, has implicit exit code
    except ValueError as e:
        sys.exit(f"Error: {args.path} {str(e)}")
    except IOError as e:
        sys.exit(f"Error: {args.path} {str(e)}")
    except OSError as e:
        sys.exit(f"Error: {args.path} {str(e)}")

    print(f"Input: {args.path} is valid {file_type}")

# Argument parser
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of file to validate', type=str)
    parser.add_argument('-t', '--type', help='input data type',
        choices=['file-input', 'file-bam', 'file-vcf', 'file-fasta', 'file-fastq'
        'file-bed', 'file-py', 'directory-rw', 'directory-r', 'md5-gen', 'sha512-gen'], required=True)

    return parser.parse_args()

# File validation
def validate_file(path, file_type):
    file_extension = detect_file_ext(path)

    if file_type == UNKNOWN_FILE_TYPE: # no further specific validation for unlisted file types
        return True

    # TODO: Check handling of no-extension files
    if not file_extension:
        raise TypeError('File does not have a valid extension.')
    if not file_extension in FILE_TYPES_DICT.get(file_type):
        raise ValueError('File type does not match extension')

    # Checksum validation
    md5_file_path = path.with_suffix(file_extension + '.md5')
    if md5_file_path.exists():
        try:
            if not compare_hash('md5', path, md5_file_path):
                raise IOError('File is corrupted, md5 checksum failed.')
        except IOError:
            raise
        except OSError:
            raise

    sha512_file_path = path.with_suffix(file_extension + '.sha512')
    if sha512_file_path.exists():
        try:
            if not compare_hash('sha512', path, sha512_file_path):
                raise IOError('File is corrupted, sha512 checksum failed.')
        except IOError:
            raise
        except OSError:
            raise

    # File level validation
    if file_type == 'file-bam':
        try:
            bam.validate_bam_file(path)
        except ValueError:
            raise

    if file_type == 'file-vcf':
        try:
            vcf.validate_vcf_file(path)
        except ValueError:
            raise

    if file_type == 'file-fastq':
        if file_extension == '.fastq' or file_extension == '.fq':
            warnings.warn('Warning: fastq or fq file is not zipped')

    return True

# File type detection for generic 'file-input'
def detect_file_type(path):
    extension = detect_file_ext(path)

    for file_type in FILE_TYPES_DICT:
        if extension in FILE_TYPES_DICT.get(file_type):
            return file_type

    return UNKNOWN_FILE_TYPE

# Extracting complete file extension from path
def detect_file_ext(path):
    extensions = path.suffixes
    extension = ''.join(extensions)

    return extension

# Directory validation
def validate_dir(path, dir_type):
    try:
        path_readable(path)
        if dir_type == 'directory-rw':
            path_writable(path)
    except IOError:
        raise

    return True

# Path helper methods
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

# Checksum methods
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

def create_checksum_file(path, hash_type):
    size = len(hash_type)
    ext = "." + hash_type[:size-4]
    try:
        file = open(str(path) +  ext, "w")
        if hash_type == 'md5-gen':
            file.write(generate_md5(path))  
        elif hash_type == 'sha512-gen':
            file.write(generate_sha512(path))
        else:
            raise IOError('Incorrect hash parameters')
        file.close()
    except OSError:
        raise

    print(f"{hash_type}erated for {str(path)}")