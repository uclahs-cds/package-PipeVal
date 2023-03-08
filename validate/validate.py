''' File validation functions '''
from pathlib import Path
import sys

from validate.validators.bam import check_bam
from validate.validators.sam import check_sam
from validate.validators.vcf import check_vcf
from validate.files import (
    check_compressed,
    path_exists
)
from generate_checksum.checksum import validate_checksums

# Currently supported data types
FILE_TYPES_DICT = {
    'file-bam': ['.bam', '.cram'],
    'file-sam': ['.sam'],
    'file-vcf': ['.vcf', '.vcf.gz'],
    'file-fasta': ['.fasta', '.fa'],
    'file-fastq':['.fastq', '.fq.gz', '.fq', '.fastq.gz'],
    'file-bed': ['.bed', '.bed.gz'],
    'file-py': ['.py']
    }
UNKNOWN_FILE_TYPE = 'file-unknown' # file type is unlisted
CHECK_FUNCTION_SWITCH = {
    'file-bam': check_bam,
    'file-sam': check_sam,
    'file-vcf': check_vcf
}
CHECK_COMPRESSION_TYPES = ['file-vcf', 'file-fastq', 'file-bed']

def validate_file(path:Path, file_type:str, file_extension:str):
    ''' Validate a single file '''
    path_exists(path)

    if not file_extension:
        raise TypeError(f'File {path} does not have a valid extension.')

    if file_type in CHECK_COMPRESSION_TYPES:
        check_compressed(path, file_extension)

    validate_checksums(path)

    CHECK_FUNCTION_SWITCH.get(file_type, lambda p: None)(path)

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
        full_extension = suffix.lower() + full_extension
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

    for path in [Path(pathname) for pathname in args.path]:
        try:
            file_type, file_extension = detect_file_type_and_extension(path)
            validate_file(path, file_type, file_extension)
        except FileNotFoundError as file_not_found_err:
            print(f"Warning: {str(path)} {str(file_not_found_err)}")
        except (TypeError, ValueError, IOError, OSError) as err:
            all_files_pass = False
            print_error(path, err)
            continue

        print_success(path, file_type)

    if not all_files_pass:
        sys.exit(1)
