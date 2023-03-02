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

@mock.patch('generate_checksum.checksum.generate_md5')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__compares_correct_md5_checksums(mock_path, mock_generate_md5):
    checksum_to_compare = '123456abcd'
    hash_type = 'md5'
    mock_path.read_text.return_value = f'{checksum_to_compare} fname'

    mock_generate_md5.return_value = checksum_to_compare

    assert compare_hash(hash_type, mock_path, mock_path)

@mock.patch('generate_checksum.checksum.generate_sha512')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__compares_correct_sha512_checksums(mock_path, mock_generate_sha512):
    checksum_to_compare = '123456abcd'
    hash_type = 'sha512'
    mock_path.read_text.return_value = f'{checksum_to_compare} fname'

    mock_generate_sha512.return_value = checksum_to_compare

    assert compare_hash(hash_type, mock_path, mock_path)

@mock.patch('generate_checksum.checksum.generate_md5')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__compares_incorrect_md5_checksums(mock_path, mock_generate_md5):
    checksum_to_compare = '123456abcd'
    hash_type = 'md5'
    mock_path.read_text.return_value = f'{checksum_to_compare} fname'

    mock_generate_md5.return_value = 'wrong'

    assert compare_hash(hash_type, mock_path, mock_path) == False

@mock.patch('generate_checksum.checksum.generate_sha512')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__compares_incorrect_sha512_checksums(mock_path, mock_generate_sha512):
    checksum_to_compare = '123456abcd'
    hash_type = 'sha512'
    mock_path.read_text.return_value = f'{checksum_to_compare} fname'

    mock_generate_sha512.return_value = 'wrong'

    assert compare_hash(hash_type, mock_path, mock_path) == False

@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__fails_on_invalid_checksum_type(mock_path):
    mock_path.read_text.return_value = 'checksum fname'
    hash_type = 'invalid_hash_type'

    with pytest.raises(IOError) as io_error:
        compare_hash(hash_type, mock_path, mock_path)

    assert str(io_error.value) == 'Incorrect hash parameters'
