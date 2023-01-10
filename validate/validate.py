''' File validation functions '''
from pathlib import Path
import sys

from validate.validators.bam import check_bam
from validate.validators.vcf import check_vcf
from validate.files import (
    check_compressed,
    path_exists,
    path_readable,
    path_writable
)
from generate_checksum.checksum import validate_checksums

# Currently supported data types
DIR_TYPES = ['directory-r', 'directory-rw']
FILE_TYPES_DICT = {'file-bam': ['.bam', '.cram', '.sam'], 'file-vcf': ['.vcf', '.vcf.gz'],
    'file-fasta': ['.fasta', '.fa'], 'file-fastq':['.fastq', '.fq.gz', '.fq', '.fastq.gz'],
    'file-bed': ['.bed', '.bed.gz'], 'file-py': ['.py']}
GENERIC_FILE_TYPE = 'file-input' # file type needs to be detected
UNKNOWN_FILE_TYPE = 'file-unknown' # file type is unlisted
CHECK_FUNCTION_SWITCH = {
    'file-bam': check_bam,
    'file-vcf': check_vcf
}
CHECK_COMPRESSION_TYPES = ['file-vcf', 'file-fastq', 'file-bed']

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
