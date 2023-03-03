from pathlib import Path
import mock
import pytest

from validate.validate import (
    detect_file_type_and_extension
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


