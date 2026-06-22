---
name: python-package-installation-and-management
description: Use when when you need to validate that a Python package (or update to it) is accessible to end users through official distribution channels, or when you are preparing a release and need to confirm that installation from PyPI and/or Bioconda does not introduce import failures or missing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - Python
  - pip
  - conda
  - bioconda-recipes
  - poetry
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- Matchms is a versatile open-source Python package
- Verify new release is on [PyPi](https://pypi.org/project/matchms/#history)
- Wait until new release is also on Bioconda (https://anaconda.org/bioconda/matchms)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# Python Package Installation and Management

## Summary

Verify that a Python package is correctly distributed across multiple channels (PyPI, Bioconda) and can be successfully installed and imported without errors. This skill ensures reproducibility of package availability and functional integrity across standard distribution platforms.

## When to use

When you need to validate that a Python package (or update to it) is accessible to end users through official distribution channels, or when you are preparing a release and need to confirm that installation from PyPI and/or Bioconda does not introduce import failures or missing dependencies.

## When NOT to use

- When the package is still in pre-release development and has not been formally versioned or tagged.
- When testing custom local editable installs (e.g., `pip install -e .`) rather than published distributions.
- When the goal is to test internal package functionality or unit tests (use pytest or equivalent; this skill only validates distribution and import).

## Inputs

- Package name and version (e.g., 'matchms>=0.18.0')
- Supported distribution channel identifiers (PyPI, Bioconda)
- Python interpreter (version 3.10 or higher)
- Virtual environment or conda environment (optional but recommended)

## Outputs

- Installation success/failure status per channel
- Import success confirmation (no traceback)
- List of Python versions and platforms tested
- Documentation or report of installation and import validation

## How to apply

Install the target package from each supported distribution channel (PyPI via pip, and Bioconda via conda) in isolated environments or virtual environments. After each installation, attempt to import the package in Python and verify that no import errors or missing dependency exceptions occur. Document the installation status, Python version tested, and any platform-specific observations (e.g., Linux, macOS, Windows; x86_64 vs. aarch64). Test across Python versions 3.10–3.14 if possible, as matchms specifies support for this range. If the package is newly released, wait for availability on Bioconda through automated recipe PRs before final validation.

## Related tools

- **pip** (Package installer for PyPI distributions; used to install matchms from PyPI package index) — https://pypi.org/project/matchms/
- **conda** (Package and environment manager for Bioconda distributions; used to install matchms from bioconda channel) — https://anaconda.org/bioconda/matchms
- **Python** (Runtime interpreter for importing and verifying installed package functionality)
- **bioconda-recipes** (Automated recipe repository for building and distributing matchms on Bioconda) — https://github.com/bioconda/bioconda-recipes
- **poetry** (Version management and release preparation tool; used to bump package version before distribution)

## Examples

```
pip install matchms && python -c "import matchms; print(matchms.__version__)" && conda install -c bioconda matchms && python -c "import matchms; print('Bioconda installation successful')"
```

## Evaluation signals

- Installation command completes without non-zero exit code (pip install and conda install both succeed).
- Python import statement (`import matchms`) executes without ImportError, ModuleNotFoundError, or other exception.
- Package version matches the intended release version when queried (e.g., `matchms.__version__`).
- Installation is confirmed to work on at least two different platforms (e.g., Linux and macOS) and architectures (x86_64 and aarch64) if supported by Bioconda.
- No warnings about unmet dependencies or version conflicts appear during or after installation.

## Limitations

- Bioconda releases may lag behind PyPI; automated PRs on bioconda-recipes must be merged and built before the package is fully available on the Bioconda channel.
- Platform and architecture support is limited: Bioconda provides packages for Linux and macOS (x86_64 and aarch64/arm64) but not Windows.
- Testing is recommended across multiple Python versions (3.10–3.14) but may be time-intensive; the article notes that higher versions 'should work as well, but are not yet tested systematically'.
- Virtual environment isolation is strongly recommended but not enforced; installations without isolation may mask dependency or system-level conflicts.

## Evidence

- [other] Installation from PyPI and Bioconda channels: "Matchms is distributed through multiple channels including PyPI and Bioconda, as referenced in the contributing guidelines which specify procedures for release management and waiting for availability"
- [other] Import verification after installation: "Import the installed matchms package in Python and verify no import errors occur."
- [readme] Supported Python versions for installation: "Python 3.10 - 3.14, (higher versions should work as well, but are not yet tested systematically)"
- [readme] Distribution channels and badges: "Conda Badge and Pypi Badge showing the package is available on both anaconda.org/bioconda/matchms and pypi.org/project/matchms/"
- [other] Bioconda automation and PRs: "Wait until new release is also on Bioconda via a automaticly created PR on bioconda recipes repo"
