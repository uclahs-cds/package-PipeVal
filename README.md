# PipeVal

## Overview
Pipeval is an easy to use CLI tool that can be used to validate different inputs and parameters in your Nextflow script/pipeline. It can be used standalone or using a Docker container.

Its primary functions are to generate and/or compare checksum files and validate your input files and directories.


**Requirements:**<br>
When used as a standalone command line tool, the following dependencies must be installed:

|tool|
|----|
|python 3.10|
|vcftools 0.1.16|

### Execution Options

**Running the standalone command line tool:**
```
validate path/to/file.bam
```

**Running as interactive docker session:**
```
docker run -it pipeval:3.0.0 /bin/bash
(bash): validate path/to/file.bam
```
_Note: Update the tag to the latest version as necessary._

**Running as Nextflow process with docker:**<br>
See the example under [/example/](https://github.com/uclahs-cds/public-tool-PipeVal/tree/main/example) or the pipeline-align-DNA repository



## Functions

### Validation
The tool will try to automatically detect the file type and do file specific validation. 
If the file type is unsupported, it will just do a simple existence and checksum (if MD5 or SHA512 checksums exist) check.

_Note: All input types will be checked for existence and checksum matching._

**Supported Inputs**

| File Type | Description |
| :-------: | ------ |
| bam | Validate bam/cram/sam using `pysam`. <br> Check for an index file in same directory as the BAM.<br><br>_Note: If a BAM input is missing an accompanying BAM index file in the same directory,<br> `validate` will not throw an exception but will print a warning._|
| vcf | Validate vcf using `vcftools` |
| fasta |  |
| bed | |
| py | |

| Directory Check Name | Description |
| :-------: | ------------ |
|directory-r | Check if directory is readable |
|directory-rw | Check if directory is readable and writeable |


**Expected Output**

Valid input
```
Input: path/to/input is valid
```
Invalid input or error
```
Error: path/to/input Error Message
```

If the input is invalid in any way, `validate` will exit with a non-zero status code.


#### How To Run

**Parameters**

Required args:<br>
- _`path`_ 
   - path of one or more files or directories to validate

Optional args
- _`-t`, `--type`_
   - specific input type
- _`-h`, `--help`_ 
   - show the help message and exit

The validation action can be specified using the `-t` tag. If not specified, it defaults to `file`. If an input type is specified as "file" (default), it will automatically try to match the file type.

##### File Validation

To automatically detect any or multiple file types, run
```
validate path/to/file.ext
```

##### Directory Validation
To check for read and write permissions, use `directory-rw`:
```
validate -t directory-rw path/to/directory/
```

To check for read permissions, use `directory-r`:
```
validate -t directory-r path/to/directory/
```

### Generate Checksum
Generate a new checksum file based on the input file path. Or generates checksum comparison if `.md5` or `.sha512` file exists.

#### How To Run

**Parameters**

Required arg
- _path_ path of one or more files or directories to validate

Optional args
- _-t, --type_ checksum type
- _-h, --help_ show this help message and exit


#### Checksum Generation (beta)
Generate a checksum file for the specified file in the same directory. Available types: `md5`, `sha512`

for `md5`:
```
generate-checksum -t md5 path/to/file.ext
```

for `sha512`:
```
generate-checksum -t sha512 path/to/file.ext
```

## References

## License
Author: Gina Kim (ginakim@mednet.ucla.edu), Arpi Beshlikyan (abeshlikyan@mednet.ucla.edu)

PipeVal is licensed under the GNU General Public License version 2. See the file LICENSE for the terms of the GNU GPL license.

PipeVal is a tool which can be used to validate the inputs and outputs of various bioinformatic pipelines.

Copyright (C) 2020-2023 University of California Los Angeles ("Boutros Lab") All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
