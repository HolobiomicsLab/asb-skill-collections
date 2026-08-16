---
name: ci-cd-workflow-adaptation-to-organization-standards
description: Use when when a Python package is being relocated to a new GitHub organization
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pip
  - GitHub Actions
  - Mummichog 3
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

# CI/CD Workflow Adaptation to Organization Standards

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Audit and migrate a Python package's continuous integration and deployment workflows to conform to an organization's established conventions, ensuring the relocated codebase installs and runs correctly in its new repository home. This skill is essential when moving projects between GitHub organizations or adopting shared CI/CD standards.

## When to use

When a Python package is being relocated to a new GitHub organization (e.g., metabolomics-cloud) that maintains standardized project structures and CI/CD practices, and you need to verify that the migrated package installs cleanly and functions correctly without breaking existing tests or workflows.

## When NOT to use

- Package is remaining in its current organization and no standards migration is required.
- Target organization's standards have not yet been documented or agreed upon.
- The package contains tightly coupled dependencies or hardcoded paths that cannot be relocated without major refactoring.

## Inputs

- Source Python package repository (including setup.py, pyproject.toml, requirements.txt)
- GitHub Actions workflow files (.github/workflows/*.yml)
- Target organization's CI/CD standards documentation
- Existing test suite and test data

## Outputs

- Migrated repository under target organization namespace
- Adapted configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows)
- Clean installation verification report
- Test execution results (passing core functionality tests)
- Migration report documenting conformance changes

## How to apply

First, clone the current package repository and systematically audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, and .github workflows) against the target organization's documented standards. Identify deviations in package metadata, module naming, documentation layout, and CI/CD workflow definitions. Adapt these configuration files to conform to the organization's conventions, then create a new repository under the organization's namespace with the migrated codebase. Run installation tests in a clean Python environment using `pip install` to verify the package builds without errors and all dependencies are correctly declared. Execute core functionality tests—for example, loading feature tables and running functional prediction workflows on representative metabolomics data—to confirm runtime correctness. Finally, validate that all existing tests pass and generate a migration report documenting conformance changes and verification results.

## Related tools

- **Python** (Package implementation and testing language)
- **pip** (Package installer used to verify clean installation from migrated repository)
- **GitHub Actions** (CI/CD platform for which workflows must be adapted to organization standards)
- **Mummichog 3** (Example package undergoing migration; provides concrete test workflows and dependencies) — https://github.com/metabolomics-cloud/mummichog

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Package installs without errors in a clean environment using `pip install` after migration.
- All existing unit and integration tests pass in the new repository.
- Core functionality (e.g., loading feature tables, running functional prediction) executes correctly on representative test data without runtime errors.
- Configuration files (setup.py, pyproject.toml, .github/workflows) conform to organization standards with no deviations flagged in the migration audit.
- Migration report documents all conformance changes made and verifies that no functionality was lost or altered during relocation.

## Limitations

- The provided documentation does not contain verification that the relocated Mummichog package actually installs and runs correctly from its new location; migration must include explicit post-move validation.
- Package metadata and module naming conventions are organization-specific; deviations discovered during audit may require non-trivial refactoring if the package exports public APIs.
- Test data and fixtures may reference absolute paths or external resources that fail when the repository is relocated; these dependencies must be identified and resolved during migration.

## Evidence

- [other] Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud organization standards.: "Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud"
- [other] Create a new repository under metabolomics-cloud/mummichog with the migrated codebase and updated configuration. Run installation tests in a clean environment using pip install to verify the package builds without errors.: "Create a new repository under metabolomics-cloud/mummichog with the migrated codebase and updated configuration. Run installation tests in a clean environment using pip install to verify the package"
- [other] Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data.: "Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data."
- [other] The Mummichog project has been moved to the new metabolomics-cloud GitHub organization, but the provided documentation does not contain verification that the relocated package installs and runs correctly from its new home.: "the provided documentation does not contain verification that the relocated package installs and runs correctly from its new home."
- [readme] Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/: "Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/"
