---
name: python-package-environment-setup
description: Use when when you have cloned a Python package repository and need to
  verify that the package installs correctly and its test suite passes locally. This
  is the prerequisite workflow before running pytest or code formatters like black
  on the package source.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3793
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pip
  - pytest
  - black
  license_tier: open
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- PyPI - Python Version
- pip install -e .[dev]
- pytest tests/
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_2_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_2_cq
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

# python-package-environment-setup

## Summary

Install a Python package from a repository in editable (development) mode with optional development dependencies, enabling local execution of the package's test suite and code quality checks. This skill is essential for contributors who need to validate package functionality before submission.

## When to use

When you have cloned a Python package repository and need to verify that the package installs correctly and its test suite passes locally. This is the prerequisite workflow before running pytest or code formatters like black on the package source.

## When NOT to use

- When you are installing a package for end-user consumption (use `pip install package_name` from PyPI instead)
- When the package does not include a tests/ directory or test suite configuration
- When you do not have write permissions to the repository directory (editable installs require local source modification capability)

## Inputs

- Python repository directory (containing pyproject.toml or setup.py)
- pip package manager
- Python 3.9+ interpreter

## Outputs

- Installed package in editable mode
- Development dependencies (pytest, black, etc.) installed in active environment
- Pytest test suite execution report (pass/fail status for all tests)

## How to apply

Navigate to the package repository root directory. Install the package in editable mode using `pip install -e .[dev]`, which allows you to make changes to the source code without reinstalling and simultaneously installs development dependencies (e.g., pytest, code formatters). After installation, verify setup by running the test suite with `pytest tests/` to confirm all tests pass. The editable installation mode is critical because it symlinks the package source into your Python environment, enabling rapid iteration and validation of changes.

## Related tools

- **pip** (Package manager for installing the package in editable mode with development dependencies specified via extras (e.g., [dev])) — https://pip.pypa.io/
- **pytest** (Test runner for executing the local test suite to validate package installation and functionality) — https://docs.pytest.org/
- **black** (Code formatter applied to verify code style compliance before committing changes) — https://github.com/psf/black
- **Python** (Runtime environment and language in which the package is implemented (3.9+))

## Examples

```
cd lucinamay/biosynfoni && pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pip install -e .[dev] completes without errors and reports successful installation
- pytest tests/ returns a summary showing all tests passed (zero failures, zero errors)
- The package can be imported in the active Python environment without ImportError or ModuleNotFoundError
- Development tools (pytest, black) are available in the environment and can be invoked from the command line
- Code formatting check with black --check {source_file_or_directory} completes without format violations, or black {source_file_or_directory} successfully reformats files in place

## Limitations

- Editable installation requires the source directory to remain accessible; moving or deleting the cloned repository will break the installation
- Installation success depends on all transitive dependencies being available and compatible with the specified Python version (biosynfoni requires Python 3.9+; RDKit is installed as a dependency)
- The test suite may require external data, network access, or specific system libraries not documented in the article or README
- No changelog was found in the biosynfoni repository, limiting visibility into breaking changes or version-specific requirements

## Evidence

- [other] Install the package in editable mode with development dependencies using pip install -e .[dev]: "Install the package in editable mode with development dependencies using pip install -e .[dev]."
- [other] Execute the test suite using pytest tests/ to confirm all tests pass: "Execute the test suite using pytest tests/ to confirm all tests pass."
- [other] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
- [other] Clone or navigate to the biosynfoni repository root directory: "Clone or navigate to the biosynfoni repository root directory."
- [readme] Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni.: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
- [other] Please use `black` to format your code before submitting a pull request: "Please use `black` to format your code before submitting a pull request"
