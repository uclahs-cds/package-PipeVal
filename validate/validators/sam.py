'''Helper methods for SAM file validation'''
from typing import Union
from pathlib import Path
import argparse

import pysam

def validate_sam_file(path):
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
def check_sam(path:Path, args:Union[argparse.Namespace,None]):
    ''' Validation for SAMs '''
    validate_sam_file(path)
