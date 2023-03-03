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

@mock.patch('validate.files.Path', autospec=True)
def test__path_exists__returns_true_for_existing_path(mock_path):
    mock_path.exists.return_value = True

    path_exists(mock_path)

@mock.patch('validate.files.Path', autospec=True)
def test__path_exists__errors_for_non_existing_path(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(IOError) as io_error:
        path_exists(mock_path)

    assert str(io_error.value) == 'File or directory does not exist.'

@mock.patch('validate.files.Path', autospec=True)
def test__check_compressed__raises_warning_for_uncompressed_path(mock_path)
    mock_path.return_value = 'mypath'
    test_extension = '.vcf'

    with pytest.warns():
        check_compressed(mock_path, test_extension)
