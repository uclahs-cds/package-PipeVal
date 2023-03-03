from pathlib import Path
import mock
import pytest

from validate.validate import (
    detect_file_type_and_extension,
    check_extension
)
from validate.files import (
    check_compressed,
    path_exists
)

def test__detect_file_type_and_extension__detects_correct_file_type():
    test_path = Path('a.vcf.gz')
    expected_file_type = 'file-vcf'
    expected_extensions = ['.vcf', '.gz']

    file_type, extension = detect_file_type_and_extension(test_path)

    assert extension == ''.join(expected_extensions)
    assert file_type == expected_file_type

def test__detect_file_type_and_extension__detects_correct_unknown_file_type():
    test_path = Path('a.unknown')
    expected_file_type = 'file-unknown'
    expected_extensions = ['.unknown']

    file_type, extension = detect_file_type_and_extension(test_path)

    assert extension == ''.join(expected_extensions)
    assert file_type == expected_file_type

def test__check_extension__correct_file_type():
    test_extension = '.vcf.gz'
    expected_type = 'file-vcf'

    file_type = check_extension(test_extension)

    assert file_type == expected_type

def test__check_extension__correct_unknown_file_type():
    test_extension = '.unknown'
    expected_type = 'file-unknown'

    file_type = check_extension(test_extension)

    assert file_type == expected_type


