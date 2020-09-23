# Validation CLI Tool 
> An easy to use CLI tool that can be used to validate different parameters in your NF script. Can be used standalone or using a Docker container.

_Requires at least Python 3.4._


## validate python module
> Validates your input files and directories for the following characteristics.

Files (bam, vf, fasta, bed, python)
- Existence of file at given path
- File extension type
- Validity of file for file type (i.e. a vcf file is a vcf file)
- Checksums (generates checksum comparison if .md5 or .sha512 file exists)

Directories (read or read-write)
- Existence of directory at given path
- Readability, writability

### input types:
|file types|directory types|
|----------|---------------|
|file-bam| directory-r |
|file-vcf| directory-rw |
|file-fasta|
|file-bed|
|file-py|

If an input type is not specified with the -t tag, it will only check readability.

### usage:

_Running the python script_
```
python3 -m validate -t file-bam path/to/file.bam [-o]
```
_Running as interactive docker session_

```
docker run -it validate:1.0.0 /bin/bash
(bash): python -m validate -t file-bam path/to/file.bam [-o]
```

_Running as Nextflow process with docker_
```
check the example under /example/ or the pipeline-align-DNA repository
```
### parameters:

Required arg
- _path_ path of file or directory to validate

Optional args
- _-t, --type_ specific input type
- _-h, --help_ show this help message and exit

### output:
Valid input
```
Input: path/to/input is valid
```
Invalid input or error
```
Error: path/to/input Error Message
```

If the input is invalid in any way, validate_io will sys.exit and throw an exception which can be detected by Nextflow and handled accordingly.

## references:
Initial design: https://uclahs.box.com/s/eejwmwmdky7wsfcrs8a3jijy70rh6atp
