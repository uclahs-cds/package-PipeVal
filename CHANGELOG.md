# Changelog

All notable changes to the PipeVal tool.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.2.0] - 2024-12-13

### Changed

- Update `pysam` version to `0.22.1`

## [5.1.0] - 2024-07-08

### Added

- Add validation flowchart
- Add support for unmapped BAM
- Add additional MIME type for GZIP compressed files
- Add support for checksum files formatted with any whitespace separator

## [5.0.0] - 2024-02-16

### Added

- Validation skip functionality for checksums

## [5.0.0-rc.3] - 2023-12-07

### Added

- Integrity test for compressed files

## [5.0.0-rc.2] - 2023-12-06

### Added

- FASTQ validator

## [5.0.0-rc.1] - 2023-11-22

### Changed

- Restructured CLI to have common main command `pipeval`

## [4.0.0] - 2023-11-22

### Added

- Parallelize validation

## [4.0.0-rc.2] - 2023-04-24

### Changed

- Resolve potential symlinks before validation

## [4.0.0-rc.1] - 2023-04-11

### Added

- Add check for empty BAM files (valid header but no reads).
- Add auto-build workflow to push image to `uclahs-cds` registry
- Add repo source label to Dockerfile
- Add check for existence of index file
- Add references for VCFtools and Pysam in README
- Unit tests for existing functions
- Unit tests for main runner functions
- Add separate checks for SAM and CRAM files
- Compression validation and detection through `python-magic`

### Changed

- Make `-t` optional, default to `file-input`
- Explicitly set Python version to `3.10`
- Split validation and checksum generation into different CLI commands
- Re-organize functions
- Change builder image to mambaforge in Dockerfile
- Update README input tables and command examples
- Re-structure README with details of current tool

### Removed

- Remove deprecated parameter options from README
- Remove inaccessible design doc link from README
- Remove directory checking
- Remove user-specified file type option

## [3.0.0] - 2022-08-03

### Added

- Add `bldocker` user and group to Dockerfile
- Add support for mutliple input files

### Changed

- Updated bl-base to 1.1.0
- Installed tools using `mamba`
- Convert module to Python CLI package; now runs directly from commandline with `validate`.
- Single source package version from \_\_init\_\_.py
- Use `pysam` instead of `samtools` in bam file validation.

### Fixed

- Add handling for valid file types whose validation is not yet implemented.

## [2.1.6] - 2021-10-18

### Changed

- File type detection update to properly detect file type when filename contains multiple .

### Fixed

- Fixed bug with detecting fasta files

[2.1.6]: https://github.com/uclahs-cds/package-PipeVal/releases/tag/v2.1.6
[3.0.0]: https://github.com/uclahs-cds/package-PipeVal/compare/v2.1.6...v3.0.0
[4.0.0]: https://github.com/uclahs-cds/package-PipeVal/compare/v4.0.0-rc.2...v4.0.0
[4.0.0-rc.1]: https://github.com/uclahs-cds/package-PipeVal/compare/v3.0.0...v4.0.0-rc.1
[4.0.0-rc.2]: https://github.com/uclahs-cds/package-PipeVal/compare/v4.0.0-rc.1...v4.0.0-rc.2
[5.0.0]: https://github.com/uclahs-cds/package-PipeVal/compare/v5.0.0-rc.3...v5.0.0
[5.0.0-rc.1]: https://github.com/uclahs-cds/package-PipeVal/compare/v4.0.0...v5.0.0-rc.1
[5.0.0-rc.2]: https://github.com/uclahs-cds/package-PipeVal/compare/v5.0.0-rc.1...v5.0.0-rc.2
[5.0.0-rc.3]: https://github.com/uclahs-cds/package-PipeVal/compare/v5.0.0-rc.2...v5.0.0-rc.3
[5.1.0]: https://github.com/uclahs-cds/package-PipeVal/compare/v5.0.0...v5.1.0
[5.2.0]: https://github.com/uclahs-cds/package-PipeVal/compare/v5.1.0...v5.2.0
