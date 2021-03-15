# Validation CLI Tool 
> An easy to use CLI tool that can be used to validate different parameters in your NF script. Can be used standalone or using a Docker container.

## specs

### functions:
> Validates your input files and directories for the following characteristics.

Files (bam, vcf, fasta, bed, python)
- Existence of file at given path
- File extension type
- Validity of file for file type (i.e. a vcf file is a vcf file)
- Checksums (generates checksum comparison if .md5 or .sha512 file exists)

Directories (read or read-write)
- Existence of directory at given path
- Readability, writability

> Generates checksum files and compares checksum files.

### input types:
The input type/function can be specified using the -t tag.

|file types|directory types|checksum types|
|----------|---------------|--------------|
|file-bam| directory-r | sha512-gen |
|file-vcf| directory-rw | md5-gen |
|file-fasta|
|file-bed|
|file-py|
|file-input|

.gz files are currently buggy

If an input type is not specified with the -t tag, it will only check readability.
If an input type is specified as "file-input", it will automatically try to match the file type.
If an input type is one of the checksum types, it will create a new checksum file based on the input file path.

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

### general usage:

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

### specific usage:
#### file specific validation
Currently file specific validation is supported for the following:
| type | tool |
|------|------|
| bam | samtools |
| vcf | vcftools |

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
