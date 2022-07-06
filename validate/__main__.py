'''Main validation script'''

from pathlib import Path
import argparse
import hashlib
import os
import sys
import warnings

from validate.validators import bam
from validate.validators import vcf
from validate import __version__

# Currently supported data types
DIR_TYPES = ['directory-r', 'directory-rw']
FILE_TYPES_DICT = {'file-bam': ['.bam', '.cram', '.sam'], 'file-vcf': ['.vcf', '.vcf.gz'],
    'file-fasta': ['.fasta', '.fa'], 'file-fastq':['.fastq', '.fq.gz', '.fq', '.fastq.gz'],
    'file-bed': ['.bed', '.bed.gz'], 'file-py': ['.py']}
GENERIC_FILE_TYPE = 'file-input' # file type needs to be detected
UNKNOWN_FILE_TYPE = 'file-unknown' # file type is unlisted
CHECKSUM_GEN_TYPES = ['md5-gen', 'sha512-gen']

# Main function and CLI tool
def main():
    '''Main function and CLI tool'''
    args = parse_args(sys.argv[1:])
    input_type = args.type
    file_type = input_type
    err_flag = False

    for path in [Path(pathname) for pathname in args.path]:
        try:
            path_exists(path)
        except IOError as err:
            err_flag = True
            print_error(path, err)# sys.exit(f"Error: {str(path)} {str(err)}") 
            continue

        try:
            if input_type in FILE_TYPES_DICT:
                validate_file(path, input_type)
            elif input_type == GENERIC_FILE_TYPE:
                file_type, _ = detect_file_type_and_ext(path)
                validate_file(path, file_type)
            elif input_type in DIR_TYPES:
                validate_dir(path, input_type)
            elif input_type in CHECKSUM_GEN_TYPES:
                create_checksum_file(path, input_type)
        except (TypeError, ValueError, IOError, OSError) as err:
            err_flag = True
            print_error(path, err) # sys.exit(f"Error: {path} {str(err)}") # raise errors, has implicit exit code
            continue

        print_success(path, file_type)
    
    if err_flag:
        sys.exit(1)

# Argument parser
def parse_args(args):
    '''Argument parser'''
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path of file to validate', type=str, nargs='+')
    parser.add_argument('-t', '--type', help='input data type',
        choices=['file-input', 'file-bam', 'file-vcf', 'file-fasta', 'file-fastq',
        'file-bed', 'file-py', 'directory-rw', 'directory-r', 'md5-gen', 'sha512-gen'],
        required=True)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    return parser.parse_args(args)

# File validation
def validate_file(path, file_type):
    '''File validation'''
    if file_type == UNKNOWN_FILE_TYPE: # no further specific validation for unlisted file types
        return True

    _, file_extension = detect_file_type_and_ext(path)

    if not file_extension:
        raise TypeError('File does not have a valid extension.')
    if not file_extension in FILE_TYPES_DICT.get(file_type):
        raise ValueError('File type does not match extension')

    # Checksum validation
    md5_file_path = path.with_suffix(path.suffix + '.md5')
    if md5_file_path.exists():
        if not compare_hash('md5', path, md5_file_path):
            raise IOError('File is corrupted, md5 checksum failed.')

    sha512_file_path = path.with_suffix(path.suffix + '.sha512')
    if sha512_file_path.exists():
        if not compare_hash('sha512', path, sha512_file_path):
            raise IOError('File is corrupted, sha512 checksum failed.')


    # File level validation
    def bam_case():
        bam.validate_bam_file(path)

    def vcf_case():
        vcf.validate_vcf_file(path)

    def fastq_case():
        if file_extension in ('.fastq', '.fq'):
            warnings.warn('Warning: fastq or fq file is not zipped')

    file_type_switcher ={
        'file-bam': bam_case,
        'file-vcf': vcf_case,
        'file-fastq': fastq_case
    }

    file_type_switcher[file_type]()

    return True

# File type and extension detection for generic 'file-input'
def detect_file_type_and_ext(path):
    '''File type and extension detection for generic file-input'''
    # Starting from the end, build up extension with each '.' separated part and try matching
    # resulting extension
    full_extension = ''
    for suffix in path.suffixes[::-1]:
        full_extension = suffix + full_extension
        extension_type = detect_file_type(full_extension)

        if extension_type != UNKNOWN_FILE_TYPE:
            return extension_type, full_extension

    # No matching extension found so return unknown type and full extension
    return UNKNOWN_FILE_TYPE, full_extension

# File type detection for generic 'file-input'
def detect_file_type(extension):
    '''File type detection for generic file-input'''
    for file_type in FILE_TYPES_DICT:
        if extension in FILE_TYPES_DICT.get(file_type):
            return file_type

    return UNKNOWN_FILE_TYPE

# Directory validation
def validate_dir(path, dir_type):
    '''Directory validation'''
    path_readable(path)
    if dir_type == 'directory-rw':
        path_writable(path)

    return True

# Path helper methods
def path_exists(path):
    '''Checks if path exists'''
    if path.exists():
        return True
    raise IOError('File or directory does not exist.')

def path_readable(path):
    '''Checks if path is readable'''
    if os.access(path, os.R_OK):
        return True
    raise IOError('File or directory is not readable.')

def path_writable(path):
    '''Checks if path is writable'''
    if os.access(path, os.W_OK):
        return True
    raise IOError('File or directory is not writable.')

# Checksum methods
def compare_hash(hash_type, path, hash_path):
    '''Compares existing hash to generated hash'''
    # Read only the hash and not the filename for comparison
    existing_hash = hash_path.read_text().split(' ')[0].strip()

    if hash_type == 'md5':
        return existing_hash == generate_md5(path)
    if hash_type == 'sha512':
        return existing_hash == generate_sha512(path)
    raise IOError('Incorrect hash parameters')

def generate_md5(path):
    '''Generates md5 hash'''
    md5_hash = hashlib.md5()

    with open(path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest() # returns string

def generate_sha512(path):
    '''Generates sah512 hash'''
    sha512_hash = hashlib.sha512()

    with open(path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha512_hash.update(byte_block)

    return sha512_hash.hexdigest() # returns string

def create_checksum_file(path, hash_type):
    '''Creates checksum'''
    size = len(hash_type)
    ext = "." + hash_type[:size-4]
    with open(str(path) +  ext, "w") as file:
        if hash_type == 'md5-gen':
            file.write(generate_md5(path)+'  '+str(path)+'\n')
        elif hash_type == 'sha512-gen':
            file.write(generate_sha512(path)+'  '+str(path)+'\n')
        else:
            raise IOError('Incorrect hash parameters')
        file.close()

    print(f"{hash_type}erated for {str(path)}")

# Exception Handling
def print_error(path, err):
    print(f"Error: {str(path)} {str(err)}")

def print_success(path, file_type):
    print(f"Input: {path} is valid {file_type}")
