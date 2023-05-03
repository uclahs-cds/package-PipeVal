'''Helper methods for BAM file validation'''
from pathlib import Path
from typing import Dict, Union

import pysam

from validate.validate_types import ValidateArgs

def _validate_bam_file(path:Path):
    '''Validates bam file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools bam check failed. " + str(err)) from err

    bam_head: pysam.IteratorRowHead = pysam.AlignmentFile(str(path)).head(1)
    if next(bam_head, None) is None:
        raise ValueError("pysam bam check failed. No reads in " + str(path))

    return True

def _check_bam_index(path:Path):
    '''Checks if index file is present and can be opened'''
    try:
        pysam.AlignmentFile(str(path)).check_index()
    except ValueError as err:
        raise FileNotFoundError(f'pysam bam index check failed. Index file for {str(path)}'\
            'could not be opened or does not exist.') from err

    return True

# pylint: disable=W0613
def _check_bam(path:Path, args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    ''' Validation for BAMs
    `args` must contains the following:
        `cram_reference` is a required key with either a string value or None
    '''
    _validate_bam_file(path)
    _check_bam_index(path)
