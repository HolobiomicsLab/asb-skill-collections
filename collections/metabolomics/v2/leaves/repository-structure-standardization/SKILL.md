---
name: repository-structure-standardization
description: Use when a scientific Python package is being moved to a new GitHub organization
  with different structural conventions (e.g., from a personal lab account to a community-led
  organization like metabolomics-cloud or scverse).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - Python setuptools
  - pip
  - GitHub Actions
  - pytest or unittest
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Repository Structure Standardization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Audit and refactor a scientific Python package to conform to organizational standards (configuration files, module naming, CI/CD workflows, metadata) and verify correct installation and functionality in its new location. This skill ensures reproducibility and maintainability when relocating codebases across GitHub organizations.

## When to use

A scientific Python package is being moved to a new GitHub organization with different structural conventions (e.g., from a personal lab account to a community-led organization like metabolomics-cloud or scverse). You need to verify that the relocated package installs cleanly and executes core functionality without errors in its new environment.

## When NOT to use

- The package is a single-file script or does not follow setuptools conventions — structured refactoring may not be necessary.
- The target organization has no published structural standards — standardization requires a clear target specification.
- The package has external dependencies that are incompatible with the target organization's Python or dependency versions.

## Inputs

- Python package source code (setup.py, pyproject.toml, requirements.txt)
- CI/CD workflow definitions (.github/workflows)
- README and documentation files
- Unit and integration test suites
- Representative input datasets for functional validation

## Outputs

- Migrated repository under target GitHub organization
- Updated configuration files (setup.py, pyproject.toml, .github workflows)
- Installation and functional test reports
- Migration report documenting conformance changes

## How to apply

Begin by cloning the current repository and auditing its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against the target organization's standards. Next, adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to the new organization's conventions. Create a new repository under the target organization with the migrated codebase and updated configuration. Run installation tests in a clean virtual environment using `pip install` to verify the package builds without errors. Execute core functionality tests (e.g., loading representative input files and running main analysis workflows) on actual or representative data to confirm runtime correctness. Finally, validate that all unit and integration tests pass and generate a migration report documenting conformance changes and verification results.

## Related tools

- **Python setuptools** (Defines package metadata, dependencies, and installation configuration in setup.py or pyproject.toml)
- **pip** (Tests package installation in a clean environment to verify build correctness)
- **GitHub Actions** (CI/CD workflows (.github/workflows) updated to conform to organization standards) — https://github.com/metabolomics-cloud/mummichog
- **pytest or unittest** (Validates that all tests pass after migration)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Package installs without errors in a fresh virtual environment using `pip install`.
- All unit and integration tests pass in the new repository location.
- Core workflows execute successfully on representative metabolomics data (e.g., feature table input, functional prediction output).
- Configuration files (setup.py, pyproject.toml, .github workflows) match target organization conventions.
- Migration report documents all structural and metadata changes with no undocumented deviations.

## Limitations

- Documentation does not specify which metabolomics-cloud organization standards were used as the migration target — standards vary by organization.
- Package builds may succeed but runtime failures can occur if dependencies have unspecified version requirements or platform-specific incompatibilities.
- The README does not detail how to handle compound identifier translation modules that may need lookup or cross-referencing during model migration.

## Evidence

- [other] Audit and adaptation workflow: "Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud"
- [readme] Migration target and rationale: "Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/"
- [other] Installation verification: "Run installation tests in a clean environment using pip install to verify the package builds without errors."
- [other] Functional validation on representative data: "Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data."
- [other] Test verification and reporting: "Validate that all tests pass and generate a migration report documenting conformance changes and verification results."
