from pathlib import Path
import sys
import os
import hashlib
import warnings

from validate.validators.bam import check_bam
from validate.validators.vcf import check_vcf

# Currently supported data types
DIR_TYPES = ['directory-r', 'directory-rw']
FILE_TYPES_DICT = {'file-bam': ['.bam', '.cram', '.sam'], 'file-vcf': ['.vcf', '.vcf.gz'],
    'file-fasta': ['.fasta', '.fa'], 'file-fastq':['.fastq', '.fq.gz', '.fq', '.fastq.gz'],
    'file-bed': ['.bed', '.bed.gz'], 'file-py': ['.py']}
GENERIC_FILE_TYPE = 'file-input' # file type needs to be detected
UNKNOWN_FILE_TYPE = 'file-unknown' # file type is unlisted
CHECKSUM_GEN_TYPES = ['md5-gen', 'sha512-gen']
CHECK_FUNCTION_SWITCH = {
    'file-bam': check_bam,
    'file-vcf': check_vcf
}
CHECK_COMPRESSION_TYPES = ['file-vcf', 'file-fastq', 'file-bed']

def check_compressed(path:Path, file_extension:str):
    ''' Check file is compressed '''
    if not file_extension.endswith('.gz'):
        warnings.warn(f'Warning: file {path} is not zipped.')

def path_exists(path:Path):
    ''' Check if path exists '''
    if not path.exists():
        raise IOError('File or directory does not exist.')

def path_readable(path:Path):
    '''Checks if path is readable'''
    if os.access(path, os.R_OK):
        return True
    raise IOError('File or directory is not readable.')

def path_writable(path:Path):
    '''Checks if path is writable'''
    if os.access(path, os.W_OK):
        return True
    raise IOError('File or directory is not writable.')

def validate_file(path:Path, file_type:str):
    ''' Validate a single file '''
    path_exists(path)

    detected_file_type, file_extension = detect_file_type_and_extension(path)
    if not file_extension:
        raise TypeError(f'File {path} does not have a valid extension.')
    if (detected_file_type != UNKNOWN_FILE_TYPE and 
        file_type != GENERIC_FILE_TYPE and
        detected_file_type != file_type):
        raise ValueError(f'Indicated and detected file types do not match. '\
            f'Indicated: {file_type}, detected: {detected_file_type}'
        )

    if detected_file_type in CHECK_COMPRESSION_TYPES:
        check_compressed(path, file_extension)

    validate_checksums(path)

    CHECK_FUNCTION_SWITCH.get(detected_file_type, lambda p: None)(path)

def validate_dir(path:Path, dir_type:str):
    ''' Validate directory '''
    path_readable(path)
    if dir_type == 'directory-rw':
        path_writable(path)

def validate_checksums(path:Path):
    ''' Validate MD5 and/or SHA512 checksums '''
    # Checksum validation
    md5_file_path = path.with_suffix(path.suffix + '.md5')
    if md5_file_path.exists():
        if not compare_hash('md5', path, md5_file_path):
            raise IOError('File is corrupted, md5 checksum failed.')

    sha512_file_path = path.with_suffix(path.suffix + '.sha512')
    if sha512_file_path.exists():
        if not compare_hash('sha512', path, sha512_file_path):
            raise IOError('File is corrupted, sha512 checksum failed.')

def compare_hash(hash_type:str, path:Path, hash_path:Path):
    ''' Compares existing hash to generated hash '''
    # Read only the hash and not the filename for comparison
    existing_hash = hash_path.read_text().split(' ')[0].strip()

    if hash_type == 'md5':
        return existing_hash == generate_md5(path)
    if hash_type == 'sha512':
        return existing_hash == generate_sha512(path)
    raise IOError('Incorrect hash parameters')

def generate_md5(path:Path):
    ''' Generates md5 hash '''
    md5_hash = hashlib.md5()

    with open(path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest() # returns string

def generate_sha512(path:Path):
    ''' Generates sah512 hash '''
    sha512_hash = hashlib.sha512()

    with open(path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha512_hash.update(byte_block)

    return sha512_hash.hexdigest() # returns string

def print_error(path:Path, err:BaseException):
    ''' Prints error message '''
    print(f'Error: {str(path)} {str(err)}')

def print_success(path:Path, file_type:str):
    ''' Prints success message '''
    print(f'Input: {path} is valid {file_type}')

def detect_file_type_and_extension(path:Path):
    ''' File type and extension detection '''
    # Starting from the end, build up extension with each '.' separated part and try matching
    # resulting extension
    full_extension = ''
    for suffix in path.suffixes[::-1]:
        full_extension = suffix + full_extension
        extension_type = check_extension(full_extension)

        if extension_type != UNKNOWN_FILE_TYPE:
            return extension_type, full_extension

    # No matching extension found so return unknown type and full extension
    return UNKNOWN_FILE_TYPE, full_extension

def check_extension(extension:str):
    ''' Check for matching file type for extension '''
    for file_type in FILE_TYPES_DICT:
        if extension in FILE_TYPES_DICT.get(file_type):
            return file_type

    return UNKNOWN_FILE_TYPE

def run_validate(args):
    ''' Function to validate file(s) '''

    all_files_pass = True

    validation_function = validate_file
    if args.type in DIR_TYPES:
        validation_function = validate_dir

    for path in [Path(pathname) for pathname in args.path]:
        try:
            validation_function(path, args.type)
        except FileNotFoundError as file_not_found_err:
            print(f"Warning: {str(path)} {str(file_not_found_err)}")
        except (TypeError, ValueError, IOError, OSError) as err:
            all_files_pass = False
            print_error(path, err)
            continue

        print_success(path, args.type)

    if not all_files_pass:
        sys.exit(1)
