---
name: package-repository-verification
description: Use when releasing a new version of a Python package to public repositories, when verifying that distribution pipelines are functioning after code changes, or when troubleshooting installation failures reported by users across different platforms (Linux, macOS) or architectures (x86_64, aarch64).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - pip
  - conda
  - Python
  - pytest
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

# package-repository-verification

## Summary

Verify that a scientific software package is correctly distributed and installable across multiple package repositories (PyPI, Bioconda, conda-forge, etc.), and that the installed package imports without errors. This skill ensures reproducibility by validating the integrity of distribution channels before users or downstream workflows depend on them.

## When to use

Apply this skill when releasing a new version of a Python package to public repositories, when verifying that distribution pipelines are functioning after code changes, or when troubleshooting installation failures reported by users across different platforms (Linux, macOS) or architectures (x86_64, aarch64). Trigger this skill during continuous integration/release workflows and before declaring a release 'ready for use'.

## When NOT to use

- Package is intended for distribution only within a private or institutional repository; use internal artifact verification instead.
- Testing during development before code is committed and tagged for release; use local editable installs (`pip install -e .`) first.
- Verifying package functionality or correctness (unit tests, integration tests); this skill only validates availability and importability, not correctness.

## Inputs

- Python package source code (git repository or release tarball)
- Package metadata (setup.py, pyproject.toml, or equivalent)
- List of target distribution channels (e.g., PyPI, Bioconda)
- Target Python version range (e.g., 3.10–3.14)

## Outputs

- Installation success/failure status per channel
- Import verification results (error messages or success confirmation)
- Platform and architecture compatibility matrix (Linux x86_64, macOS arm64, etc.)
- Release readiness report

## How to apply

Install the target package from each documented distribution channel (e.g., PyPI via pip, Bioconda/conda via conda) in isolated virtual environments to avoid dependency conflicts. For each installation method, follow the documented prerequisites (e.g., Python 3.10–3.14 for matchms) and platform-specific instructions. After each installation, explicitly import the package in Python and verify no import errors or missing dependencies occur. Document the installation success status, import verification results, and any platform-specific observations. This approach validates that both the package metadata and binaries are correctly staged in each repository.

## Related tools

- **pip** (Package installer for PyPI distributions; used to install the package from PyPI repositories)
- **conda** (Package manager for Bioconda and conda-forge distributions; used to install the package from Bioconda channel)
- **Python** (Runtime environment; used to import and verify successful package loading)
- **pytest** (Test framework; optionally used to run existing tests after installation to verify package integrity) — https://github.com/matchms/matchms

## Examples

```
pip install matchms && python -c 'import matchms; print(matchms.__version__)' && conda install -c bioconda matchms && python -c 'import matchms; print(matchms.__version__)'
```

## Evaluation signals

- Installation completes without errors or unresolved dependency warnings for each channel (PyPI, Bioconda)
- Python import statement (e.g., `import matchms`) executes without ImportError, ModuleNotFoundError, or DLL load errors
- Package version matches the intended release version when queried (e.g., `matchms.__version__`)
- Installation succeeds on documented platform/architecture combinations (Linux x86_64, macOS arm64, etc.)
- Existing test suite (if present) passes after installation from each channel

## Limitations

- Verification timing lag: a new release on PyPI may be immediately available, but Bioconda builds are asynchronous and can take hours or days. The Contributing Guidelines note: 'Wait until new release is also on Bioconda via a automatically created PR'.
- Platform coverage: Bioconda officially supports Linux and macOS (x86_64 and aarch64); Windows users must use PyPI. This skill cannot fully validate Windows distribution without separate Windows infrastructure.
- Transitive dependency failures: installation may succeed but import may fail if an upstream dependency (e.g., a C extension or system library) is unavailable in the user's environment. This skill verifies only the immediate package, not the full dependency graph.
- Architecture-specific binaries: pre-built wheels may not exist for all Python versions or architectures, falling back to source builds which may fail if build tools or headers are missing.

## Evidence

- [other] Distribution validation across PyPI and Bioconda: "Matchms is distributed through multiple channels including PyPI and Bioconda, as referenced in the contributing guidelines which specify procedures for release management and waiting for availability"
- [other] Installation from PyPI using pip: "Install matchms from PyPI using pip or equivalent package manager"
- [other] Installation from Bioconda using conda: "Install matchms from Bioconda using conda package manager"
- [other] Import verification after installation: "Import the installed matchms package in Python and verify no import errors occur"
- [readme] Release workflow and Bioconda timing: "Wait until new release is also on Bioconda via a automaticly created PR on bioconda recipes repo"
- [readme] Python version prerequisites: "Python 3.10 - 3.14, (higher versions should work as well, but are not yet tested systematically)"
- [readme] Multiple platform support in Bioconda: "The bioconda channel is a Conda channel providing bioinformatics related packages for Linux and macOS, supporting both x86_64 and aarch64/arm64 architectures"
