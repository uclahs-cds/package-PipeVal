# pylint: disable=C0116
# pylint: disable=C0114
from unittest.mock import mock_open
import hashlib
from types import SimpleNamespace
import mock
import pytest

from generate_checksum.checksum import (
    validate_checksums,
    compare_hash,
    write_checksum_file,
    generate_md5,
    generate_sha512,
    generate_checksum
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

    with pytest.raises(IOError):
        validate_checksums(mock_path)

@pytest.mark.parametrize(
    'hash_type',
    [
        ('md5'),
        ('sha512')
    ]
)
@mock.patch('generate_checksum.checksum.generate_sha512')
@mock.patch('generate_checksum.checksum.generate_md5')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__compares_correct_checksums(
    mock_path,
    mock_generate_md5,
    mock_generate_sha512,
    hash_type):
    checksum_to_compare = '123456abcd'
    mock_path.read_text.return_value = f'{checksum_to_compare} fname'

    mock_generate_md5.return_value = checksum_to_compare
    mock_generate_sha512.return_value = checksum_to_compare

    assert compare_hash(hash_type, mock_path, mock_path)

@pytest.mark.parametrize(
    'hash_type',
    [
        ('md5'),
        ('sha512')
    ]
)
@mock.patch('generate_checksum.checksum.generate_sha512')
@mock.patch('generate_checksum.checksum.generate_md5')
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__compares_incorrect_checksums(
    mock_path,
    mock_generate_md5,
    mock_generate_sha512,
    hash_type):
    checksum_to_compare = '123456abcd'
    mock_path.read_text.return_value = f'{checksum_to_compare} fname'

    mock_generate_md5.return_value = 'wrong'
    mock_generate_sha512.return_value = 'wrong'

    assert not compare_hash(hash_type, mock_path, mock_path)

@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__compare_hash__fails_on_invalid_checksum_type(mock_path):
    mock_path.read_text.return_value = 'checksum fname'
    hash_type = 'invalid_hash_type'

    with pytest.raises(IOError):
        compare_hash(hash_type, mock_path, mock_path)

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

# pylint: disable=W0613
@mock.patch('generate_checksum.checksum.open', new_callable=mock_open)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
@mock.patch('generate_checksum.checksum.iter')
def test__generate_md5__return_correct_checksum(mock_iter, mock_path, mock_read_open):
    md5_checksum = hashlib.md5()
    md5_checksum.update(b'')
    mock_iter.return_value = iter([b''])

    assert generate_md5(mock_path) == md5_checksum.hexdigest()

# pylint: disable=W0613
@mock.patch('generate_checksum.checksum.open', new_callable=mock_open)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
@mock.patch('generate_checksum.checksum.iter')
def test__generate_sha512__return_correct_checksum(mock_iter, mock_path, mock_read_open):
    sha512_checksum = hashlib.sha512()
    sha512_checksum.update(b'')
    mock_iter.return_value = iter([b''])

    assert generate_sha512(mock_path) == sha512_checksum.hexdigest()

@pytest.mark.parametrize(
    'test_args',
    [
        (SimpleNamespace(path=[], type='md5')),
        (SimpleNamespace(path=[], type='sha512'))
    ]
)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__generate_checksum__calls_passes_generation_no_files(mock_path, test_args):
    generate_checksum(test_args)

@mock.patch('generate_checksum.checksum.Path', autospec=True)
def test__generate_checksum__fails_with_invalid_type(mock_path):
    test_args = SimpleNamespace(path=['some/path'], type='bad_type')
    expected_code = 1

    with pytest.raises(SystemExit) as pytest_exit:
        generate_checksum(test_args)
    assert pytest_exit.value.code == expected_code

@pytest.mark.parametrize(
    'test_args',
    [
        (SimpleNamespace(path=['some/path'], type='md5')),
        (SimpleNamespace(path=['some/path'], type='sha512'))
    ]
)
@mock.patch('generate_checksum.checksum.Path', autospec=True)
@mock.patch('generate_checksum.checksum.generate_md5')
@mock.patch('generate_checksum.checksum.generate_sha512')
@mock.patch('generate_checksum.checksum.write_checksum_file')
def test__generate_checksum__fails_with_failed_write(
    mock_write_checksum_file,
    mock_generate_sha512,
    mock_generate_md5,
    mock_path,
    test_args):
    mock_generate_md5.return_value = ''
    mock_generate_sha512.return_value = ''
    mock_write_checksum_file.side_effect = IOError('fail write')
    expected_code = 1

    with pytest.raises(SystemExit) as pytest_exit:
        generate_checksum(test_args)
    assert pytest_exit.value.code == expected_code
