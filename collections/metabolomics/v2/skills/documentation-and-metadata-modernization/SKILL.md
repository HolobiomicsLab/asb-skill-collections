---
name: documentation-and-metadata-modernization
description: Use when a mature scientific package (e.g., Mummichog 3) is being migrated to a new GitHub organization that enforces standardized project structure, and the current setup.py, pyproject.toml, requirements.txt, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - Python setuptools / pyproject.toml
  - GitHub Actions / .github/workflows
  - virtualenv
  - scverse.org project structure
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

# documentation-and-metadata-modernization

## Summary

Audit and adapt a scientific Python package's metadata, configuration files, and documentation to conform to organizational standards (e.g., metabolomics-cloud conventions) when relocating to a new GitHub organization. This ensures consistent project structure, CI/CD workflows, and installation behavior across a federated codebase.

## When to use

A mature scientific package (e.g., Mummichog 3) is being migrated to a new GitHub organization that enforces standardized project structure, and the current setup.py, pyproject.toml, requirements.txt, .github workflows, and module naming do not yet conform to the target organization's conventions.

## When NOT to use

- The package is a one-off analysis script with no installation infrastructure (setup.py, pyproject.toml) — documentation modernization assumes a distributable package.
- The target organization has not published explicit standards or exemplar projects to audit against — without reference conventions, conformance cannot be assessed.
- The package is already installed and in active use by downstream projects; migration risk may outweigh standardization benefits without a staged rollout plan.

## Inputs

- Current package repository (source code, setup.py, pyproject.toml, requirements.txt, .github/workflows)
- Target organization's standards documentation or exemplar repositories (e.g., scverse.org projects)
- Representative metabolomics test data (feature table TSV, annotation JSON, metabolic model JSON)

## Outputs

- Migrated repository under target organization (e.g., metabolomics-cloud/mummichog)
- Updated package metadata and configuration files conforming to organizational standards
- Installation verification report (pip install success, no build errors)
- Functional verification report (core workflows execute correctly on test data)
- Migration summary documenting all conformance changes and validation results

## How to apply

Begin by cloning the current repository and auditing its structure against the target organization's standards, documenting differences in package metadata, module naming, documentation layout, and CI/CD workflows. Systematically adapt configuration files (setup.py, pyproject.toml, requirements.txt) and .github action workflows to match organizational conventions. Create a new repository under the target organization with the migrated codebase and updated metadata. Verify the migration by running installation tests in a clean environment (e.g., pip install in a virtualenv) to ensure the package builds without errors. Execute core functionality tests on representative data (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness. Finally, validate that all unit tests pass and generate a migration report documenting all conformance changes and verification results.

## Related tools

- **Python setuptools / pyproject.toml** (Define package metadata, dependencies, and build configuration for standardized installation)
- **GitHub Actions / .github/workflows** (Implement organization-standard CI/CD workflows for testing and validation on migration) — https://github.com/metabolomics-cloud/mummichog
- **virtualenv** (Create isolated Python environments to verify clean installation without dependency conflicts)
- **scverse.org project structure** (Reference exemplar for organizing modular scientific Python packages in federated organizations) — https://scverse.org/

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- pip install succeeds in a clean virtualenv without build errors or dependency resolution failures
- Core Mummichog workflows (feature table loading, functional prediction on representative metabolomics data) execute without runtime errors
- All existing unit tests pass in the migrated repository
- Package metadata (name, version, author, dependencies) is consistent across setup.py, pyproject.toml, and README
- Documentation structure and .github workflow files match target organization's exemplar repositories (e.g., scverse.org standards)

## Limitations

- Migration report assumes target organization standards are explicit and documented; ad-hoc or unstated conventions will require manual interpretation.
- Testing may be incomplete if representative metabolomics test data is unavailable; functional verification relies on test dataset representativeness.
- Backward compatibility with v2.7 (mummichog-2.7 branch) is not verified in the migration workflow; deprecated APIs or breaking changes may emerge.
- No changelog was found in the source material; migration changes should be documented explicitly to inform users of v2 → v3 differences.

## Evidence

- [other] Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud organization standards.: "Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud"
- [other] Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to metabolomics-cloud conventions.: "Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to metabolomics-cloud conventions."
- [other] Run installation tests in a clean environment using pip install to verify the package builds without errors.: "Run installation tests in a clean environment using pip install to verify the package builds without errors."
- [other] Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data.: "Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data."
- [readme] Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/: "Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/"
- [readme] Let's keep this as core package, with minimal dependency.: "Let's keep this as core package, with minimal dependency."
