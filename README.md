# PipeVal

## Overview
Pipeval is an easy to use CLI tool that can be used to validate different inputs and parameters in your Nextflow script/pipeline. It can be used standalone or using a Docker container.

Its primary functions are to generate and/or compare checksum files and validate your input files and directories.


**Requirements:**<br>
When used as a standalone command line tool, the following dependencies must be installed:

|tool|
|----|
|Python 3.10|
|VCFtools 0.1.16|

## Execution Options

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

## Validation
The tool will attempt to automatically detect the file type and do file specific validation. 
If the file type is unsupported, it will just do a simple existence and checksum (if MD5 or SHA512 checksums exist) check.

_Note: All input types will be checked for existence and checksum matching._

### Supported Inputs

| File Type     | Validation |
| :-------:     | :---------: |
| BAM           | Validate BAM/CRAM/SAM using `pysam`. <br> Check for an index file in same directory as the BAM.<br><br>_Note: If a BAM input is missing an accompanying BAM index file in the same directory,<br> `validate` will not throw an exception but will print a warning._|
| VCF           | Validate VCF using `VCFtools` |
| FASTA         | |
| BED           | |
| Python script | |

_Note: If the input is invalid in any way, `validate` will exit with a non-zero status code._


### Expected Output

Valid input
```
Input: path/to/input is valid
```
Invalid input or error
```
Error: path/to/input Error Message
```

### How To Run

**Parameters**

Required args:<br>
- _`path`_ 
   - path of one or more files to validate

Optional args
- _`-h`, `--help`_ 
   - show the help message and exit

#### File Validation

To automatically detect any or multiple file types, run
```
validate path/to/file.ext
```

## Generate Checksum
Generate a new checksum file based on the input file path. Or generates checksum comparison if `.md5` or `.sha512` file exists.

### How To Run

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

### Pysam

1. Repository: [pysam-developers/pysam](https://github.com/pysam-developers/pysam)

#### Publications

2.	[Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer, Gabor Marth, Goncalo Abecasis, Richard Durbin, 1000 Genome Project Data Processing Subgroup, The Sequence Alignment/Map format and SAMtools, Bioinformatics, Volume 25, Issue 16, 15 August 2009, Pages 2078–2079, https://doi.org/10.1093/bioinformatics/btp352](https://academic.oup.com/bioinformatics/article/25/16/2078/204688)

3. [James K Bonfield, John Marshall, Petr Danecek, Heng Li, Valeriu Ohan, Andrew Whitwham, Thomas Keane, Robert M Davies, HTSlib: C library for reading/writing high-throughput sequencing data, GigaScience, Volume 10, Issue 2, February 2021, giab007, https://doi.org/10.1093/gigascience/giab007](https://academic.oup.com/gigascience/article/10/2/giab007/6139334)

4. [Danecek P, Bonfield JK, Liddle J, Marshall J, Ohan V, Pollard MO, Whitwham A, Keane T, McCarthy SA, Davies RM, Li H. Twelve years of SAMtools and BCFtools. Gigascience. 2021 Feb 16;10(2):giab008. doi: 10.1093/gigascience/giab008. PMID: 33590861; PMCID: PMC7931819.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7931819/)

### VCFtools

5. Repository: [vcftools/vcftools](https://github.com/vcftools/vcftools)

#### Publications


6. [Danecek P, Auton A, Abecasis G, Albers CA, Banks E, DePristo MA, Handsaker RE, Lunter G, Marth GT, Sherry ST, McVean G, Durbin R; 1000 Genomes Project Analysis Group. The variant call format and VCFtools. Bioinformatics. 2011 Aug 1;27(15):2156-8. doi: 10.1093/bioinformatics/btr330. Epub 2011 Jun 7. PMID: 21653522; PMCID: PMC3137218.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3137218/)


## License
Author: Gina Kim (ginakim@mednet.ucla.edu), Arpi Beshlikyan (abeshlikyan@mednet.ucla.edu), Yash Patel (YashPatel@mednet.ucla.edu), Madison Jordan (MBJordan@mednet.ucla.edu)

PipeVal is licensed under the GNU General Public License version 2. See the file LICENSE for the terms of the GNU GPL license.

PipeVal is a tool which can be used to validate the inputs and outputs of various bioinformatic pipelines.

Copyright (C) 2020-2023 University of California Los Angeles ("Boutros Lab") All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
