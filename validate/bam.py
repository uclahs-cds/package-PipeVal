# Helper methods for bam file validation

import subprocess

def validate_bam_file(path):
    samtools_command = "samtools quickcheck " + str(path)

    try:
        subprocess.check_call(samtools_command, shell=True)
    except subprocess.CalledProcessError as e:
        raise ValueError("samtools bam check failed. " + str(e))

    print("Ran command: " + samtools_command)

    return True