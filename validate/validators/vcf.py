'''Helper methods for vcf file validation'''

from pathlib import Path

import subprocess

def validate_vcf_file(path):
    '''Validate vcf file'''
    vcf_command = "vcf-validator " + str(path)

    try:
        subprocess.check_call(vcf_command, shell=True)
    except subprocess.CalledProcessError as err:
        raise ValueError("vcftools validation check failed. " + str(err)) from err

    return True

def check_vcf(path:Path):
    ''' Validation for VCFs '''
    validate_vcf_file(path)
