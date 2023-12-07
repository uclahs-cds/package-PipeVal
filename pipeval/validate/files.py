''' File checking functions '''
from pathlib import Path
from typing import Union
import warnings
import zlib
import gzip
import bz2
import magic

def _identify_compression(path:Path):
    ''' Identify compression type and returns appropriate file handler '''
    compression_handlers = {
        'application/x-gzip': gzip.open,
        'application/x-bzip2': bz2.open
    }

    file_mime = magic.from_file(path.resolve(), mime=True)
    return compression_handlers.get(file_mime, None)

def _check_compression_integrity(path:Path, handler:Union[gzip.open,bz2.open]):
    ''' Verify integrity of compressed file '''
    integrity_error = ''
    read_chunk_size = 1000000 # 1 MB chunks

    with handler(path, 'rb') as file_reader:
        try:
            while file_reader.read(read_chunk_size) != b'':
                pass
        except gzip.BadGzipFile as bad_gzip:
            integrity_error = f'Invalid Gzip file: {bad_gzip}'
        except EOFError as eof_error:
            integrity_error = f'Truncated or corrupted file: {eof_error}'
        except zlib.error as zlib_error:
            integrity_error = f'Decompression error: {zlib_error}'

    if integrity_error != '':
        raise TypeError(f'Compression integrity check failed: {integrity_error}')

def _check_compressed(path:Path, test_integrity:bool):
    ''' Check file compression '''

    file_handler = _identify_compression(path)

    if file_handler is None:
        warnings.warn(f'Warning: file {path} is not compressed.')
        return

    if test_integrity:
        _check_compression_integrity(path, file_handler)

def _path_exists(path:Path):
    ''' Check if path exists '''
    if not path.exists():
        raise IOError('File or directory does not exist.')
