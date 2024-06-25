'''Type definitions for validation functions'''
from collections import namedtuple

ValidateArgs = namedtuple(
    'args',
    'path, cram_reference, unmapped_bam, processes, test_integrity'
)
