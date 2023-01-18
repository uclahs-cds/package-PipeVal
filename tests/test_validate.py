import pytest
from pathlib import Path
from validate import validate

def test__detect_extension__uncompressed_files():
    assert validate.detect_extension(Path('file.something.vcf')) == '.vcf'
    assert validate.detect_extension(Path('file.something.bed')) == '.bed'
    assert validate.detect_extension(Path('file.something.fastq')) == '.fastq'
    assert validate.detect_extension(Path('file.something.fq')) == '.fq'
    assert validate.detect_extension(Path('file.something.fasta')) == '.fasta'
    assert validate.detect_extension(Path('file.something.fa')) == '.fa'
    assert validate.detect_extension(Path('file.something.bam')) == '.bam'
    assert validate.detect_extension(Path('file.something.cram')) == '.cram'
    assert validate.detect_extension(Path('file.something.sam')) == '.sam'

def test__detect_extension__script():
    assert validate.detect_extension(Path('main.py')) == '.py'

def test__detect_extension__compressed_files():
    assert validate.detect_extension(Path('file.something.vcf.gz')) == '.vcf.gz'
    assert validate.detect_extension(Path('file.something.bed.gz')) ==  '.bed.gz'
    assert validate.detect_extension(Path('file.something.fastq.gz')) ==  '.fastq.gz'
    assert validate.detect_extension(Path('file.something.fq.gz')) == '.fq.gz'

def test__detect_file_type__vcf():
    assert validate.detect_file_type('.vcf') == 'file-vcf'
    assert validate.detect_file_type('.vcf.gz') == 'file-vcf'

def test__detect_file_type__bed():
    assert validate.detect_file_type('.bed') == 'file-bed'
    assert validate.detect_file_type('.bed.gz') == 'file-bed'

def test__detect_file_type__fastq():
    assert validate.detect_file_type('.fastq') == 'file-fastq'
    assert validate.detect_file_type('.fastq.gz') == 'file-fastq'
    assert validate.detect_file_type('.fq') == 'file-fastq'
    assert validate.detect_file_type('.fq.gz') == 'file-fastq'

def test__detect_file_type__fasta():
    assert validate.detect_file_type('.fasta') == 'file-fasta'
    assert validate.detect_file_type('.fa') == 'file-fasta'

def test__detect_file_type__bam():
    assert validate.detect_file_type('.bam') == 'file-bam'
    assert validate.detect_file_type('.cram') == 'file-bam'
    assert validate.detect_file_type('.sam') == 'file-bam'

def test__detect_file_type__unknown():
    assert validate.detect_file_type('.something.vcf') == 'file-unknown'

def test__detect_file_type__unsupported_compression():
    assert validate.detect_file_type('.bam.gz') == 'file-unknown'
    assert validate.detect_file_type('.fasta.gz') == 'file-unknown'

