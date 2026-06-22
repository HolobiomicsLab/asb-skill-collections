---
name: package-dependency-management
description: 'Use when you need to set up a cloned or downloaded scientific Python package for local development, testing, or execution. Specifically, use it when: (1) you have a package repository with a pyproject.toml or setup.py that declares dev dependencies;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3823
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pip
  - biosynfoni
  - pytest
  - black
  - falcon
  - falcon-ms
  - spectrum-utils
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
- doi: 10.1002/rcm.9153
  title: ''
evidence_spans:
- pip install -e .[dev]
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  - 10.1002/rcm.9153
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# package-dependency-management

## Summary

Install and manage Python package dependencies in development mode, ensuring all required tooling and test infrastructure are available for reproducible builds and local validation. This skill is essential when setting up a scientific Python package for development, testing, or reproducible analysis.

## When to use

Apply this skill when you need to set up a cloned or downloaded scientific Python package for local development, testing, or execution. Specifically, use it when: (1) you have a package repository with a pyproject.toml or setup.py that declares dev dependencies; (2) you need to run the full test suite locally before analysis or contribution; (3) you want to ensure all development tools (testing, linting, formatting) are installed alongside the package itself.

## When NOT to use

- When you need only the released/stable version of the package for end-user analysis—use `pip install biosynfoni` instead of editable mode.
- When the package is already installed and all tests have passed in a prior session—reinstalling is redundant unless dependencies have changed.
- When working in a CI/CD environment (GitHub Actions, etc.) that handles dependency installation automatically—check the workflow YAML instead of installing locally.

## Inputs

- Python package repository (with pyproject.toml or setup.py declaring [dev] extras)
- pip package manager
- pytest configuration (pytest.ini or pyproject.toml [tool.pytest.ini_options])

## Outputs

- Installed package in editable mode (symlinked to repository)
- Installed development dependencies (pytest, black, etc.)
- Test suite execution report (stdout/stderr; exit code 0 on success)

## How to apply

Navigate to the package repository root directory and install the package in editable (development) mode using pip with the dev dependency group: `pip install -e .[dev]`. This approach installs the package in-place, allowing live code changes to be reflected immediately, and simultaneously installs all test runners (pytest), formatters (black), and other development dependencies declared in the [dev] extras. Once installed, validate the installation by executing the complete test suite using `pytest tests/` from the repository root. All tests must pass before proceeding with package usage or analysis workflows; any test failures indicate incomplete or incompatible dependencies.

## Related tools

- **pip** (Package installer and dependency resolver; used to install the package and all [dev] dependencies in editable mode via `pip install -e .[dev]`)
- **pytest** (Test runner; executes the test suite declared in tests/ to validate installation and package functionality)
- **black** (Code formatter; installed as part of [dev] dependencies to enforce consistent code style before contribution or release) — https://github.com/psf/black
- **biosynfoni** (The package being installed and tested) — https://github.com/lucinamay/biosynfoni

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pytest exit code is 0 (all tests pass) after running `pytest tests/`
- Package is importable in Python: `from biosynfoni import Biosynfoni` succeeds without ImportError
- Package code changes are immediately reflected in the installed environment (editable mode is active)
- All declared dependencies (RDKit, numpy, etc.) are present and satisfy version constraints
- black formatting check passes on the codebase with no style errors (or `black --check` returns exit code 0)

## Limitations

- Installation requires Python 3.9 or later; earlier Python versions will fail dependency resolution or import.
- RDKit is a compiled dependency that may require system-level chemistry libraries (e.g., boost); installation can fail on systems without appropriate build tools.
- Development mode installation leaves the package tightly coupled to the repository; moving or deleting the repo breaks the installation.
- The [dev] extras group is only available if the package declares it in pyproject.toml or setup.py; packages without dev dependencies will fail with `error: [dev] is not a valid extra` or equivalent.

## Evidence

- [other] Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`: "Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`"
- [other] Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`: "Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`"
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] You can also run the tests locally with the following command: "You can also run the tests locally with the following command"
- [readme] Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni.: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
- [readme] To install the package, you can use pip: pip install biosynfoni: "To install the package, you can use pip: pip install biosynfoni"
