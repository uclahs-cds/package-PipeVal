from pathlib import Path
import pytest
import mock

from generate_checksum.checksum import (
    validate_checksums,
    compare_hash
)

@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__validate_checksums__validate_checksums_passes_with_no_checksum_file(mock_path):
    mock_path.suffix.return_value = ''
    mock_path.with_suffix.return_value = mock_path
    mock_path.exists.return_value = False

    validate_checksums(mock_path)

@mock.patch('generate_checksum.checksum.compare_hash')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__validate_checksums__validate_checksum_passes(mock_path, mock_compare_hash):
    mock_path.suffix.return_value = ''
    mock_path.with_suffix.return_value = mock_path
    mock_path.exists.return_value = True

    mock_compare_hash.return_value =  True

    validate_checksums(mock_path)

@mock.patch('generate_checksum.checksum.compare_hash')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__validate_checksums__error_raised_when_comparison_fails(mock_path, mock_compare_hash):
    mock_path.suffix.return_value = ''
    mock_path.with_suffix.return_value = mock_path
    mock_path.exists.return_value = True

    mock_compare_hash.return_value =  False

    with pytest.raises(IOError) as io_error:
        validate_checksums(mock_path)

    assert str(io_error.value) == 'File is corrupted, md5 checksum failed.'

def test__compare_hash__compares_md5_checksums()
