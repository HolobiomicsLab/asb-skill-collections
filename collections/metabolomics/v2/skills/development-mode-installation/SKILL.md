---
name: development-mode-installation
description: Use when you need to run a local test suite, contribute code changes to a repository, or iterate rapidly on package modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pip
  - pytest
  - black
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# development-mode-installation

## Summary

Install a Python package in editable mode with development dependencies to enable local testing and code contribution workflows. This skill allows developers to modify source code and immediately test changes without reinstalling the package.

## When to use

Apply this skill when you need to run a local test suite, contribute code changes to a repository, or iterate rapidly on package modifications. Specifically, use it before executing pytest tests locally or when the project README instructs 'Run the following command from the root of the project to install the project for development'.

## When NOT to use

- When installing a package for end-user production deployment (use `pip install package_name` instead)
- When the package has not declared a [dev] extras group or development dependencies in its build metadata
- When working in an environment where editable installs are forbidden or unsupported (e.g., restricted container or sandboxed runtime)

## Inputs

- Python package source repository root directory
- pyproject.toml or setup.py with [dev] extras defined

## Outputs

- Editable package installation in site-packages (as symlink)
- Development dependencies (pytest, black, etc.) available in environment
- Test suite executable and passing (pytest tests/ exit code 0)

## How to apply

Navigate to the package repository root directory. Execute `pip install -e .[dev]` to install the package in editable mode with all development dependencies (including test runners and code formatters). The `-e` flag installs the package as a symbolic link to the source directory, allowing source code edits to take effect immediately without reinstallation. The `[dev]` extra installs development-specific dependencies such as pytest and black. After installation, verify by running the test suite with `pytest tests/` to confirm all tests pass and dependencies are correctly configured.

## Related tools

- **pip** (Package manager used to install the package in editable mode with development extras)
- **pytest** (Test runner installed as a development dependency and used to verify successful installation by running the test suite)
- **black** (Code formatter installed as a development dependency to enforce code style before committing changes) — https://github.com/psf/black

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- Command `pip install -e .[dev]` completes without errors or unresolved dependencies
- pytest test suite runs successfully with command `pytest tests/` and all tests pass (exit code 0)
- Source code modifications (e.g., in a .py file) take effect immediately in subsequent test runs without reinstalling
- Development tools (pytest, black) are executable and available in the Python environment (verify with `which pytest` or `pytest --version`)
- The package is listed in `pip freeze` or `pip list` with an editable path indicator (e.g., `-e /path/to/repo` or showing a file:// URL)

## Limitations

- Editable installs work reliably only with packages using modern build backends (setuptools with pyproject.toml); some legacy packages may not support `-e` mode
- Changes to compiled extensions or package metadata (e.g., version strings in __init__.py) may require reinstallation even in editable mode
- Development dependency installation depends on the [dev] extras group being properly defined in the package's build configuration; if missing or misconfigured, pytest and other tools will not be installed

## Evidence

- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] pip install -e .[dev]: "pip install -e .[dev]"
- [other] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
- [other] Please use `black` to format your code before submitting a pull request: "Please use `black` to format your code before submitting a pull request"
- [other] The biosynfoni package includes a pytest test suite located in the tests/ directory that can be executed locally: "The biosynfoni package includes a pytest test suite located in the tests/ directory that can be executed locally"
