''' File checking functions '''
from pathlib import Path
import warnings

def check_compressed(path:Path, file_extension:str):
    ''' Check file is compressed '''
    compression_extensions = ['.gz']
    if not any(file_extension.endswith(ext) for ext in compression_extensions):
        warnings.warn(f'Warning: file {path} is not compressed.')

def path_exists(path:Path):
    ''' Check if path exists '''
    if not path.exists():
        raise IOError('File or directory does not exist.')
