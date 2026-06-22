---
name: development-environment-setup
description: Use when when you have cloned a Python package repository and need to prepare a working environment for development, debugging, or contribution. Specifically when the package declares dev dependencies in setup.py or pyproject.toml and maintains a pytest test suite in a tests/ directory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3693
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pip
  - biosynfoni
  - pytest
  - black
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# development-environment-setup

## Summary

Install a Python package in development mode with optional dev dependencies, then execute the full test suite to verify functional integrity. This skill is essential for contributors and maintainers who need to validate package behavior before committing changes or releasing updates.

## When to use

When you have cloned a Python package repository and need to prepare a working environment for development, debugging, or contribution. Specifically when the package declares dev dependencies in setup.py or pyproject.toml and maintains a pytest test suite in a tests/ directory.

## When NOT to use

- Package has no pytest test suite or tests/ directory is absent
- You are installing the package for end-user consumption (use `pip install biosynfoni` without `-e` flag instead)
- The package does not declare dev dependencies and you only need to run the main package code

## Inputs

- Python package source repository (cloned locally)
- setup.py or pyproject.toml with [dev] extras defined
- tests/ directory containing pytest test suite

## Outputs

- Editable package installation in the Python environment
- pytest test report (stdout/stderr with test counts and pass/fail status)
- Verified functional package suitable for development or contribution

## How to apply

From the repository root directory, use pip to install the package in editable (development) mode with dev dependencies via `pip install -e .[dev]`. This preserves the source code in place and installs additional testing and formatting tools. Then execute the complete test suite using `pytest tests/` to verify all unit and integration tests pass. Success is indicated by all tests passing without errors or failures, confirming the package is properly installed and all declared functionality works as expected. The pytest output will display test counts and any failures; zero failures indicates correct application.

## Related tools

- **pip** (Package manager for editable installation of package with dev dependencies) — https://pip.pypa.io
- **pytest** (Test runner for executing complete test suite to verify package functionality) — https://docs.pytest.org
- **biosynfoni** (Example package being installed and tested in development mode) — https://github.com/lucinamay/biosynfoni
- **black** (Code formatter optionally installed as dev dependency for code style compliance) — https://github.com/psf/black

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pip install command completes without errors and reports successful editable installation
- pytest discovers and collects all test files in tests/ directory (test count > 0)
- All pytest tests pass with exit code 0 and no FAILED or ERROR markers in output
- Package can be imported and used in Python REPL after installation: `from biosynfoni import Biosynfoni` succeeds
- Running tests multiple times produces consistent pass/fail results (no flakiness)

## Limitations

- Development installation requires writable file system access to the repository root
- Tests may have external dependencies (network, databases, RDKit) that could cause failures unrelated to the package installation itself
- No changelog or version history is formally documented in the biosynfoni repository, making it difficult to track breaking changes across development sessions

## Evidence

- [other] Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`.: "Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`"
- [other] Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`.: "Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`"
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] You can also run the tests locally with the following command: "You can also run the tests locally with the following command"
- [other] The biosynfoni package has a GitHub Actions CI workflow that runs tests, as indicated by the Tests badge displayed in the repository.: "The biosynfoni package has a GitHub Actions CI workflow that runs tests, as indicated by the Tests badge displayed in the repository"
