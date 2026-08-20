---
name: python-package-installation-from-source
description: Use when when you need to verify a Python package installs successfully
  from a cloned or local repository, validate that all tests pass after installation,
  or prepare a development environment for contributing to the package.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3363
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - pip
  - biosynfoni
  - pytest
  - black
  - Python
  - metabolabpy
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
- doi: 10.3390/metabo15010048
  title: ''
evidence_spans:
- pip install -e .[dev]
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic
  research
- Python package to process 1D and 2D NMR spectroscopic data
- github.com__ludwigc__metabolabpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  - build: coll_metabolabpy_cq
    doi: 10.3390/metabo15010048
    title: MetaboLabPy
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  - 10.3390/metabo15010048
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-package-installation-from-source

## Summary

Install a Python package directly from its source repository in development mode, with optional dev dependencies, to enable local testing and modification. This skill is essential for validating that a package builds correctly, its test suite passes, and the codebase is functional before contributing or deploying.

## When to use

When you need to verify a Python package installs successfully from a cloned or local repository, validate that all tests pass after installation, or prepare a development environment for contributing to the package. Use this when the package is not yet published to PyPI, you need bleeding-edge changes, or you must confirm the CI/CD test workflow works locally.

## When NOT to use

- Package is already installed from PyPI and you only need to run it (not develop or modify it).
- Repository has no tests or a broken test suite with known failures unrelated to your changes.
- You are in a read-only environment or production deployment (use stable PyPI releases instead).

## Inputs

- Python package source repository (git clone or local directory)
- pyproject.toml or setup.py with dev dependencies defined
- tests/ directory containing pytest test suite

## Outputs

- Installed Python package in editable/development mode
- pytest test report (pass/fail for all tests)
- confirmation that package is importable and functional

## How to apply

Clone or navigate to the package repository root directory. Install the package in development (editable) mode using `pip install -e .[dev]` to load source code directly and include development dependencies (typically pytest, code formatters like black, and linting tools). After installation, run the full test suite using `pytest tests/` to verify all unit tests pass. Check for a GitHub Actions CI workflow badge or CI configuration (e.g., test-biosynfoni.yml) to confirm the expected test targets. Development installation allows you to modify source code and immediately test changes without reinstalling; success is confirmed when all pytest tests pass without errors.

## Related tools

- **pip** (Package manager used to install the package in editable mode with optional dev dependencies via `pip install -e .[dev]`)
- **pytest** (Test runner used to execute the complete test suite on the tests/ directory via `pytest tests/`)
- **black** (Code formatter recommended for formatting source code before committing changes (invoked pre-submission, optional during dev installation)) — https://github.com/psf/black
- **biosynfoni** (Example package demonstrating the skill; provides CI workflow reference and dev dependency structure) — https://github.com/lucinamay/biosynfoni

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pip install exits with status 0 and package appears in site-packages or .eggs (confirm with `pip show <package>` or `python -c 'import <package>'`).
- pytest runs without import errors and discovers all tests in tests/ directory.
- All tests pass with 0 failures, 0 errors (pytest output shows '... passed' with no red X marks).
- Package is importable immediately after install: `python -c 'from biosynfoni import Biosynfoni'` succeeds.
- GitHub Actions CI workflow badge (e.g., Tests badge in README) shows passing status, confirming same test suite passes in CI.

## Limitations

- Development installation requires write access to the repository directory and may conflict with system-wide Python packages if virtual environments are not used.
- No changelog or version history was found in the biosynfoni repository, making it difficult to track which commits or tags correspond to tested versions.
- Platform-specific dependencies (e.g., RDKit compiled binaries) may fail on certain OS/architecture combinations despite successful local installation elsewhere.
- Dev dependencies must be explicitly defined in pyproject.toml or setup.py; if missing or incomplete, tests may fail due to unmet imports.

## Evidence

- [other] Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`.: "Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`."
- [other] Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`.: "Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`."
- [other] The biosynfoni package has a GitHub Actions CI workflow that runs tests, as indicated by the Tests badge displayed in the repository.: "The biosynfoni package has a GitHub Actions CI workflow that runs tests, as indicated by the Tests badge displayed in the repository."
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] You can also run the tests locally with the following command: "You can also run the tests locally with the following command"
- [readme] Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni.: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
