# pylint: disable=C0116
# pylint: disable=C0114
from pathlib import Path
from unittest.mock import Mock
import warnings
import mock
import pytest

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
from validate.validators.sam import (
    validate_sam_file
)
from validate.validators.cram import (
    validate_cram_file,
    check_cram_index
)
from validate.validate import (
    detect_file_type_and_extension,
    check_extension,
    run_validate,
    validate_file
)
from validate.validate_types import ValidateArgs

@pytest.mark.parametrize(
    'expected_extension, expected_file_type',
    [
        ('.vcf.gz', 'file-vcf'),
        ('.unknown', 'file-unknown')
    ]
)
def test__detect_file_type_and_extension__detects_correct_file_type(
    expected_extension,
    expected_file_type):
    test_path = Path(f'a{expected_extension}')

    file_type, extension = detect_file_type_and_extension(test_path)

    assert extension == expected_extension
    assert file_type == expected_file_type

@pytest.mark.parametrize(
    'test_extension, expected_type',
    [
        ('.vcf.gz', 'file-vcf'),
        ('.unknown', 'file-unknown')
    ]
)
def test__check_extension__correct_file_type(test_extension, expected_type):
    file_type = check_extension(test_extension)

    assert file_type == expected_type

@mock.patch('validate.files.Path', autospec=True)
def test__path_exists__returns_true_for_existing_path(mock_path):
    mock_path.exists.return_value = True

    path_exists(mock_path)

@mock.patch('validate.files.Path', autospec=True)
def test__path_exists__errors_for_non_existing_path(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(IOError):
        path_exists(mock_path)

@mock.patch('validate.files.magic.from_file')
@mock.patch('validate.files.Path', autospec=True)
def test__check_compressed__raises_warning_for_uncompressed_path(mock_path, mock_magic):
    test_extension = '.vcf'
    mock_magic.return_value = 'text/plain'

    with pytest.warns(UserWarning):
        check_compressed(mock_path)

@pytest.mark.parametrize(
    'compression_mime',
    [
        ('application/x-gzip'),
        ('application/x-bzip2')
    ]
)
@mock.patch('validate.files.magic.from_file')
@mock.patch('validate.files.Path', autospec=True)
def test__check_compressed__passes_compression_check(mock_path, mock_magic, compression_mime):
    mock_magic.return_value = compression_mime

    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        check_compressed(mock_path)

@mock.patch('validate.validators.bam.pysam')
def test__validate_bam_file__empty_bam_file(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/bam')

    with pytest.raises(ValueError):
        validate_bam_file(test_path)

@mock.patch('validate.validators.bam.Path', autospec=True)
def test__validate_bam_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError):
        validate_bam_file(mock_path)

@mock.patch('validate.validators.bam.pysam', autospec=True)
def test__check_bam_index__no_index_file_error(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.side_effect = ValueError('no')
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    with pytest.raises(FileNotFoundError):
        check_bam_index('/some/file')

@mock.patch('validate.validators.bam.pysam', autospec=True)
def test__check_bam_index__index_check_pass(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.return_value = True
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    check_bam_index('/some/file')

@mock.patch('validate.validators.bam.pysam')
def test__validate_sam_file__empty_sam_file(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/sam')

    with pytest.raises(ValueError):
        validate_sam_file(test_path)

@mock.patch('validate.validators.sam.Path', autospec=True)
def test__validate_sam_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError):
        validate_sam_file(mock_path)

@pytest.mark.parametrize(
    'test_reference',
    [
        (None),
        ('ref')
    ]
)
@mock.patch('validate.validators.cram.pysam')
def test__validate_cram_file__empty_cram_file(mock_pysam, test_reference):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/cram')

    with pytest.raises(ValueError):
        validate_cram_file(test_path, test_reference)

@mock.patch('validate.validators.cram.Path', autospec=True)
def test__validate_cram_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError):
        validate_cram_file(mock_path)

@mock.patch('validate.validators.cram.pysam', autospec=True)
def test__check_cram_index__no_index_file_error(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.side_effect = ValueError('no')
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    with pytest.raises(FileNotFoundError):
        check_cram_index('/some/file')

@mock.patch('validate.validators.cram.pysam', autospec=True)
def test__check_cram_index__index_check_pass(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.return_value = True
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    check_cram_index('/some/file')

@mock.patch('validate.validators.vcf.subprocess.call')
def test__validate_vcf_file__fails_vcf_validation(mock_call):
    mock_call.return_value = 1

    with pytest.raises(ValueError):
        validate_vcf_file('some/file')

@mock.patch('validate.validators.vcf.subprocess.call')
def test__validate_vcf_file__passes_vcf_validation(mock_call):
    mock_call.return_value = 0

    validate_vcf_file('some/file')

@mock.patch('validate.validate.print_success')
def test__run_validate__passes_validation_no_files(mock_print_success):
    test_args = ValidateArgs(path=[], cram_reference=None)
    mock_print_success.return_value = ''
    run_validate(test_args)

@pytest.mark.parametrize(
    'test_exception',
    [
        (TypeError),
        (ValueError),
        (IOError),
        (OSError)
    ]
)
@mock.patch('validate.validate.detect_file_type_and_extension')
@mock.patch('validate.validate.validate_file')
@mock.patch('validate.validate.print_error')
def test__run_validate__fails_with_failing_checks(
    mock_print_error,
    mock_validate_file,
    mock_detect_file_type_and_extension,
    test_exception):
    test_args = ValidateArgs(path=['some/path'], cram_reference=None)
    mock_validate_file.side_effect = test_exception
    mock_detect_file_type_and_extension.return_value = ('', '')
    mock_print_error.return_value = ''
    expected_code = 1

    with pytest.raises(SystemExit) as pytest_exit:
        run_validate(test_args)
    assert pytest_exit.value.code == expected_code

@mock.patch('validate.validate.path_exists')
def test__validate_file__errors_with_invalid_extension(mock_path_exists):
    mock_path_exists.return_value = True

    with pytest.raises(TypeError):
        validate_file('', 'file-test', '', None)

@pytest.mark.parametrize(
    'test_file_types',
    [
        ('file-vcf'),
        ('file-fastq'),
        ('file-bed')
    ]
)
@mock.patch('validate.validate.path_exists')
@mock.patch('validate.validate.check_compressed')
@mock.patch('validate.validate.validate_checksums')
@mock.patch('validate.validate.CHECK_FUNCTION_SWITCH')
def test__validate_file__checks_compression(
    mock_check_function_switch,
    mock_validate_checksums,
    mock_check_compressed,
    mock_path_exists,
    test_file_types):
    mock_validate_checksums.return_value = None
    mock_path_exists.return_value = True
    mock_check_function_switch.return_value = {}

    validate_file('', test_file_types, 'ext', None)

    mock_check_compressed.assert_called_once()
