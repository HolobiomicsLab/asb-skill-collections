---
name: dependency-management-with-pip
description: Use when when you have cloned a Python package repository and need to verify that the package and its test suite can be installed and executed locally, or when preparing to contribute code changes that must pass the project's test suite before submission.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dependency-management-with-pip

## Summary

Install a Python package and its development dependencies in editable mode using pip, enabling local testing and development workflows. This skill ensures reproducible environment setup for package verification and contribution.

## When to use

When you have cloned a Python package repository and need to verify that the package and its test suite can be installed and executed locally, or when preparing to contribute code changes that must pass the project's test suite before submission.

## When NOT to use

- You are installing a released package for production use (use `pip install biosynfoni` without `-e` flag instead)
- The package repository does not define a [dev] extra or setup.py configuration
- You lack write permissions in the repository directory

## Inputs

- Python package repository root directory (local or cloned)
- pyproject.toml or setup.py with [dev] dependency specification

## Outputs

- Installed package in editable mode
- Installed development dependencies (pytest, black, etc.)
- Environment ready for local test execution

## How to apply

From the repository root directory, run `pip install -e .[dev]` to install the package in editable mode with development dependencies. This approach allows you to modify source code and immediately test changes without reinstalling, while also provisioning tools like pytest needed to run the test suite. After installation, verify success by executing the test suite with `pytest tests/` and confirming all tests pass. The editable mode is essential for development workflows because it creates a link to the source directory rather than copying files, allowing changes to be reflected immediately.

## Related tools

- **pip** (Package installer and dependency resolver; used to fetch and install the package and development dependencies from the repository) — https://pip.pypa.io
- **pytest** (Test runner; invoked after installation to execute the test suite and verify correct package behavior) — https://docs.pytest.org
- **black** (Code formatter; installed as a development dependency and used to format code before submitting pull requests) — https://github.com/psf/black

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pip install command completes without errors and reports successful installation
- Test suite executes without import errors (`pytest tests/` runs to completion)
- All tests pass or expected test results are reported
- Source code modifications are reflected in test behavior without reinstalling
- Development tools (pytest, black) are available in the environment and can be invoked from CLI

## Limitations

- Requires Python 3.9 or later (as specified for biosynfoni)
- Package repository must define development dependencies in a recognized format (e.g., setup.py with extras_require or pyproject.toml with optional-dependencies)
- Editable installs may fail if the repository structure or build system is non-standard
- Development dependencies may introduce transitive dependencies that increase installation footprint or introduce version conflicts

## Evidence

- [other] Install the package in editable mode with development dependencies using pip install -e .[dev]: "Install the package in editable mode with development dependencies using pip install -e .[dev]"
- [other] Execute the test suite using pytest tests/ to confirm all tests pass: "Execute the test suite using pytest tests/ to confirm all tests pass"
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [readme] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
- [readme] Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni.: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
