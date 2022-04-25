# Changelog
All notable changes to the PipeVal tool.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
### Updated
- Updated bl-base to 1.1.0
- Installed tools using `mamba`

### Added
- Add `bldocker` user and group to Dockerfile

### Changed
- Convert module to Python CLI package; now runs directly from commandline with `validate`.

---

## [2.1.6] - 2021-10-18
### Changed
-  File type detection update to properly detect file type when filename contains multiple .

### Fixed
- Fixed bug with detecting fasta files
