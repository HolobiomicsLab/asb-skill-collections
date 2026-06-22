---
name: distribution-channel-validation
description: 'Use when when preparing a software release, testing contribution workflows, or auditing package availability: verify that matchms can be installed and imported successfully from all advertised distribution channels (PyPI and Bioconda) to confirm the package metadata, dependencies, and entry points.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - matchms
  - pip
  - conda
  - bioconda-recipes
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
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

# distribution-channel-validation

## Summary

Verify that a software package is functional and correctly importable across its documented distribution channels (e.g., PyPI, Bioconda). This skill ensures reproducibility and accessibility by confirming installation and import success on each declared distribution platform.

## When to use

When preparing a software release, testing contribution workflows, or auditing package availability: verify that matchms can be installed and imported successfully from all advertised distribution channels (PyPI and Bioconda) to confirm the package metadata, dependencies, and entry points are correct across platforms before users encounter installation or import failures.

## When NOT to use

- When validating a package that has not yet been released or tagged; distribution channels reflect published versions only.
- When testing internal development branches or unreleased features; use local editable installs (`pip install -e .`) instead.
- When the goal is to validate functionality of the installed package itself (e.g., running the full test suite); this skill only checks installation and basic import.

## Inputs

- distribution channel URLs or package identifiers (e.g., 'matchms' on PyPI, 'bioconda/matchms')
- target Python version(s) (3.10–3.14 as documented)
- package manager(s) available (pip, conda)

## Outputs

- installation success/failure status per channel
- import test results (pass/fail, error messages if any)
- documentation of environment details (OS, Python version, package version installed)

## How to apply

Install matchms from each documented distribution channel using the appropriate package manager (pip for PyPI, conda for Bioconda). After each installation, run a Python import test to confirm the package loads without errors and exposes the expected public API. Document the installation success status and any error messages for each channel and platform combination. This validation should be performed in a fresh virtual environment to avoid dependency conflicts. Cross-reference against the contributing guidelines to confirm release procedures have been followed (e.g., version bumping, waiting for automatic Bioconda PR approval) before declaring the distribution complete.

## Related tools

- **pip** (Package installer for PyPI distribution channel; installs matchms and its declared dependencies) — https://pip.pypa.io
- **conda** (Package manager for Bioconda distribution channel; installs matchms from conda-forge/bioconda with pre-built binaries) — https://conda.io
- **matchms** (The package under validation; imported after installation to verify correct loading) — https://github.com/matchms/matchms
- **bioconda-recipes** (Repository hosting the Bioconda recipe and automated build/release pipeline; referenced in release process to confirm package availability) — https://github.com/bioconda/bioconda-recipes

## Examples

```
pip install matchms && python -c "import matchms; print(matchms.__version__)" && conda install -c bioconda matchms && python -c "import matchms; print('Import successful')"
```

## Evaluation signals

- Installation from PyPI via `pip install matchms` completes without errors and reports successful package installation.
- Installation from Bioconda via `conda install -c bioconda matchms` completes without errors and resolves all dependencies.
- Python statement `import matchms` executes without ImportError, AttributeError, or missing module exceptions.
- Public API is accessible: `matchms.Spectrum`, `matchms.Scores`, or other documented classes/functions can be imported and instantiated.
- Installed version matches the intended release tag when queried (e.g., `matchms.__version__` or `pip show matchms | grep Version`).

## Limitations

- This skill validates installation and import only; it does not verify that all functionality works correctly or that tests pass. Separate test suites (pytest) should be used to validate behavior.
- Distribution channels may have different update latencies; Bioconda availability may lag PyPI by hours or days due to automated PR and build workflows, as documented in the contributing guidelines.
- Platform coverage may vary: Bioconda officially supports Linux and macOS (x86_64 and aarch64/arm64); Windows users must use PyPI. This skill must be executed on each target platform.
- Virtual environment isolation is required to avoid false positives from pre-installed dependencies or conflicting packages in the system environment.

## Evidence

- [other] distribution channels (PyPI and Bioconda): "Matchms is distributed through multiple channels including PyPI and Bioconda, as referenced in the contributing guidelines which specify procedures for release management and waiting for availability"
- [other] installation and import verification: "Wait until new release is also on Bioconda via a automaticly created PR on bioconda recipes repo"
- [readme] PyPI and pip installation: "Installation: Prerequisites: Python 3.10 - 3.14, (higher versions should work as well, but are not yet tested systematically)"
- [readme] Bioconda channel and conda package manager: "The bioconda channel is a Conda channel providing bioinformatics related packages for Linux and macOS, supporting both x86_64 and aarch64/arm64 architectures."
- [intro] matchms versatility and imports: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data"
