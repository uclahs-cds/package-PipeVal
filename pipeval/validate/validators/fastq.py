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
class FASTQ_RECORD_VALIDATOR:
    minimim_quality_ordinal: ClassVar[int] = 33
    maximum_quality_ordinal: ClassVar[int] = 126
    record_identifier_format: ClassVar[re.Pattern] = re.compile('^@')
    extra_field_format: ClassVar[re.Pattern] = re.compile('^\+')
    sequence_format: ClassVar[re.Pattern] = re.compile('^[ACTGNactgn]+$')

    @staticmethod
    def validate_record(record:list):
        '''Validate the given FASTQ read record'''
        invalid_entries = []
        identifier = record[0]
        sequence = record[1]
        extra_field = record[2]
        quality = record[3]

        if not FASTQ_RECORD_VALIDATOR.record_identifier_format.match(identifier):
            invalid_entries.append(
                f'Record identifier `{identifier}` is invalid. It must begin with \'@\''
            )

        if not FASTQ_RECORD_VALIDATOR.sequence_format.match(sequence):
            invalid_entries.append(
                f'Read sequence `{sequence}` contains invalid characters. '
                'Only \'ACTGNactgn\' are allowed'
            )

        if not FASTQ_RECORD_VALIDATOR.extra_field_format.match(extra_field):
            invalid_entries.append(
                f'Extra field `{extra_field}` is invalid. It must begin with \'+\''
            )

        if len(sequence) != len(quality):
            invalid_entries.append(
                f'Sequence and quality must be of the same length:\n'
                f'Sequence - {len(sequence)} - {sequence}\n'
                f'Quality - {len(quality)} - {quality}'
            )

        min_quality = min(quality, key=lambda x: ord(x))
        max_quality = max(quality, key=lambda x: ord(x))

        if ord(min_quality) < FASTQ_RECORD_VALIDATOR.minimim_quality_ordinal or \
            ord(max_quality) > FASTQ_RECORD_VALIDATOR.maximum_quality_ordinal:
            invalid_entries.append(
                f'Quality scores out of valid range. Quality scores must fall between '
                f'{FASTQ_RECORD_VALIDATOR.minimim_quality_ordinal} and '
                f'{FASTQ_RECORD_VALIDATOR.maximum_quality_ordinal}. '
                f'Found min:`{min_quality}` ({ord(min_quality)}) and '
                f'max:`{max_quality}` ({ord(max_quality)}) in record.'
            )

        if len(invalid_entries) != 0:
            record_errors = '\n'.join(invalid_entries)
            raise ValueError(f'Record {record} is invalid: {record_errors}')

class FASTQ():
    def __init__(self, fastq_file:Path):
        '''Constructor'''
        self._fastq_path = fastq_file
        self._file_handler = self._get_file_handler()

    def _get_file_handler(self):
        '''Detect file format and return approriate handler to read file'''
        _handler_map = {
            'application/x-gzip': gzip.open,
            'application/x-bzip2': bz2.open,
            'text/plain': open
        }

        file_mime = magic.from_file(self._fastq_path.resolve(), mime=True)

        handler = _handler_map.get(file_mime, None)

        if handler is None:
            raise TypeError(f'Unexpected FASTQ format `{file_mime}` for file: `{self._fastq_path}`')

        return handler

    def validate_fastq(self):
        with self._file_handler(self._fastq_path, 'rt') as rd:
            current_record = []
            current_record_length = 0
            for line in rd:
                current_record.append(line.strip())
                current_record_length = current_record_length + 1

                if current_record_length == RECORD_LENGTH:
                    FASTQ_RECORD_VALIDATOR.validate_record(current_record)
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
