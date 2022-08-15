'''Helper methods for bam file validation'''

import pysam

def validate_bam_file(path):
    '''Validates bam file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools bam check failed. " + str(err)) from err

    numLines = int(pysam.view("-c", str(path)).strip())
    if 0 >= numLines:
        raise ValueError("pysam bam check failed. No reads in " + str(path))

    return True
