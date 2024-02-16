''' Checksum generation and validation functions '''
import hashlib
import sys
from collections import namedtuple
from typing import Dict, Union
from pathlib import Path

from pipeval.common import skippedValidation

ChecksumArgs = namedtuple(
    'args',
    'path, type'
)

@skippedValidation('CHECKSUM')
def _validate_checksums(path:Path):
    ''' Validate MD5 and/or SHA512 checksums '''
    # Checksum validation
    md5_file_path = path.with_suffix(path.suffix + '.md5')
    if md5_file_path.exists():
        if not _compare_hash('md5', path, md5_file_path):
            raise IOError('File is corrupted, md5 checksum failed.')

    sha512_file_path = path.with_suffix(path.suffix + '.sha512')
    if sha512_file_path.exists():
        if not _compare_hash('sha512', path, sha512_file_path):
            raise IOError('File is corrupted, sha512 checksum failed.')

def _compare_hash(hash_type:str, path:Path, hash_path:Path):
    ''' Compares existing hash to generated hash '''
    # Read only the hash and not the filename for comparison
    existing_hash = hash_path.read_text().split(' ')[0].strip()

    if hash_type == 'md5':
        return existing_hash == _generate_md5(path)
    if hash_type == 'sha512':
        return existing_hash == _generate_sha512(path)
    raise IOError('Incorrect hash parameters')

def _generate_md5(path:Path):
    ''' Generates md5 hash '''
    md5_hash = hashlib.md5()

    with open(path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest() # returns string

def _generate_sha512(path:Path):
    ''' Generates sah512 hash '''
    sha512_hash = hashlib.sha512()

    with open(path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha512_hash.update(byte_block)

    return sha512_hash.hexdigest() # returns string

def _write_checksum_file(path:Path, hash_type:str, computed_hash:str):
    ''' Write checksum to file '''
    with open(str(path) + '.' + hash_type, 'w', encoding="utf-8") as checksum_file:
        checksum_file.write(computed_hash + '  ' + str(path) + '\n')

    print(f'{hash_type} checksum generated for {str(path)}')

def generate_checksum(args:Union[ChecksumArgs,Dict[str, Union[str,list]]]):
    ''' Function to generate checksum(s)
        `args` must contain the following:
        `path` is a required argument with a value of list of files
        `type` is a required argument with a value of string indicating type of checksum
    '''

    checksum_gen_functions = {
        'md5': _generate_md5,
        'sha512': _generate_sha512
    }

    all_checksums_generated = True

    for path in [Path(pathname) for pathname in args.path]:
        try:
            checksum = checksum_gen_functions[args.type](path)
            _write_checksum_file(path, args.type, checksum)
        except KeyError as key_err:
            all_checksums_generated = False
            print(f'Invalid checksum type. {str(key_err)}')
        except (IOError, PermissionError, OSError, FileNotFoundError) as err:
            all_checksums_generated = False
            print(f'Failed to write checksum for {str(path)}: {str(err)}')

    if not all_checksums_generated:
        sys.exit(1)
