'''Helper methods for bam file validation'''

import pysam

def validate_bam_file(path):
    '''Validates bam file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools bam check failed. " + str(err)) from err

    num_lines = int(pysam.view("-c", str(path)).strip())
    if num_lines <= 0:
        raise ValueError("pysam bam check failed. No reads in " + str(path))

    return True
