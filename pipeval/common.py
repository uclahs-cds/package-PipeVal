""" Common functions for PipeVal """
import os
from functools import wraps

# pylint: disable=C0103,W0613
def skippedValidation(name):
    """
    Conditionally mark a validation to be skipped

    If the environment variable f'PIPEVAL_SKIP_{name}' is set to `true`,
    the decorated function will skip that validation.
    """
    def decorator(func):
        return func

    def print_skip_message(func):
        @wraps(func)
        def skip_message(*args, **kwargs):
            print(f'PID:{os.getpid()} - Skipping validation {name.upper()}')

        return skip_message

    value = os.environ.get(f"PIPEVAL_SKIP_{name.upper()}")
    should_skip_validate = value is not None and value.lower() == 'true'

    if not should_skip_validate:
        return decorator

    return print_skip_message
