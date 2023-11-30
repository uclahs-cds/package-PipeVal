'''Helper methods for vcf file validation'''

from pathlib import Path
import argparse

import subprocess

def _validate_vcf_file(path):
    '''Validate vcf file'''
    vcf_command = "vcf-validator " + str(path)

    try:
        subprocess.check_call(vcf_command, shell=True)
    except subprocess.CalledProcessError as err:
        raise ValueError("vcftools validation check failed. " + str(err)) from err

    return True

# pylint: disable=W0613
def _check_vcf(path:Path, args:argparse.Namespace):
    ''' Validation for VCFs '''
    _validate_vcf_file(path)
