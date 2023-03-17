'''Type definitions for validation functions'''
from collections import namedtuple

ValidateArgs = namedtuple(
    'args',
    'path, cram_reference'
)
