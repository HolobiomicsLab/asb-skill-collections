---
name: installation-troubleshooting
description: Use when when setting up matchms for the first time in a new environment, after upgrading Python or conda, when switching between package managers (pip vs conda), or when distributing matchms to end users to confirm functionality across supported installation channels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - pip
  - conda
  - Python
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# installation-troubleshooting

## Summary

Verify that matchms installs successfully and imports without errors across multiple distribution channels (PyPI and Bioconda). This skill ensures reproducibility and early detection of environment or dependency issues before running analysis workflows.

## When to use

When setting up matchms for the first time in a new environment, after upgrading Python or conda, when switching between package managers (pip vs conda), or when distributing matchms to end users to confirm functionality across supported installation channels.

## When NOT to use

- When matchms is already installed and verified to be working in the current environment; use this skill only when setting up new installations or diagnosing existing failures.
- When testing matchms functionality on specific workflows or data (e.g., importing MS/MS data, running spectral similarity comparisons); this skill only validates package availability, not analysis correctness.
- When customizing or extending matchms (e.g., integrating custom similarity measures); installation troubleshooting does not cover development setup or building from source.

## Inputs

- matchms package identifier (version or 'latest')
- target distribution channel (PyPI or Bioconda)
- Python interpreter version (3.10–3.14)
- system architecture (x86_64 or aarch64/arm64)

## Outputs

- installation status report (success or failure, version installed)
- import test result (no errors or detailed error traceback)
- dependency resolution log (list of packages installed)
- cross-channel verification summary (PyPI vs Bioconda compatibility)

## How to apply

Install matchms from the target distribution channel (PyPI via pip or Bioconda via conda), then immediately attempt to import the package in Python and verify no errors occur. For PyPI installations, use `pip install matchms`; for Bioconda, use `conda install -c bioconda matchms`. After each installation method, run a simple import test (`import matchms`) in a fresh Python interpreter session. Document the installation output (version number, dependencies resolved) and any warnings or errors that appear during import. Compare import success across both channels to identify channel-specific issues. If import fails, check that the Python version is 3.10–3.14 as documented, that virtual environment isolation is used, and that no conflicting dependencies exist from prior installations.

## Related tools

- **pip** (Package manager for PyPI-based installation of matchms)
- **conda** (Package manager for Bioconda-based installation of matchms) — https://github.com/bioconda/bioconda-recipes
- **Python** (Runtime environment for importing and testing matchms package)
- **matchms** (Target package being installed and validated) — https://github.com/matchms/matchms

## Examples

```
pip install matchms && python -c "import matchms; print(matchms.__version__)"
```

## Evaluation signals

- Installation command completes without errors and reports successful package installation with a specific version number.
- Python `import matchms` statement executes without ModuleNotFoundError, ImportError, or dependency resolution errors.
- Same version and import success achieved from both PyPI and Bioconda channels (cross-channel consistency).
- No unresolved or conflicting dependencies reported in pip/conda output; all transitive dependencies resolve to compatible versions.
- Python interpreter version used is documented and confirmed to be within the supported range (3.10–3.14).

## Limitations

- Installation verification does not test functional correctness of matchms (e.g., actual data import or spectral comparison); it only confirms package availability and import.
- Bioconda support is limited to Linux and macOS platforms (x86_64 and aarch64/arm64); Windows users must use PyPI or alternative package managers.
- Virtual environment isolation is recommended but not enforced; if existing dependencies conflict, installation may succeed but import or runtime functionality may fail.
- This skill does not cover custom or development installations (building from source, editable installs via `pip install -e`); those workflows require additional setup and testing.

## Evidence

- [other] Are the documented distribution channels (PyPI and Bioconda) for matchms functional and does the package import successfully after installation from these channels?: "research question: Are the documented distribution channels (PyPI and Bioconda) for matchms functional and does the package import successfully after installation from these channels?"
- [other] Matchms is distributed through PyPI and Bioconda with specific release management procedures.: "Matchms is distributed through multiple channels including PyPI and Bioconda, as referenced in the contributing guidelines which specify procedures for release management and waiting for availability"
- [other] Installation steps: pip/conda install, Python import, verify no errors.: "1. Install matchms from PyPI using pip or equivalent package manager. 2. Import the installed matchms package in Python and verify no import errors occur. 3. Install matchms from Bioconda using conda"
- [readme] Python version prerequisites for matchms installation.: "Prerequisites: Python 3.10 - 3.14, (higher versions should work as well, but are not yet tested systematically)"
- [readme] Bioconda channel supports Linux and macOS with x86_64 and aarch64 architectures.: "The [bioconda channel](https://anaconda.org/bioconda) is a Conda channel providing bioinformatics related packages for **Linux** and **macOS**, supporting both x86_64 and aarch64/arm64 architectures."
