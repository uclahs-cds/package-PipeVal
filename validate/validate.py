''' File validation functions '''
from pathlib import Path
import sys
import os
from typing import Dict, Union
import multiprocessing
from itertools import repeat

from validate.validators.bam import _check_bam
from validate.validators.sam import _check_sam
from validate.validators.cram import _check_cram
from validate.validators.vcf import _check_vcf
from validate.files import (
    _check_compressed,
    _path_exists
)
from validate.validate_types import ValidateArgs
from generate_checksum.checksum import _validate_checksums

# Currently supported data types
FILE_TYPES_DICT = {
    'file-bam': ['.bam'],
    'file-sam': ['.sam'],
    'file-cram': ['.cram'],
    'file-vcf': ['.vcf', '.vcf.gz'],
    'file-fasta': ['.fasta', '.fa'],
    'file-fastq':['.fastq', '.fq.gz', '.fq', '.fastq.gz'],
    'file-bed': ['.bed', '.bed.gz'],
    'file-py': ['.py']
    }
UNKNOWN_FILE_TYPE = 'file-unknown' # file type is unlisted
CHECK_FUNCTION_SWITCH = {
    'file-bam': _check_bam,
    'file-sam': _check_sam,
    'file-cram': _check_cram,
    'file-vcf': _check_vcf
}
CHECK_COMPRESSION_TYPES = ['file-vcf', 'file-fastq', 'file-bed']

def _validate_file(
    path:Path, file_type:str,
    file_extension:str,
    args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    ''' Validate a single file
        `args` must contain the following:
        `path` is a required argument with a value of list of files
        `cram_reference` is a required argument with either a string value or None
    '''
    _path_exists(path)

    if not file_extension:
        raise TypeError(f'File {path} does not have a valid extension.')

    if file_type in CHECK_COMPRESSION_TYPES:
        _check_compressed(path)

    _validate_checksums(path)

    CHECK_FUNCTION_SWITCH.get(file_type, lambda p, a: None)(path, args)

def _print_error(path:Path, err:BaseException):
    ''' Prints error message '''
    print(f'PID:{os.getpid()} - Error: {str(path)} {str(err)}')

def _print_success(path:Path, file_type:str):
    ''' Prints success message '''
    print(f'PID:{os.getpid()} - Input: {path} is valid {file_type}')

def _detect_file_type_and_extension(path:Path):
    ''' File type and extension detection '''
    # Starting from the end, build up extension with each '.' separated part and try matching
    # resulting extension
    full_extension = ''
    for suffix in path.suffixes[::-1]:
        full_extension = suffix.lower() + full_extension
        extension_type = _check_extension(full_extension)

        if extension_type != UNKNOWN_FILE_TYPE:
            return extension_type, full_extension

    # No matching extension found so return unknown type and full extension
    return UNKNOWN_FILE_TYPE, full_extension

def _check_extension(extension:str):
    ''' Check for matching file type for extension '''
    for file_type in FILE_TYPES_DICT:
        if extension in FILE_TYPES_DICT.get(file_type):
            return file_type

    return UNKNOWN_FILE_TYPE

def _validation_worker(path: Path, args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    ''' Worker function to validate a single file '''
    try:
        file_type, file_extension = _detect_file_type_and_extension(path)
        _validate_file(path, file_type, file_extension, args)
    except FileNotFoundError as file_not_found_err:
        print(f"Warning: {str(path)} {str(file_not_found_err)}")
    except (TypeError, ValueError, IOError, OSError) as err:
        _print_error(path, err)
        return False

    _print_success(path, file_type)
    return True

def run_validate(args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    ''' Function to validate file(s)
        `args` must contain the following:
        `path` is a required argument with a value of list of files
        `cram_reference` is a required argument with either a string value or None
    '''

    num_parallel = min(args.processes, multiprocessing.cpu_count())

    with multiprocessing.Pool(num_parallel) as parallel_pool:
        validation_results = parallel_pool.starmap(_validation_worker, \
            zip([Path(pathname).resolve(strict=True) for pathname in args.path], repeat(args)))

    if not all(validation_results):
        sys.exit(1)
