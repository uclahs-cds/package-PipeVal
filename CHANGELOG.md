# Changelog
All notable changes to the PipeVal tool.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
### Added
- Add check for empty BAM files (valid header but no reads).
- Add auto-build workflow to push image to `uclahs-cds` registry
- Add repo source label to Dockerfile
### Changed
- Make `-t` optional, default to `file-input`
- Explicitly set python version to `3.10`
### Fixed

---

## [3.0.0] - 2022-08-03
### Updated
- Updated bl-base to 1.1.0
- Installed tools using `mamba`

### Added
- Add `bldocker` user and group to Dockerfile
- Add support for mutliple input files

### Changed
- Convert module to Python CLI package; now runs directly from commandline with `validate`.
- Single source package version from \_\_init__.py
- Use `pysam` instead of `samtools` in bam file validation.

### Fixed
- Add handling for valid file types whose validation is not yet implemented.

---

## [2.1.6] - 2021-10-18
### Changed
-  File type detection update to properly detect file type when filename contains multiple .

### Fixed
- Fixed bug with detecting fasta files
