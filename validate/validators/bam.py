'''Helper methods for bam file validation'''

import subprocess

def validate_bam_file(path):
    '''Validates bam file'''
    samtools_command = "samtools quickcheck " + str(path)

    try:
        subprocess.check_call(samtools_command, shell=True)
    except subprocess.CalledProcessError as err:
        raise ValueError("samtools bam check failed. " + str(err)) from err

    print("Ran command: " + samtools_command)

    return True
