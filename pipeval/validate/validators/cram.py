'''Helper methods for CRAM file validation'''
from pathlib import Path
from typing import Dict, Union, Optional

import pysam

from pipeval.validate.validate_types import ValidateArgs

def _validate_cram_file(path:Path, reference:str=None):
    '''Validates cram file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools cram check failed. " + str(err)) from err

    if not reference:
        print(f'No reference specified for {str(path)}, ' \
            'pysam will automatically check CRAM header for reference URL')
        cram_head: pysam.IteratorRowHead = pysam.AlignmentFile(str(path)).head(1)
    else:
        cram_head: pysam.IteratorRowHead = pysam.AlignmentFile(
            str(path), reference_filename=reference).head(1)
    if next(cram_head, None) is None:
        raise ValueError("pysam cram check failed. No reads in " + str(path))

    return True

def _check_cram_index(path:Path):
    '''Checks if index file is present and can be opened'''
    try:
        pysam.AlignmentFile(str(path)).check_index()
    except ValueError as err:
        raise FileNotFoundError(f'pysam cram index check failed. Index file for {str(path)}'\
            'could not be opened or does not exist.') from err

    return True

def _check_cram(path:Path, args:Union[ValidateArgs,Dict[str, Optional[str]]]):
    ''' Validation for CRAMs
        `args` must contains the following:
        `cram_reference` is a required key with either a string value or None
    '''
    _validate_cram_file(path, args.cram_reference)
    _check_cram_index(path)
