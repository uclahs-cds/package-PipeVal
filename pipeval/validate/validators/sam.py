'''Helper methods for SAM file validation'''
from pathlib import Path
from typing import Dict, Union

import pysam

from pipeval.validate.validate_types import ValidateArgs

def _validate_sam_file(path:Path):
    '''Validates sam file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools sam check failed. " + str(err)) from err

    sam_head: pysam.IteratorRowHead = pysam.AlignmentFile(str(path)).head(1)
    if next(sam_head, None) is None:
        raise ValueError("pysam sam check failed. No reads in " + str(path))

    return True

# pylint: disable=W0613
def _check_sam(path:Path, args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    ''' Validation for SAMs
    `args` must contains the following:
        `cram_reference` is a required key with either a string value or None
    '''
    _validate_sam_file(path)
