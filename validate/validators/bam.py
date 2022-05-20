'''Helper methods for bam file validation'''

import subprocess
import pysam

def validate_bam_file(path):
    '''Validates bam file'''
    try:
        pysam.quickcheck(str(path))
    except pysam.SamtoolsError as err:
        raise ValueError("samtools bam check failed. " + str(err)) from err

    print("Ran command: pysam.quickcheck()")

    return True
