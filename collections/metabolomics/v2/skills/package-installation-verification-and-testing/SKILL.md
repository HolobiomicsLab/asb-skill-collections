---
name: package-installation-verification-and-testing
description: Use when a Python package has been relocated to a new repository location, reorganized to conform to new organizational standards (e.g., metabolomics-cloud conventions), or its dependencies, metadata, or CI/CD workflows have been modified.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - Python pip
  - virtualenv
  - mummichog (version 3)
  - pytest or unittest
derived_from:
- doi: 10.1371/journal.pcbi.1003123
  title: mummichog
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mummichog
    doi: 10.1371/journal.pcbi.1003123
    title: mummichog
  dedup_kept_from: coll_mummichog
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1003123
  all_source_dois:
  - 10.1371/journal.pcbi.1003123
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# package-installation-verification-and-testing

## Summary

Verify that a relocated or migrated Python package installs correctly in a clean environment and executes core functionality without errors. This skill bridges codebase migration (e.g., to a new GitHub organization) and production readiness by confirming that all dependencies resolve, build succeeds, and representative workflows run correctly.

## When to use

A Python package has been relocated to a new repository location, reorganized to conform to new organizational standards (e.g., metabolomics-cloud conventions), or its dependencies, metadata, or CI/CD workflows have been modified. Before declaring the migration complete, verify that the package can be installed from scratch and that canonical workflows (e.g., loading a feature table and running functional prediction) produce valid outputs.

## When NOT to use

- The package has not been moved or substantially reorganized; use for initial releases only when establishing a baseline.
- The target environment is not a clean, isolated virtual environment; prior installations or system packages may mask dependency issues.
- Test datasets are not representative of real-world inputs (e.g., too small, missing required columns like m/z or p-value) and cannot validate core workflows.

## Inputs

- Source Python package codebase (mummichog-style: setup.py, pyproject.toml, requirements.txt, module structure)
- Target organization standards documentation (e.g., metabolomics-cloud conventions for repository structure, CI/CD)
- Representative test datasets (e.g., feature table with m/z, retention time, p-values; annotation JSON; metabolic model in JSON format)
- Automated test suite (unit and integration tests)

## Outputs

- Clean installation confirmation (pip install exit code 0, no unresolved dependencies)
- Successful execution of core workflows on test data (feature table → functional prediction)
- Test suite pass/fail report
- Migration report documenting conformance changes and verification results
- Installation and runtime logs (stdout, stderr, build artifacts)

## How to apply

First, audit the source repository structure, setup.py, pyproject.toml, requirements.txt, and .github workflows against target organization standards. Adapt package metadata, module naming, documentation, and CI/CD configurations to conform to those conventions. Create the new repository with the migrated codebase and updated configuration. Install the package in a clean virtual environment using pip install to confirm the build succeeds without errors or missing dependencies. Execute representative core workflows (e.g., loading a feature table with m/z, retention time, and p-values, then running functional prediction against a metabolic model) on test datasets. Validate that all automated tests pass and document all conformance changes and verification outcomes in a migration report.

## Related tools

- **Python pip** (Package manager; installs the migrated package in a clean virtual environment to verify all dependencies resolve and build succeeds.)
- **virtualenv** (Creates an isolated Python environment to test clean installation without interference from system or prior packages.)
- **mummichog (version 3)** (The subject package being verified after migration; provides core functionality (feature table input, functional prediction, metabolic network analysis).) — https://github.com/metabolomics-cloud/mummichog
- **pytest or unittest** (Executes automated test suite to confirm all tests pass post-migration.)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- pip install in a clean virtual environment exits with code 0 and reports 'Successfully installed [package-name]' with all dependencies resolved.
- Core workflow (e.g., `python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .`) completes without traceback or import errors.
- Output files are generated and contain expected data structures (result.html, JSON pathway/network analysis objects, no null or malformed entries).
- All automated tests pass: `pytest` or equivalent test runner reports 0 failures.
- Package metadata (name, version, author, dependencies) matches target organization standards and is correctly read from setup.py or pyproject.toml.

## Limitations

- Installation verification in a clean environment does not guarantee correctness on all downstream platforms or with all optional dependencies; test on representative target systems.
- Core workflow verification requires representative test datasets (feature tables with m/z, retention time, p-value; annotation; metabolic models); absence of such datasets limits scope.
- Migration report does not validate scientific accuracy of results, only that code executes without error; downstream validation against gold-standard outputs is separate.
- Compound identifier alignment and formula lookup (especially for user-supplied models) are manual steps outside this skill; the README notes 'a translation module is needed' but does not automate it.

## Evidence

- [other] Run installation tests in a clean environment using pip install to verify the package builds without errors.: "Run installation tests in a clean environment using pip install to verify the package builds without errors."
- [other] Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data.: "Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data."
- [other] Validate that all tests pass and generate a migration report documenting conformance changes and verification results.: "Validate that all tests pass and generate a migration report documenting conformance changes and verification results."
- [other] Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to metabolomics-cloud conventions.: "Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to metabolomics-cloud conventions."
- [readme] virtualenv env; source env/bin/activate; pip install scipy matplotlib xlsxwriter networkx: "virtualenv env; source env/bin/activate; pip install scipy matplotlib xlsxwriter networkx"
