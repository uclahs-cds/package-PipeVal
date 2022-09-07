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
