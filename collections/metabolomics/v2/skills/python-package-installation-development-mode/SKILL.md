---
name: python-package-installation-development-mode
description: Use when when you have cloned a Python package repository locally and need to test code changes, run the package's test suite, or contribute to development without reinstalling the package after each modification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3795
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pip
  - pytest
  - black
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- PyPI - Python Version
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_cq
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

# python-package-installation-development-mode

## Summary

Install a Python package in editable/development mode using pip with optional development dependencies, enabling local code changes to be reflected immediately without reinstallation. This is essential for contributing to or testing a package during active development.

## When to use

When you have cloned a Python package repository locally and need to test code changes, run the package's test suite, or contribute to development without reinstalling the package after each modification. Use this when the package offers a [dev] or similar extras group that bundles testing and formatting dependencies.

## When NOT to use

- The package is already installed globally or in a virtual environment and you do not plan to modify its source code.
- You are installing a package for end-user or production use; standard installation (`pip install package_name`) is more appropriate.
- The package repository does not have a setup.py, pyproject.toml, or equivalent packaging configuration.

## Inputs

- Local cloned git repository root directory
- Package source code with setup.py or pyproject.toml defining package metadata and optional dependency groups

## Outputs

- Installed package linked to the local repository (editable mode)
- Development dependencies (pytest, black, linters, etc.) installed in the active Python environment

## How to apply

Navigate to the root directory of the cloned package repository. Run `pip install -e .[dev]` (or the appropriate extras group name specified in the package's setup.py or pyproject.toml). The `-e` flag installs the package in editable mode, meaning the package is linked to the source directory rather than copied to site-packages; the `[dev]` suffix installs additional development tools (e.g., pytest, black, or other test/lint dependencies). Verify installation by importing the package in Python or checking `pip list`. This setup enables you to modify source code and immediately run tests or other workflows without reinstalling.

## Related tools

- **pip** (Package installer; used to fetch and install the package and its dependencies in editable mode with the -e flag and optional extras groups) — https://pip.pypa.io/
- **pytest** (Test runner; installed as part of the [dev] extras to validate the package's test suite after development-mode installation) — https://github.com/pytest-dev/pytest
- **black** (Code formatter; included in [dev] extras to enforce consistent code style before submitting pull requests) — https://github.com/psf/black

## Examples

```
pip install -e .[dev]
```

## Evaluation signals

- Package import succeeds in Python without raising ModuleNotFoundError after installation.
- Running `pip list` shows the package listed with location pointing to the cloned repository directory, not site-packages.
- Modifications to source code (e.g., adding a debug print statement) take effect immediately when re-importing or re-running the code without reinstalling.
- Development dependencies (pytest, black, etc.) are available; e.g., `pytest --version` and `black --version` both return version strings.
- Full test suite runs successfully with `pytest tests/` and reports no import or dependency errors.

## Limitations

- Editable installs are most reliable on Unix-like systems (Linux, macOS); behavior on Windows with certain package configurations may vary.
- If the package's setup.py or pyproject.toml does not define a [dev] or equivalent extras group, this skill cannot provision development dependencies and requires manual installation of testing and linting tools.
- Changes to setup.py or pyproject.toml (e.g., adding new dependencies) may require reinstalling the package for changes to take effect.

## Evidence

- [other] Install the package in editable/development mode using pip with the dev extras (pip install -e .[dev]).: "Install the package in editable/development mode using pip with the dev extras (pip install -e .[dev])"
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] Please use `black` to format your code before submitting a pull request: "Please use `black` to format your code before submitting a pull request"
