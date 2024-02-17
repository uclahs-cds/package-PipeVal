""" Common functions for PipeVal """
import os

# pylint: disable=C0103,W0613
def skippedValidation(name):
    """
    Conditionally mark a validation to be skipped

    If the environment variable f'PIPEVAL_SKIP_{name}' is set to `true`,
    the decorated function will skip that validation.
    """
    def decorator(func):
        return func

    def do_nothing(func):
        return lambda *args, **kwargs: \
            print(f'PID:{os.getpid()} - Skipping validation {name.upper()}')

    value = os.environ.get(f"PIPEVAL_SKIP_{name.upper()}")
    should_skip_validate = value is not None and value.lower() == 'true'

    if not should_skip_validate:
        return decorator

    return do_nothing
