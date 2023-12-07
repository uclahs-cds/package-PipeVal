# PipeVal

- [Overview](#overview)
- [Docker](#docker)
- [Installation](#installation)
    - [From GitHub](#install-directly-from-github)
    - [From local](#install-from-cloned-repository)
- [Usage](#usage)
    - [validate](#validate)
        - [Supported Types](#supported-types)
        - [Expected Output](#expected-output)
    - [generate-checksum](#generate-checksum)
- [Development](#development)
- [References](#references)
- [Discussions](#discussions)
- [Contributors](#contributors)
- [License](#license)

## Overview
PipeVal is an easy to use CLI tool that can be used to validate different inputs and parameters in various settings, including Nextflow scripts/pipelines. It can be used standalone or using a Docker container.

Its primary functions are to generate and/or compare checksum files and validate input files.

## Docker
The tool can be used via the docker image [`ghcr.io/uclahs-cds/pipeval:<tag>`](https://github.com/orgs/uclahs-cds/packages/container/package/pipeval)

## Installation
The tool can be installed as a standalone command line tool. The following dependencies must be installed for this option:
|Tool|Version|
|:---:|:---:|
|Python|3.10|
|VCFtools|0.1.16|

Additionally, the `libmagic` C library must also be installed on the system.

### Installing `libmagic`

On Debian/Ubuntu, install through:
```Bash
sudo apt-get install libmagic-dev
```

On Mac, install through homebrew (https://brew.sh/):
```Bash
brew install libmagic
```

`libmagic` can also be installed through the `conda` package manager:
```Bash
conda install -c conda-forge libmagic
```

With the dependencies (and the proper versions) installed, install `pipeval` through one of the options below:

### Install directly from GitHub through SSH
```Bash
pip install git+ssh://git@github.com/uclahs-cds/package-PipeVal.git
```

### Install directly from GitHub through HTTPS
```Bash
pip install git+https://git@github.com/uclahs-cds/package-PipeVal.git
```

### Install from cloned repository
```Bash
<clone the PipeVal GitHub repository>
cd </path/to/cloned/repository>
pip install .
```

## Usage
### `pipeval validate`
```
usage: pipeval validate [-h] [-v] [-r CRAM_REFERENCE] path [path ...]

positional arguments:
  path                  one or more paths of files to validate

options:
  -h, --help            show this help message and exit
  -r CRAM_REFERENCE, --cram-reference CRAM_REFERENCE
                        Path to reference file for CRAM
  -p PROCESSES, --processes PROCESSES
                        Number of processes to run in parallel when validating multiple files
  -t, --test-integrity  Whether to perform a full integrity test on compressed files
```

The tool will attempt to automatically detect the file type based on extension and perform the approriate validations. The tool will also perform an existence check along with a checksum check if an MD5 or SHA512 checksum exists regardless of file type.

#### Supported Types

| File Type     | Validation |
| ---------     | ---------- |
| BAM           | Validate BAM/CRAM/SAM using `pysam`. <br> Check for an index file in same directory as the BAM.<br><br>_Note: If a BAM input is missing an accompanying BAM index file in the same directory,<br> `validate` will not throw an exception but will print a warning._|
| SAM           | Validate SAM file using `pysam`. |
| CRAM          | Validate CRAM file using `pysam`. <br> Check for existence of an index file in the same directory as the CRAM. <br> Accept an optional reference genome parameter for use with CRAM. <br> In the absence of the parameter, the reference URL from the CRAM header will be used. <br><br>_Note: If a CRAM input is missing an accompanying CRAM index file in the same directory,<br> `validate` will not throw an exception but will print a warning._|
| VCF           | Validate VCF using `VCFtools` |


_Note: If the input is invalid in any way, `validate` will exit with a non-zero status code._

#### Expected Output

- Valid input:
```
Input: path/to/input is valid <file-type>
```
- Invalid input or failed validation
```
Error: path/to/input <error message>
```

### `pipeval generate-checksum`
```
usage: pipeval generate-checksum [-h] [-t {md5,sha512}] [-v] path [path ...]

positional arguments:
  path                  one or more paths of files to validate

options:
  -h, --help            show this help message and exit
  -t {md5,sha512}, --type {md5,sha512}
                        Checksum type
```

## Development

Testing for PipeVal itself can be done through `pytest` by running the following:
```Bash
pytest
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


## Discussions

- [Issue tracker](https://github.com/uclahs-cds/package-PipeVal/issues) to report errors and enhancement ideas.
- Discussions can take place in [package-PipeVal Discussions](https://github.com/uclahs-cds/package-PipeVal/discussions)
- [package-PipeVal pull requests](https://github.com/uclahs-cds/package-PipeVal/pulls) are also open for discussion

## Contributors

Please see list of [Contributors](https://github.com/uclahs-cds/package-PipeVal/graphs/contributors) at GitHub.

## License
Author: Yash Patel (YashPatel@mednet.ucla.edu), Arpi Beshlikyan (abeshlikyan@mednet.ucla.edu), Madison Jordan (MBJordan@mednet.ucla.edu), Gina Kim (ginakim@mednet.ucla.edu)

PipeVal is licensed under the GNU General Public License version 2. See the file LICENSE for the terms of the GNU GPL license.

PipeVal is a tool which can be used to validate the inputs and outputs of various bioinformatic pipelines.

Copyright (C) 2020-2023 University of California Los Angeles ("Boutros Lab") All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
