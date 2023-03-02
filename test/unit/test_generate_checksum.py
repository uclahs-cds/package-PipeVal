from pathlib import Path
import pytest
from unittest.mock import mock_open
import mock

from generate_checksum.checksum import (
    validate_checksums,
    compare_hash,
    write_checksum_file,
    generate_md5,
    generate_sha512
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

@mock.patch('generate_checksum.checksum.open', new_callable=mock_open)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__write_checksum_file__writes_proper_checksum(mock_path, mock_write_open):
    file_path = 'filepath'
    computed_hash = 'hash'
    hash_type = 'md5'
    mock_path.__str__.return_value = file_path

    write_checksum_file(mock_path, hash_type, computed_hash)

    mock_write_open.assert_called_once_with(f'{file_path}.{hash_type}', 'w')

    handle = mock_write_open()
    handle.write.assert_called_once_with(f'{computed_hash}  {file_path}\n')

@mock.patch('generate_checksum.checksum.open', new_callable=mock_open)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
@mock.patch('generate_checksum.checksum.iter')
def test__generate_md5__return_correct_checksum(mock_iter, mock_path, mock_read_open):
    md5_checksum = 'd41d8cd98f00b204e9800998ecf8427e'
    mock_iter.return_value = iter([b''])

    assert generate_md5(mock_path) == md5_checksum

@mock.patch('generate_checksum.checksum.open', new_callable=mock_open)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
@mock.patch('generate_checksum.checksum.iter')
def test__generate_sha512__return_correct_checksum(mock_iter, mock_path, mock_read_open):
    sha512_checksum = 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
    mock_iter.return_value = iter([b''])

    assert generate_sha512(mock_path) == sha512_checksum
