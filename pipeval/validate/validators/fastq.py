'''Helper methods for FASTQ file validation'''
from pathlib import Path
from typing import Dict, Union
import gzip
import bz2
import magic

from pipeval.validate.validate_types import ValidateArgs

class FASTQ():
    def __init__(self, fastq_file:Path):
        '''Constructor'''
        self._fastq_path = fastq_file
        self._file_handler = self._get_file_handler()

    def _get_file_handler(self):
        '''Detect file format and set approriate handler'''
        _handler_map = {
            'application/x-gzip': gzip.open,
            'application/x-bzip2': bz2.open,
            'text/plain': open
        }

        file_mime = magic.from_file(self._fastq_path.resolve(), mime=True)

        handler = _handler_map.get(file_mime, None)

        if handler is None:
            raise TypeError(f'Unexpected FASTQ format {file_mime} for file: {self._fastq_path}')

        return handler

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
def _check_fastq(path:Path, args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    '''Validation for FASTQs'''
    _validate_sam_file(path)
