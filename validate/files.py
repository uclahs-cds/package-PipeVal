''' File checking functions '''
from pathlib import Path
import os
import warnings

def check_compressed(path:Path, file_extension:str):
    ''' Check file is compressed '''
    if not file_extension.endswith('.gz'):
        warnings.warn(f'Warning: file {path} is not zipped.')

def path_exists(path:Path):
    ''' Check if path exists '''
    if not path.exists():
        raise IOError('File or directory does not exist.')
