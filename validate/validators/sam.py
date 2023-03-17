'''Helper methods for SAM file validation'''
from typing import Union
from pathlib import Path
import argparse
from typing import Dict, Union

import pysam

from validate.validate_types import ValidateArgs

def validate_sam_file(path:Path):
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
def check_sam(path:Path, args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    ''' Validation for SAMs 
    `args` must contains the following:
        `cram_reference` is a required key with either a string value or None
    '''
    validate_sam_file(path)
