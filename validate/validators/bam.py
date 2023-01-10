'''Helper methods for bam file validation'''

import pysam

def validate_bam_file(path):
    '''Validates bam file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools bam check failed. " + str(err)) from err

    bam_head: pysam.IteratorRowHead = pysam.AlignmentFile(str(path)).head(1)
    if next(bam_head, None) is None: #if the iterator is exhausted, next() returns None
        raise ValueError("pysam bam check failed. No reads in " + str(path))

    return True

def check_bam_index(path):
    '''Checks if index file is present and can be opened'''
    try:
        pysam.AlignmentFile(str(path)).check_index()
    except ValueError as err:
        raise FileNotFoundError(f'''pysam bam index check failed. Index file for {str(path)}
            could not be opened or does not exist.''') from err

    return True

def check_bam(path:Path):
    ''' Validation for BAMs '''
    bam.validate_bam_file(path)
    bam.check_bam_index(path)
