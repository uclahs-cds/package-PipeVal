''' File checking functions '''
from pathlib import Path
import warnings
import magic

def _check_compressed(path:Path):
    ''' Check file is compressed '''
    compression_mimes = [
        'application/x-gzip',
        'application/x-bzip2'
    ]
    if magic.from_file(path.resolve(), mime=True) not in compression_mimes:
        warnings.warn(f'Warning: file {path} is not compressed.')

def _path_exists(path:Path):
    ''' Check if path exists '''
    if not path.exists():
        raise IOError('File or directory does not exist.')
