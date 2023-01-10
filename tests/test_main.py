# pylint: disable=1101
# TO-DO: Fix tests and remove pylint disable above
'''Test functions in __main__.py'''
from pathlib import Path
from unittest.mock import Mock
import pytest
import mock
import validate

@mock.patch('validate.__main__.Path', autospec=True)
def test_validate_file_value_error(mock_path):
    '''Tests value error for validate_file'''
    mock_path.suffix.return_value = ".no"

    with pytest.raises(TypeError):
        validate.__main__.validate_file(mock_path, 'file-py')

@mock.patch('validate.__main__.path_readable')
def test_validate_dir_readable_io_error(mock_path_readable):
    '''Tests readable IO error for validate_dir'''
    mock_path_readable.side_effect = IOError('oh no')
    test_dir = Path('unreadable/dir')

    with pytest.raises(IOError):
        validate.__main__.validate_dir(test_dir, 'directory-w')

@mock.patch('validate.__main__.path_readable')
@mock.patch('validate.__main__.path_writable')
def test_validate_dir_writable_io_error(mock_path_readable, mock_path_writable):
    '''Tests writable IO error for validate_dir'''
    mock_path_readable.return_value = True
    mock_path_writable.side_effect = IOError('oh no')
    test_dir = Path('unreadable/unwritable/dir')

    with pytest.raises(IOError):
        validate.__main__.validate_dir(test_dir, 'directory-rw')

@mock.patch('validate.__main__.Path', autospec=True)
def test_path_exists(mock_path):
    '''Tests path_exits'''
    mock_path.exists.return_value = True

    assert validate.__main__.path_exists(mock_path)

@mock.patch('validate.__main__.Path', autospec=True)
def test_path_exists_io_error(mock_path):
    '''Tests IO error for path_exists'''
    mock_path.exists.return_value = False

    with pytest.raises(IOError):
        validate.__main__.path_exists(mock_path)

@mock.patch('validate.__main__.os.access')
def test_path_readable(mock_os_access):
    '''Tests path_readable'''
    mock_os_access.return_value = True
    test_path = Path('readable/path')

    assert validate.__main__.path_readable(test_path)

@mock.patch('validate.__main__.os.access')
def test_path_readable_io_error(mock_os_access):
    '''Tests IO error for path_readable'''
    mock_os_access.return_value = False
    test_path = Path('not/readable/path')

    with pytest.raises(IOError):
        validate.__main__.path_readable(test_path)

@mock.patch('validate.__main__.os.access')
def test_path_writable(mock_os_access):
    '''Tests path_writable'''
    mock_os_access.return_value = True
    test_path = Path('writable/path')

    assert validate.__main__.path_writable(test_path)

@mock.patch('validate.__main__.os.access')
def test_path_writable_io_error(mock_os_access):
    '''Tests IO error for path_writable'''
    mock_os_access.return_value = False
    test_path = Path('not/writable/path')

    with pytest.raises(IOError):
        validate.__main__.path_writable(test_path)

@mock.patch('validate.validators.bam.pysam')
def test_file_bam_empty(mock_pysam):
    '''Tests Value error for valid BAM header with no reads'''
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file
    test_path = Path('empty/valid/bam')

    with pytest.raises(ValueError):
        validate.validators.bam.validate_bam_file(test_path)

def generate_md5_for_file_success():
    '''Tests successful generate_md5'''
    return

def generate_md5_for_file_error():
    '''Tests generate_md5 error'''
    return

def generate_sha512_for_file_success():
    '''Tests successful generate_sha512'''
    return

def generate_sha512_for_file_error():
    '''Tests generate_sha512 error'''
    return
