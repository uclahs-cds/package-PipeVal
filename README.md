# PipeVal

## Overview
Pipeval is designed to be an easy to use CLI tool that can be used to validate different parameters in your Nextflow script/pipeline. It can be used standalone or using a Docker container.

Its primary functions are to generate and/or compare checksum files and validate your input files and directories.


**Requirements:**
When used as a standalone command line tool, the following dependencies must be installed:

|tool|
|----|
|python 3.10|
|vcftools 0.1.16|

Otherwise, it's recommended to use the docker to keep dependencies bundled.

## Functions

### Validation

**Supported Inputs**


Note: All input types will be checked for existence.

| file type | description |
| -------| ------ |
| bam | Validate bam/cram/sam using `pysam`. Check for index file in same directory as BAM |
| vcf | Validate vcf using `vcftools` |
| fasta |  |
| bed | |
| py | |



directory checks
| type name | description |
| -------| ------------ |
|directory-r | check if directory is readable |
|directory-rw | check if directory is readable and writeable |

#### How To Run
The validation action can be specified using the `-t` tag. If not specified, it defaults to `file`. If an input type is specified as "file" (default), it will automatically try to match the file type.

##### File Validation

To automatically detect any or multiple file types, run
```
validate path/to/file.ext
```
The tool will try to automatically detect the file type and do file specific validation, and if the file type is unsupported, will just do a simple existence check.

##### Directory Validation
To run validation for checking basic directory permissions you can run the following

```
validate -t directory-rw path/to/directory/
```
```
validate -t directory-r path/to/directory/
```

Using "directory-r" for read permissions, and "directory-rw" for read and write permissions.



### Commands


### Generate Checksum
Generate a new checksum file based on the input file path. Or generates checksum comparison if .md5 or .sha512 file exists.




## Usage

### Parameters

Required arg
- _path_ path of one or more files or directories to validate or generate checksum for

Optional args
- _-t, --type_ specific input type
- _-h, --help_ show this help message and exit



#### Checksum Generation (beta)
To generate a sha512 or md5 checksum file using this tool, run the following

```
generate-checksum -t md5 path/to/file.ext
```

```
generate-checksum -t sha512 path/to/file.ext
```

Available types: `md5`, `sha512`

It should create a checksum file at the path/to/file.ext.{checksum_ext}

(TBD: Checksum comparison function still under development)

### Output
Valid input
```
Input: path/to/input is valid
```
Invalid input or error
```
Error: path/to/input Error Message
```

If the input is invalid in any way, `validate` will sys.exit and throw an exception which can be detected by Nextflow and handled accordingly.
If a BAM input is missing an accompanying BAM index file in the same directory, `validate` will not throw an exception but will print a warning.

### Execution Options
_Running the standalone command line tool_
```
validate path/to/file.bam
```

_Running as interactive docker session_
```
docker run -it pipeval:3.0.0 /bin/bash
(bash): validate path/to/file.bam
```

_Running as Nextflow process with docker_
```
check the example under /example/ or the pipeline-align-DNA repository
```

## References
Initial design: https://uclahs.box.com/s/eejwmwmdky7wsfcrs8a3jijy70rh6atp

## License
Author: Gina Kim (ginakim@mednet.ucla.edu), Arpi Beshlikyan (abeshlikyan@mednet.ucla.edu)

PipeVal is licensed under the GNU General Public License version 2. See the file LICENSE for the terms of the GNU GPL license.

PipeVal is a tool which can be used to validate the inputs and outputs of various bioinformatic pipelines.

Copyright (C) 2020-2023 University of California Los Angeles ("Boutros Lab") All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
