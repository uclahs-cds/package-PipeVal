'''Test functions in validate.py'''
from pathlib import Path
from validate import validate

def test__detect_extension__uncompressed_files():
    '''Tests detection of all supported uncompressed extensions'''
    assert validate.detect_extension(Path('file.name.vcf')) == '.vcf'
    assert validate.detect_extension(Path('file.name.bed')) == '.bed'
    assert validate.detect_extension(Path('file.name.fastq')) == '.fastq'
    assert validate.detect_extension(Path('file.name.fq')) == '.fq'
    assert validate.detect_extension(Path('file.name.fasta')) == '.fasta'
    assert validate.detect_extension(Path('file.name.fa')) == '.fa'
    assert validate.detect_extension(Path('file.name.bam')) == '.bam'
    assert validate.detect_extension(Path('file.name.cram')) == '.cram'
    assert validate.detect_extension(Path('file.name.sam')) == '.sam'

def test__detect_extension__script():
    '''Tests detection of script extension'''
    assert validate.detect_extension(Path('main.py')) == '.py'

def test__detect_extension__compressed_files():
    '''Tests detection of all supported compressed full extensions'''
    assert validate.detect_extension(Path('file.name.vcf.gz')) == '.vcf.gz'
    assert validate.detect_extension(Path('file.name.bed.gz')) ==  '.bed.gz'
    assert validate.detect_extension(Path('file.name.fastq.gz')) ==  '.fastq.gz'
    assert validate.detect_extension(Path('file.name.fq.gz')) == '.fq.gz'

def test__detect_file_type__vcf():
    '''Tests detection of file type from supported vcf extensions'''
    assert validate.detect_file_type('.vcf') == 'file-vcf'
    assert validate.detect_file_type('.vcf.gz') == 'file-vcf'

def test__detect_file_type__bed():
    '''Tests detection of file type from supported bed extensions'''
    assert validate.detect_file_type('.bed') == 'file-bed'
    assert validate.detect_file_type('.bed.gz') == 'file-bed'

def test__detect_file_type__fastq():
    '''Tests detection of file type from supported fastq extensions'''
    assert validate.detect_file_type('.fastq') == 'file-fastq'
    assert validate.detect_file_type('.fastq.gz') == 'file-fastq'
    assert validate.detect_file_type('.fq') == 'file-fastq'
    assert validate.detect_file_type('.fq.gz') == 'file-fastq'

def test__detect_file_type__fasta():
    '''Tests detection of file type from supported fasta extensions'''
    assert validate.detect_file_type('.fasta') == 'file-fasta'
    assert validate.detect_file_type('.fa') == 'file-fasta'

def test__detect_file_type__bam():
    '''Tests detection of file type from supported bam extensions'''
    assert validate.detect_file_type('.bam') == 'file-bam'
    assert validate.detect_file_type('.cram') == 'file-bam'
    assert validate.detect_file_type('.sam') == 'file-bam'

def test__detect_file_type__unknown():
    '''Tests detection of unsupported file type'''
    assert validate.detect_file_type('.name.vcf') == 'file-unknown'

def test__detect_file_type__py():
    '''Tests detection of .py file type'''
    assert validate.detect_file_type('.py') == 'file-py'

def test__detect_file_type__unsupported_compression():
    '''Tests detection of unsupported compression'''
    assert validate.detect_file_type('.bam.gz') == 'file-unknown'
    assert validate.detect_file_type('.fasta.gz') == 'file-unknown'
