# pylint: disable=C0116
# pylint: disable=C0114
from pathlib import Path
from unittest.mock import Mock
import warnings
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
from validate.validators.bam import (
    validate_bam_file,
    check_bam_index
)
from validate.validators.vcf import (
    validate_vcf_file
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
def test__check_compressed__raises_warning_for_uncompressed_path(mock_path):
    test_extension = '.vcf'

    with pytest.warns(UserWarning):
        check_compressed(mock_path, test_extension)

@mock.patch('validate.files.Path', autospec=True)
def test__check_compressed__passes_compression_check(mock_path):
    test_extension = '.vcf.gz'

    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        check_compressed(mock_path, test_extension)

@mock.patch('validate.validators.bam.pysam')
def test__validate_bam_file__empty_bam_file(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/bam')

    with pytest.raises(ValueError) as ve_error:
        validate_bam_file(test_path)

    assert str(ve_error.value) == f'pysam bam check failed. No reads in {test_path}'

@mock.patch('validate.validators.bam.Path', autospec=True)
def test__validate_bam_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError) as ve_error:
        validate_bam_file(mock_path)

    assert str(ve_error.value).startswith('samtools bam check failed.')

@mock.patch('validate.validators.bam.pysam', autospec=True)
def test__check_bam_index__no_index_file_error(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.side_effect = ValueError('no')
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    with pytest.raises(FileNotFoundError) as fnf_error:
        check_bam_index('/some/file')

    assert str(fnf_error.value).startswith('pysam bam index check failed.')

@mock.patch('validate.validators.bam.pysam', autospec=True)
def test__check_bam_index__index_check_pass(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.return_value = True
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    check_bam_index('/some/file')

@mock.patch('validate.validators.vcf.subprocess.call')
def test__validate_vcf_file__fails_vcf_validation(mock_call):
    mock_call.return_value = 1

    with pytest.raises(ValueError) as ve_error:
        validate_vcf_file('some/file')
    assert str(ve_error.value).startswith('vcftools validation check failed.')

@mock.patch('validate.validators.vcf.subprocess.call')
def test__validate_vcf_file__passes_vcf_validation(mock_call):
    mock_call.return_value = 0

    validate_vcf_file('some/file')
