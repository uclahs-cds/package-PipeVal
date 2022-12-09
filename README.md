# PipeVal
> An easy to use CLI tool that can be used to validate different parameters in your NF script/pipeline. Can be used standalone or using a Docker container.

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
The validation action can be specified using the `-t` tag. If not specified, it defaults to `file-input`.

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
|python 3.10|
|vcftools 0.1.16|

Otherwise, it's recommended to use the docker to keep dependencies bundled.

## usage

### parameters:

Required arg
- _path_ path of one or more files or directories to validate or generate checksum for

Optional args
- _-t, --type_ specific input type
- _-h, --help_ show this help message and exit

### how to use:

_Running the standalone command line tool_
```
validate -t file-bam path/to/file.bam
```

_Running as interactive docker session_
```
docker run -it validate:1.0.0 /bin/bash
(bash): validate -t file-input path/to/file.bam
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
| bam | pysam |
| vcf | vcftools |

To explicitly check a single file type, run
```
validate -t file-py path/to/file.py
```
Where file-py can be replaced with any file type listed in the input types table.
To automatically detect any or multiple file types, run
```
validate -t file-input path/to/file.ext
```
The tool will try to automatically detect the file type and do file specific validation, and if the file type is unsupported, will just do a simple existence check.

#### directory specific validation
To run validation for checking basic directory permissions you can run the following

```
validate -t directory-rw path/to/directory/
```
```
validate -t directory-r path/to/directory/
```

Using "directory-r" for read permissions, and "directory-rw" for read and write permissions.

#### checksum generation (beta)
To generate a sha512 or md5 checksum file using this tool, run the following

```
validate -t md5-gen path/to/file.ext
```

```
validate -t sha512-gen path/to/file.ext
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

If the input is invalid in any way, `validate` will sys.exit and throw an exception which can be detected by Nextflow and handled accordingly.

## references:
Initial design: https://uclahs.box.com/s/eejwmwmdky7wsfcrs8a3jijy70rh6atp

## license:
Author: Gina Kim (ginakim@mednet.ucla.edu), Arpi Beshlikyan (abeshlikyan@mednet.ucla.edu)

PipeVal is licensed under the GNU General Public License version 2. See the file LICENSE for the terms of the GNU GPL license.

PipeVal is a tool which can be used to validate the inputs and outputs of various bioinformatic pipelines.

Copyright (C) 2020-2022 University of California Los Angeles ("Boutros Lab") All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
