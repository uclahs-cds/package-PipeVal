# Validation CLI Tool 
> An easy to use CLI tool that can be used to validate different parameters in your NF script. Can be used standalone or using a Docker container.

## specs

### function:
> A. Validates your input files and directories for the following characteristics.

Files (bam, vcf, fasta, bed, python)
- Existence of file at given path
- File extension type
- Validity of file for specific file type (i.e. a vcf file is a vcf file)
- Checksums (generates checksum comparison if .md5 or .sha512 file exists)

Directories (read or read-write)
- Existence of directory at given path
- Readability, writability

> B. Generates checksum files and compares checksum files.

### input types:
The validation action can be specified using the -t tag.

|file types|directory types|checksum types|
|----------|---------------|--------------|
|file-bam| directory-r | sha512-gen |
|file-vcf| directory-rw | md5-gen |
|file-fasta|
|file-bed|
|file-py|
|file-input|

If an input type is specified as "file-input", it will automatically try to match the file type or simply check for existence/readability.
If an input type is one of the checksum types, it will create a new checksum file based on the input file path.
All input types regardless will be checked for existence.

### requirements:
When used as a standalone command line tool, the following dependencies must be installed:

|tool|
|----|
|python 3.8|
|samtools 1.11|
|vcftools 0.1.16|

Otherwise, it's recommended to use the docker to keep dependencies bundled.

## usage

### parameters:

Required arg
- _path_ path of file or directory to validate or generate checksum for

Optional args
- _-t, --type_ specific input type
- _-h, --help_ show this help message and exit

### how to use:

_Running the standalone command line tool_
```
python3 -m validate -t file-bam path/to/file.bam [-o]
```

_Running as interactive docker session_
```
docker run -it validate:1.0.0 /bin/bash
(bash): python -m validate -t file-input path/to/file.bam [-o]
```

_Running as Nextflow process with docker_
```
check the example under /example/ or the pipeline-align-DNA repository
```

### usage commands:
#### file specific validation
Currently file type specific validation is supported for the following:
| type | tool |
|------|------|
| bam | samtools |
| vcf | vcftools |

To explicitly check a single file type, run
```
python3 -m validate -t file-py path/to/file.py
```
Where file-py can be replaced with any file type listed in the input types table.
To automatically detect any or multiple file types, run
```
python3 -m validate -t file-input path/to/file.ext
```
The tool will try to automatically detect the file type and do file specific validation, and if the file type is unsupported, will just do a simple existence check.

#### directory specific validation
To run validation for checking basic directory permissions you can run the following

```
python3 -m validate -t directory-rw path/to/directory/
```
```
python3 -m validate -t directory-r path/to/directory/
```

Using "directory-r" for read permissions, and "directory-rw" for read and write permissions.

#### checksum generation (beta)
To generate a sha512 or md5 checksum file using this tool, run the following

```
python3 -m validate -t md5-gen path/to/file.ext
```

```
python3 -m validate -t sha512-gen path/to/file.ext
```

It should create a checksum file at the path/to/file.ext.{checksum_ext}

(TBD: Checksum comparison function still under development)

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

## license:
Author: Gina Kim (ginakim@mednet.ucla.edu)

Pipeval is currently free to use under the GPL 2 license, terms of which are under the "COPYING" file.

Copyright (C) 2021 University of California Los Angeles ("Boutros Lab"). All rights reserved.
