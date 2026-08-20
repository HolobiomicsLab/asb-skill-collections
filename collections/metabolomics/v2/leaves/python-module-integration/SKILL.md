---
name: python-module-integration
description: Use when when you have developed or obtained a new Python package that
  encapsulates domain-specific computational logic (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3307
  tools:
  - Python
  - pip
  - pytest
  - black
  - biosynfoni
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Python Module Integration

## Summary

Integrate a specialized Python package (such as biosynfoni) into a development workflow by installing it in editable mode, verifying its core functions work on test inputs, and validating the implementation through automated test suites. This skill ensures that domain-specific computational modules are correctly instantiated and produce outputs matching expected structure and dimensionality.

## When to use

When you have developed or obtained a new Python package that encapsulates domain-specific computational logic (e.g., molecular fingerprinting, bioinformatic analysis) and need to verify it functions correctly in your local environment before using it in downstream analysis pipelines or before submitting code for review.

## When NOT to use

- The package is already installed and working in production; editable mode is for development only.
- The package has no automated test suite; skip pytest validation if tests/ directory does not exist or is empty.
- You are installing a third-party package from PyPI for end-user analysis; use standard `pip install` rather than editable mode.

## Inputs

- Python package source tree with setup.py or pyproject.toml
- Test molecule or input object (e.g., RDKit Mol object for chemistry packages)
- Development environment with pip and pytest installed

## Outputs

- Successfully installed editable package in Python environment
- Fixed-length numerical vector or array output from core function
- Passing pytest test suite with full coverage report

## How to apply

First, install the package in editable (development) mode using `pip install -e .[dev]` from the project root; this allows you to modify source code and immediately see changes without reinstalling. Second, locate the core computational function within the package's module structure and execute it on a representative test molecule or input object. Third, verify that the output is a fixed-length numerical vector or array with the expected dimensionality and data type (e.g., for biosynfoni, a count fingerprint array). Finally, run the full test suite using `pytest tests/` to ensure all unit and integration tests pass, confirming the implementation meets the package's specification. Code should be formatted using black before validation to ensure consistency.

## Related tools

- **pip** (Package manager used to install the module in editable development mode and manage dependencies)
- **pytest** (Test runner used to validate that all computational functions pass unit and integration tests)
- **black** (Code formatter applied before committing changes to ensure consistent style across the module) — https://github.com/psf/black
- **biosynfoni** (Example domain-specific module providing biosynformatic molecular fingerprinting for natural product research) — https://github.com/lucinamay/biosynfoni

## Examples

```
pip install -e .[dev] && from biosynfoni import Biosynfoni; from rdkit import Chem; mol = Chem.MolFromSmiles('CC(=O)OC1=CC=CC=C1C(=O)O'); fp = Biosynfoni(mol).fingerprint && pytest tests/
```

## Evaluation signals

- The package installs without errors or dependency conflicts in editable mode via `pip install -e .[dev]`.
- The core computational function executes successfully on a test input and returns an object with the correct type, shape, and dimensionality (e.g., numpy array or count fingerprint).
- All pytest tests pass with exit code 0, confirming no regressions or failures in the implementation.
- Output vectors or arrays match the expected fixed length and numeric data type defined in the package specification.
- Code passes black formatting validation without style violations.

## Limitations

- Editable mode installation requires write access to the source tree; cannot be used in read-only or sandboxed environments.
- Test suite may have incomplete coverage of edge cases; passing pytest does not guarantee correctness on all possible inputs.
- The skill assumes the package has a well-structured test suite; packages without tests cannot be fully validated this way.
- Fingerprint dimensionality and data type are module-specific; this skill does not validate semantic correctness of outputs, only their structure.

## Evidence

- [other] Install the biosynfoni package from the repository and verify fingerprint structure: "Load the biosynfoni package from the repository (lucinamay/biosynfoni) and install it in development mode using pip install -e .[dev]."
- [other] Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation: "Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation."
- [other] Verify the output is a valid fingerprint array matching the expected dimensionality and data type: "Verify the output is a valid fingerprint array matching the expected dimensionality and data type."
- [other] Run pytest tests to validate that all fingerprint computation tests pass successfully: "Run pytest tests/ to validate that all fingerprint computation tests pass successfully."
- [other] Code formatting requirement before pull request submission: "Please use `black` to format your code before submitting a pull request"
- [readme] biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [readme] Command-line and Python API examples for fingerprint generation: "from biosynfoni import Biosynfoni
from rdkit import Chem

smi = <SMILES>
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint"
