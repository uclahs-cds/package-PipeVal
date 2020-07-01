# Validation CLI Tools
> A collection of easy to use CLI tools that can be used to validate your Nextflow script. Can be used standalone or within a Docker container.

_Requires at least Python 3.4._


## validate_io.py
> Validates your input and output files for the following.

- Existence of file at given path
- File extension type
- Validity of file for file type (i.e. a vcf file is a vcf file)

### Usage:
```
python3 validate_io.py path/to/file.bam [-o]
```

required arg
- _path_ file path of file to validate

optional args
- _-e, --extension_ get file extension
- _-h, --help_ show this help message and exit

### Output:
Valid file
```
Valid
```
-e is selected
```
.bam
```
Invalid file
```
Invalid: Error Message
```


## validate_nf.py
> Validates your Nextflow script level parameters.

*Under Construction*
