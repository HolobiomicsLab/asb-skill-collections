---
name: python-package-migration-and-refactoring
description: Use when you have a mature Python package (e.g., Mummichog 2.x) that
  needs to be relocated to a new GitHub organization (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Python setuptools / pip
  - GitHub Actions (CI/CD workflows)
  - pytest or equivalent test framework
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1003123
  title: mummichog
evidence_spans:
- Mummichog is a Python program for analyzing data from high throughput, untargeted
  metabolomics
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

# Python package migration and refactoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Migrate a Python package to a new GitHub organization while conforming to organizational standards, verifying installation and functionality in the new location. This skill ensures that relocated packages maintain code integrity, dependency correctness, and runtime behavior after structural and configuration changes.

## When to use

You have a mature Python package (e.g., Mummichog 2.x) that needs to be relocated to a new GitHub organization (e.g., metabolomics-cloud) and you need to adapt its structure, metadata, and CI/CD workflows to match the target organization's conventions while confirming that the package installs and runs correctly from its new home.

## When NOT to use

- The source package has undocumented external dependencies or non-standard configuration that cannot be audited before migration.
- The target organization's standards documentation is unavailable or in flux.
- The package has critical breaking changes scheduled that are incompatible with the new organization's supported Python versions or dependency trees.

## Inputs

- Source Python package repository with setup.py, pyproject.toml, requirements.txt
- Organization standards documentation (naming conventions, structure templates, CI/CD patterns)
- Existing test suite and representative input datasets
- .github workflow configuration files

## Outputs

- New repository in target organization with migrated codebase
- Updated package metadata and configuration files conforming to organizational standards
- Test results confirming successful installation and runtime functionality
- Migration report documenting conformance changes and verification results

## How to apply

Begin by cloning the current repository and auditing its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against the target organization's standards. Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to the new organization's conventions. Create a new repository under the target organization with the migrated codebase and updated configuration. Run installation tests in a clean environment using `pip install` to verify the package builds without errors. Execute core functionality tests (e.g., loading feature tables and running primary analysis workflows) on representative datasets to confirm runtime correctness. Finally, validate that all existing tests pass and generate a migration report documenting conformance changes and verification results.

## Related tools

- **Python setuptools / pip** (Package building, installation verification, and dependency resolution in clean environments)
- **GitHub Actions (CI/CD workflows)** (Automated testing and validation of package installation and functionality post-migration) — https://github.com/metabolomics-cloud/mummichog
- **pytest or equivalent test framework** (Execution of core functionality tests on representative metabolomics data)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Package builds without errors when installed from clean environment using `pip install` from the new repository URL.
- All existing unit tests pass in the migrated repository with no failures or new warnings.
- Core functionality (e.g., loading feature tables with m/z, rtime, p-value columns and running pathway prediction) executes successfully on representative test datasets without runtime errors.
- Configuration files (setup.py, pyproject.toml, .github/workflows) conform structurally and semantically to target organization conventions as documented.
- Package metadata (name, version, author, dependencies) is correctly reflected in package imports and distribution metadata post-installation.

## Limitations

- The provided documentation does not contain explicit verification that the relocated Mummichog package installs and runs correctly from its new location in metabolomics-cloud, requiring hands-on testing.
- Compound formula handling and model translation workflows may require bespoke validation if the metabolic model format or chemical database references change during migration.
- Backward compatibility with user-supplied annotation formats and optional metabolic models must be tested explicitly; the skill does not address breaking changes in input/output schemas.

## Evidence

- [other] The Mummichog project has been moved to the new metabolomics-cloud GitHub organization, but the provided documentation does not contain verification that the relocated package installs and runs correctly from its new home.: "The Mummichog project has been moved to the new metabolomics-cloud GitHub organization, but the provided documentation does not contain verification that the relocated package installs and runs"
- [other] 1. Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud organization standards. 2. Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to metabolomics-cloud conventions. 3. Create a new repository under metabolomics-cloud/mummichog with the migrated codebase and updated configuration. 4. Run installation tests in a clean environment using pip install to verify the package builds without errors. 5. Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data. 6. Validate that all tests pass and generate a migration report documenting conformance changes and verification results.: "Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud"
- [readme] Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/: "Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/"
- [readme] Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics. It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics. It leverages the organization of metabolic networks to predict functional activity directly from"
