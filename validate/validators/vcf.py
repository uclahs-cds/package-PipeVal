# Helper methods for vcf file validation

import subprocess

def validate_vcf_file(path):
    vcf_command = "vcf-validator " + str(path)

    try:
        subprocess.check_call(vcf_command, shell=True)
    except subprocess.CalledProcessError as e:
        raise ValueError("vcftools validation check failed. " + str(e))
    
    print("Ran command: " + vcf_command)

    return True