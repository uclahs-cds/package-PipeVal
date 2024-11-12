# pylint: disable=C0116
# pylint: disable=C0114
from pathlib import Path
from argparse import Namespace, ArgumentTypeError
from unittest.mock import Mock, mock_open, MagicMock
import warnings
import zlib
import gzip
import bz2
import mock
import pytest

from pipeval.validate.files import (
    _check_compressed,
    _path_exists,
    _identify_compression,
    _check_compression_integrity
)
from pipeval.validate.validators.bam import (
    _validate_bam_file,
    _check_bam_index
)
from pipeval.validate.validators.vcf import (
    _validate_vcf_file
)
from pipeval.validate.validators.sam import (
    _validate_sam_file
)
from pipeval.validate.validators.cram import (
    _validate_cram_file,
    _check_cram_index
)
from pipeval.validate.validators.fastq import (
    FASTQ,
    FASTQ_RECORD,
    FASTQ_RECORD_VALIDATOR
)
from pipeval.validate.validate import (
    _detect_file_type_and_extension,
    _check_extension,
    run_validate,
    _validate_file,
    _validation_worker
)
from pipeval.validate.__main__ import positive_integer
from pipeval.validate.validate_types import ValidateArgs

def test__positive_integer__returns_correct_integer():
    expected_number = 2
    number_str = '2'
    assert expected_number == positive_integer(number_str)

@pytest.mark.parametrize(
    'number_str',
    [
        ('-2'),
        ('0'),
        ('1.2'),
        ('number'),
        ('')
    ]
)
def test__positive_integer__fails_non_positive_integers(number_str):
    with pytest.raises(ArgumentTypeError):
        positive_integer(number_str)

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

    file_type, extension = _detect_file_type_and_extension(test_path)

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
    file_type = _check_extension(test_extension)

    assert file_type == expected_type

@mock.patch('pipeval.validate.files.Path', autospec=True)
def test__path_exists__returns_true_for_existing_path(mock_path):
    mock_path.exists.return_value = True

    _path_exists(mock_path)

@mock.patch('pipeval.validate.files.Path', autospec=True)
def test__path_exists__errors_for_non_existing_path(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(IOError):
        _path_exists(mock_path)

@mock.patch('pipeval.validate.files.magic.from_file')
@mock.patch('pipeval.validate.files.Path', autospec=True)
def test__check_compressed__raises_warning_for_uncompressed_path(mock_path, mock_magic):
    mock_magic.return_value = 'text/plain'
    test_args = ValidateArgs(
        path=[],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False
    )

    with pytest.warns(UserWarning):
        _check_compressed(mock_path, test_args)

@pytest.mark.parametrize(
    'compression_mime',
    [
        ('application/x-gzip'),
        ('application/x-bzip2')
    ]
)
@mock.patch('pipeval.validate.files._check_compression_integrity')
@mock.patch('pipeval.validate.files.magic.from_file')
@mock.patch('pipeval.validate.files.Path', autospec=True)
def test__check_compressed__passes_compression_check(
    mock_path,
    mock_magic,
    mock_integrity,
    compression_mime):
    mock_magic.return_value = compression_mime
    mock_integrity.return_value = None
    test_args = ValidateArgs(
        path=[],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False
    )

    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        _check_compressed(mock_path, test_args)

@mock.patch('pipeval.validate.validators.bam.pysam')
def test__validate_bam_file__empty_bam_file(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/bam')

    with pytest.raises(ValueError):
        _validate_bam_file(test_path, unmapped_bam=False)

@mock.patch('pipeval.validate.validators.bam.pysam')
def test__validate_bam_file__quickcheck_called_with_unmapped(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter(['read1'])
    mock_quickcheck = Mock()

    mock_pysam.quickcheck = mock_quickcheck
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = 'empty/valid/bam'
    test_unmapped_option = '-u'

    _validate_bam_file(test_path, unmapped_bam=True)
    mock_quickcheck.assert_called_with(test_path, test_unmapped_option)

@mock.patch('pipeval.validate.validators.bam.pysam')
def test__validate_bam_file__alignmentfile_called_with_unmapped(mock_pysam):
    mock_alignment_file = MagicMock()
    mock_alignment_file.__iter__.return_value = ['read1']
    mock_quickcheck = Mock()

    mock_pysam.quickcheck = mock_quickcheck
    mock_pysam.AlignmentFile = mock_alignment_file

    test_path = 'empty/valid/bam'
    test_unmapped_option = False

    _validate_bam_file(test_path, unmapped_bam=True)
    mock_alignment_file.assert_called_with(
        **{'filename': test_path, 'check_sq': test_unmapped_option}
    )

@mock.patch('pipeval.validate.validators.bam.Path', autospec=True)
def test__validate_bam_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError):
        _validate_bam_file(mock_path, unmapped_bam=False)

@mock.patch('pipeval.validate.validators.bam.pysam', autospec=True)
def test__check_bam_index__no_index_file_error(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.side_effect = ValueError('no')
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    with pytest.raises(FileNotFoundError):
        _check_bam_index('/some/file')

@mock.patch('pipeval.validate.validators.bam.pysam', autospec=True)
def test__check_bam_index__index_check_pass(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.return_value = True
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    _check_bam_index('/some/file')

@mock.patch('pipeval.validate.validators.bam.pysam')
def test__validate_sam_file__empty_sam_file(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/sam')

    with pytest.raises(ValueError):
        _validate_sam_file(test_path)

@mock.patch('pipeval.validate.validators.sam.Path', autospec=True)
def test__validate_sam_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError):
        _validate_sam_file(mock_path)

@pytest.mark.parametrize(
    'test_reference',
    [
        (None),
        ('ref')
    ]
)
@mock.patch('pipeval.validate.validators.cram.pysam')
def test__validate_cram_file__empty_cram_file(mock_pysam, test_reference):
    mock_alignment_file = Mock()
    mock_alignment_file.head.return_value = iter([])
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    test_path = Path('empty/valid/cram')

    with pytest.raises(ValueError):
        _validate_cram_file(test_path, test_reference)

@mock.patch('pipeval.validate.validators.cram.Path', autospec=True)
def test__validate_cram_file__quickcheck_fails(mock_path):
    mock_path.exists.return_value = False

    with pytest.raises(ValueError):
        _validate_cram_file(mock_path)

@mock.patch('pipeval.validate.validators.cram.pysam', autospec=True)
def test__check_cram_index__no_index_file_error(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.side_effect = ValueError('no')
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    with pytest.raises(FileNotFoundError):
        _check_cram_index('/some/file')

@mock.patch('pipeval.validate.validators.cram.pysam', autospec=True)
def test__check_cram_index__index_check_pass(mock_pysam):
    mock_alignment_file = Mock()
    mock_alignment_file.check_index.return_value = True
    mock_pysam.AlignmentFile.return_value = mock_alignment_file

    _check_cram_index('/some/file')

@mock.patch('pipeval.validate.validators.vcf.subprocess.call')
def test__validate_vcf_file__fails_vcf_validation(mock_call):
    mock_call.return_value = 1

    with pytest.raises(ValueError):
        _validate_vcf_file('some/file')

@mock.patch('pipeval.validate.validators.vcf.subprocess.call')
def test__validate_vcf_file__passes_vcf_validation(mock_call):
    mock_call.return_value = 0

    _validate_vcf_file('some/file')

def test__run_validate__passes_validation_no_files():
    test_args = ValidateArgs(
        path=[],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False
    )
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
@mock.patch('pipeval.validate.validate._detect_file_type_and_extension')
@mock.patch('pipeval.validate.validate._validate_file')
@mock.patch('pipeval.validate.validate._print_error')
@mock.patch('pipeval.validate.validate.Path.resolve')
def test___validation_worker__fails_with_failing_checks(
    mock_path_resolve,
    mock_print_error,
    mock_validate_file,
    mock_detect_file_type_and_extension,
    test_exception):
    test_path = 'some/path'
    test_args = ValidateArgs(
        path=[test_path],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False)
    mock_path_resolve.return_value = test_path
    mock_validate_file.side_effect = test_exception
    mock_detect_file_type_and_extension.return_value = ('', '')
    mock_print_error.return_value = ''

    assert not _validation_worker(test_path, test_args)

@mock.patch('pipeval.validate.validate.Path.resolve', autospec=True)
@mock.patch('pipeval.validate.validate.multiprocessing.Pool')
def test__run_validate__passes_on_all_valid_files(
    mock_pool,
    mock_path_resolve
    ):
    test_path = 'some/path'
    test_args = ValidateArgs(
        path=[test_path],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False)

    mock_path_resolve.return_value = None
    mock_pool.return_value.__enter__.return_value = Namespace(starmap=lambda y, z: [True])

    run_validate(test_args)

@mock.patch('pipeval.validate.validate.Path.resolve', autospec=True)
@mock.patch('pipeval.validate.validate.multiprocessing.Pool')
def test__run_validate__fails_with_failing_file(
    mock_pool,
    mock_path_resolve):
    test_path = 'some/path'
    test_args = ValidateArgs(
        path=[test_path],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False)
    expected_code = 1

    mock_path_resolve.return_value = None
    mock_pool.return_value.__enter__.return_value = Namespace(starmap=lambda y, z: [False])

    with pytest.raises(SystemExit) as pytest_exit:
        run_validate(test_args)
    assert pytest_exit.value.code == expected_code

@mock.patch('pipeval.validate.validate._path_exists')
def test__validate_file__errors_with_invalid_extension(mock_path_exists):
    mock_path_exists.return_value = True

    with pytest.raises(TypeError):
        _validate_file('', 'file-test', '', None)

@pytest.mark.parametrize(
    'test_file_types',
    [
        ('file-vcf'),
        ('file-fastq'),
        ('file-bed')
    ]
)
@mock.patch('pipeval.validate.validate._path_exists')
@mock.patch('pipeval.validate.validate._check_compressed')
@mock.patch('pipeval.validate.validate._validate_checksums')
@mock.patch('pipeval.validate.validate.CHECK_FUNCTION_SWITCH')
def test__validate_file__checks_compression(
    mock_check_function_switch,
    mock_validate_checksums,
    mock_check_compressed,
    mock_path_exists,
    test_file_types):
    mock_validate_checksums.return_value = None
    mock_path_exists.return_value = True
    mock_check_function_switch.return_value = {}

    test_args = ValidateArgs(
        path=[],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False)

    _validate_file('', test_file_types, 'ext', test_args)

    mock_check_compressed.assert_called_once()

@mock.patch('pipeval.validate.validate.Path.resolve', autospec=True)
def test__run_validate__fails_on_unresolvable_symlink(mock_path_resolve):
    expected_error = FileNotFoundError
    mock_path_resolve.side_effect = expected_error

    test_path = 'some/path'

    test_args = ValidateArgs(
        path=[test_path],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False)

    with pytest.raises(expected_error):
        run_validate(test_args)

@mock.patch('pipeval.validate.validate.Path.resolve', autospec=True)
@mock.patch('pipeval.validate.validate._detect_file_type_and_extension')
@mock.patch('pipeval.validate.validate._validate_file')
@mock.patch('pipeval.validate.validate._print_success')
def test___validation_worker__passes_proper_validation(
    mock_print_success,
    mock_validate_file,
    mock_detect_file_type_and_extension,
    mock_path_resolve):
    mock_print_success.return_value = None
    mock_detect_file_type_and_extension.return_value = (None, None)
    mock_validate_file.return_value = None
    mock_path_resolve.return_value = None

    test_path = 'some/path'

    test_args = ValidateArgs(
        path=[test_path],
        cram_reference=None,
        unmapped_bam=False,
        processes=1,
        test_integrity=False)

    _validation_worker(test_path, test_args)

@pytest.mark.parametrize(
    'test_record',
    [
        (['badID', 'A', '+', '!']),
        (['@ID', 'BADSEQ', '+', '!FFFFF']),
        (['@ID', 'A', 'badextra', '!']),
        (['@ID', 'A', '+', ' ']),
        (['@ID', 'AC', '+', '!']),
        (['badID', 'BADSEQ', 'badextra', '   '])
    ]
)
def test__validate_record__fails_with_invalid_reads(test_record):
    record = FASTQ_RECORD(
        identifier = test_record[0],
        sequence = test_record[1],
        extra_field = test_record[2],
        quality = test_record[3]
    )
    with pytest.raises(ValueError):
        FASTQ_RECORD_VALIDATOR.validate_record(record)

def test__validate_record__passes_valid_read():
    valid_record = FASTQ_RECORD(
        identifier = '@record1',
        sequence = 'ACTGANAAAC',
        extra_field = '+',
        quality = 'FFF*GH!#FF'
    )

    FASTQ_RECORD_VALIDATOR.validate_record(valid_record)

# pylint: disable=W0212
@pytest.mark.parametrize(
    'test_file_type, test_handler',
    [
        ('application/x-gzip', gzip.open),
        # ('application/gzip', gzip.open),
        ('application/x-bzip2', bz2.open),
        ('text/plain', open)
    ]
)
@mock.patch('pipeval.validate.validators.fastq.magic.from_file')
def test___get_file_handler__detects_correct_handler(
    mock_from_file,
    test_file_type,
    test_handler):
    mock_from_file.return_value = test_file_type

    test_fastq = FASTQ(Path('test/path'))

    assert test_handler == test_fastq._file_handler

@mock.patch('pipeval.validate.validators.fastq.magic.from_file')
def test___get_file_handler__fails_with_invalid_type(mock_from_file):
    mock_from_file.return_value = 'invalid/type'

    with pytest.raises(TypeError):
        _ = FASTQ(Path('test/path'))

# pylint: disable=W0612
@pytest.mark.parametrize(
    'test_num_lines',
    [
        (1),
        (2),
        (3),
        (5),
    ]
)
@mock.patch('pipeval.validate.validators.fastq.magic.from_file')
@mock.patch('pipeval.validate.validators.fastq.FASTQ_RECORD_VALIDATOR.validate_record')
def test__validate_fastq__fails_with_invalid_number_of_lines(
    mock_validate_record,
    mock_from_file,
    test_num_lines):
    test_data = '\n'.join([str(i) for i in range(test_num_lines)])
    mock_from_file.return_value = 'text/plain'
    mock_validate_record.return_value = lambda x: None
    with mock.patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
        test_fastq = FASTQ(Path('test/path'))
        with pytest.raises(ValueError):
            test_fastq.validate_fastq()

# pylint: disable=W0612
@mock.patch('pipeval.validate.validators.fastq.magic.from_file')
@mock.patch('pipeval.validate.validators.fastq.FASTQ_RECORD_VALIDATOR.validate_record')
def test__validate_fastq__fails_with_invalid_record(
    mock_validate_record,
    mock_from_file):
    test_data = '1\n2\n3\n4'
    mock_from_file.return_value = 'text/plain'
    mock_validate_record.side_effect = ValueError('no')
    with mock.patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
        test_fastq = FASTQ(Path('test/path'))
        with pytest.raises(ValueError):
            test_fastq.validate_fastq()

# pylint: disable=W0612
@pytest.mark.parametrize(
    'test_num_lines',
    [
        (0),
        (4),
        (8),
        (12),
    ]
)
@mock.patch('pipeval.validate.validators.fastq.magic.from_file')
@mock.patch('pipeval.validate.validators.fastq.FASTQ_RECORD_VALIDATOR.validate_record')
def test__validate_fastq__passes_valid_fastq(
    mock_validate_record,
    mock_from_file,
    test_num_lines):
    test_data = '\n'.join([str(i) for i in range(test_num_lines)])
    mock_from_file.return_value = 'text/plain'
    mock_validate_record.return_value = lambda x: None
    with mock.patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
        test_fastq = FASTQ(Path('test/path'))
        test_fastq.validate_fastq()


# pylint: disable=W0212
@pytest.mark.parametrize(
    'test_file_type, test_handler',
    [
        ('application/x-gzip', gzip.open),
        ('application/x-bzip2', bz2.open),
        ('any/other', None)
    ]
)
@mock.patch('pipeval.validate.files.magic.from_file')
def test___identify_compression__identified_correct_handler(
    mock_from_file,
    test_file_type,
    test_handler):
    mock_from_file.return_value = test_file_type

    identifier_handler = _identify_compression(Path('test/path'))

    assert identifier_handler == test_handler

@pytest.mark.parametrize(
    'test_handler',
    [
        ("gzip.open"),
        ("bz2.open")
    ]
)
def test___check_compression_integrity__passes_valid_file(test_handler):
    with mock.patch(test_handler, mock_open(read_data=b'data')) as mock_file:
        _check_compression_integrity('test/path', mock_file)

@pytest.mark.parametrize(
    'test_handler, test_exception',
    [
        ("gzip.open", gzip.BadGzipFile),
        ("gzip.open", EOFError),
        ("gzip.open", zlib.error),
        ("bz2.open", EOFError),
        ("bz2.open", zlib.error)
    ]
)
def test___check_compression_integrity__raises_on_exception(test_handler, test_exception):
    with mock.patch(test_handler, mock_open(read_data=b'data')) as mock_file:
        mock_file.return_value.read.side_effect = test_exception

        with pytest.raises(TypeError):
            _check_compression_integrity('test/path', mock_file)
