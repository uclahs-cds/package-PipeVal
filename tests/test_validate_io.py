from pathlib import Path
import argparse
import pytest
import mock
import validate

@mock.patch('validate.validate_io.Path', autospec=True)
def test_validate_file_value_error(mock_path):
    mock_path.suffix.return_value = ".no"

    with pytest.raises(TypeError):
        validate.validate_io.validate_file(mock_path, 'file-py')

@mock.patch('validate.validate_io.path_readable')
def test_validate_dir_readable_io_error(mock_path_readable):
    mock_path_readable.side_effect = IOError('oh no')
    test_dir = Path('unreadable/dir')

    with pytest.raises(IOError):
        validate.validate_io.validate_dir(test_dir, 'directory-w')

@mock.patch('validate.validate_io.path_readable')
@mock.patch('validate.validate_io.path_writable')
def test_validate_dir_writable_io_error(mock_path_readable, mock_path_writable):
    mock_path_readable.return_value = True
    mock_path_writable.side_effect = IOError('oh no')
    test_dir = Path('unreadable/unwritable/dir')

    with pytest.raises(IOError):
        validate.validate_io.validate_dir(test_dir, 'directory-rw')

@mock.patch('validate.validate_io.Path', autospec=True)
def test_path_exists(mock_path):
    mock_path.exists.return_value = True

    assert validate.validate_io.path_exists(mock_path)

@mock.patch('validate.validate_io.Path', autospec=True)
def test_path_exists_io_error(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(IOError):
        validate.validate_io.path_exists(mock_path)

@mock.patch('validate.validate_io.os.access')
def test_path_readable(mock_os_access):
    mock_os_access.return_value = True
    test_path = Path('readable/path')

    assert validate.validate_io.path_readable(test_path)

@mock.patch('validate.validate_io.os.access')
def test_path_readable_io_error(mock_os_access):
    mock_os_access.return_value = False
    test_path = Path('not/readable/path')

    with pytest.raises(IOError):
        validate.validate_io.path_readable(test_path)

@mock.patch('validate.validate_io.os.access')
def test_path_writable(mock_os_access):
    mock_os_access.return_value = True
    test_path = Path('writable/path')

    assert validate.validate_io.path_writable(test_path)

@mock.patch('validate.validate_io.os.access')
def test_path_writable_io_error(mock_os_access):
    mock_os_access.return_value = False
    test_path = Path('not/writable/path')

    with pytest.raises(IOError):
        validate.validate_io.path_writable(test_path)

def generate_md5_for_file_success(path):
    return
    #TODO: implement unit test

def generate_md5_for_file_error(path):
    return
    #TODO: implement unit test

def generate_sha512_for_file_success(path):
    return
    #TODO: implement unit test

def generate_sha512_for_file_error(path):
    return
    #TODO: implement unit test