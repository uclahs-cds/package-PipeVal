# pylint: disable=C0103
'''Helper methods for FASTQ file validation'''
from pathlib import Path
from typing import Dict, Union, ClassVar
from dataclasses import dataclass
import re
import gzip
import bz2
import magic

from pipeval.validate.validate_types import ValidateArgs

RECORD_LENGTH = 4

@dataclass
class FASTQ_RECORD:
    ''' FASTQ Record class '''
    identifier: str = ''
    sequence: str = ''
    extra_field: str = ''
    quality: str = ''

@dataclass
class FASTQ_RECORD_VALIDATOR:
    ''' FASTQ Record validator class '''
    minimum_quality_ordinal: ClassVar[int] = 33
    maximum_quality_ordinal: ClassVar[int] = 126
    record_identifier_format: ClassVar[re.Pattern] = re.compile('^@')
    extra_field_format: ClassVar[re.Pattern] = re.compile(r'^\+')
    sequence_format: ClassVar[re.Pattern] = re.compile('^[ACTGNactgn]+$')

    @staticmethod
    def validate_record(record:FASTQ_RECORD):
        '''Validate the given FASTQ read record'''
        invalid_entries = []

        if not FASTQ_RECORD_VALIDATOR.record_identifier_format.match(record.identifier):
            invalid_entries.append(
                f'Record identifier `{record.identifier}` is invalid. It must begin with \'@\''
            )

        if not FASTQ_RECORD_VALIDATOR.sequence_format.match(record.sequence):
            invalid_entries.append(
                f'Read sequence `{record.sequence}` contains invalid characters. '
                'Only \'ACTGNactgn\' are allowed'
            )

        if not FASTQ_RECORD_VALIDATOR.extra_field_format.match(record.extra_field):
            invalid_entries.append(
                f'Extra field `{record.extra_field}` is invalid. It must begin with \'+\''
            )

        if len(record.sequence) != len(record.quality):
            invalid_entries.append(
                f'Sequence and quality must be of the same length:\n'
                f'Sequence - {len(record.sequence)} - {record.sequence}\n'
                f'Quality - {len(record.quality)} - {record.quality}'
            )

        min_quality = min(record.quality)
        max_quality = max(record.quality)

        if ord(min_quality) < FASTQ_RECORD_VALIDATOR.minimum_quality_ordinal or \
            ord(max_quality) > FASTQ_RECORD_VALIDATOR.maximum_quality_ordinal:
            invalid_entries.append(
                f'Quality scores out of valid range. Quality scores must fall between '
                f'{FASTQ_RECORD_VALIDATOR.minimum_quality_ordinal} and '
                f'{FASTQ_RECORD_VALIDATOR.maximum_quality_ordinal}. '
                f'Found min:`{min_quality}` ({ord(min_quality)}) and '
                f'max:`{max_quality}` ({ord(max_quality)}) in record.'
            )

        if len(invalid_entries) != 0:
            record_errors = '\n'.join(invalid_entries)
            raise ValueError(f'Record {record} is invalid: {record_errors}')

# pylint: disable=R0903
class FASTQ():
    ''' FASTQ file handling and validation class '''
    def __init__(self, fastq_file:Path):
        '''Constructor'''
        self._fastq_path = fastq_file
        self._file_handler = self._get_file_handler()

    def _get_file_handler(self):
        '''Detect file format and return approriate handler to read file'''
        _handler_map = {
            'application/x-gzip': gzip.open,
#            'application/gzip': gzip.open,
            'application/x-bzip2': bz2.open,
            'text/plain': open
        }

        file_mime = magic.from_file(self._fastq_path.resolve(), mime=True)

        handler = _handler_map.get(file_mime, None)

        if handler is None:
            raise TypeError(f'Unexpected FASTQ format `{file_mime}` for file: `{self._fastq_path}`')

        return handler

    def validate_fastq(self):
        ''' Validate the FASTQ file '''
        with self._file_handler(self._fastq_path, 'rt') as rd:
            current_record = []
            current_record_length = 0
            for line in rd:
                current_record.append(line.strip())
                current_record_length = current_record_length + 1

                if current_record_length == RECORD_LENGTH:
                    record = FASTQ_RECORD(
                        identifier = current_record[0],
                        sequence = current_record[1],
                        extra_field = current_record[2],
                        quality = current_record[3]
                    )
                    FASTQ_RECORD_VALIDATOR.validate_record(record)
                    current_record = []
                    current_record_length = 0

        if current_record_length != 0:
            raise ValueError(f'FASTQ check failed. FASTQ file `{self._fastq_path}` '
                'contains invalid number of lines. The file may be truncated or corrupted.')

# pylint: disable=W0613
def _check_fastq(path:Path, args:Union[ValidateArgs,Dict[str, Union[str,list]]]):
    '''Validation for FASTQs'''
    fastq = FASTQ(path)
    fastq.validate_fastq()
