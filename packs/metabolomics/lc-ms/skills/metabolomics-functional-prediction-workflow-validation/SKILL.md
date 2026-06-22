---
name: metabolomics-functional-prediction-workflow-validation
description: Use when a Python-based metabolomics analysis package has been relocated to a new GitHub organization (e.g., metabolomics-cloud) and you need to confirm that the migration preserved package integrity, installation, and runtime correctness.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Mummichog 3
  - metDataModel
  - JMS
  - Python 3 virtualenv
  - pytest / unittest
  techniques:
  - LC-MS
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

# metabolomics-functional-prediction-workflow-validation

## Summary

Verify that a metabolomics functional prediction package (specifically Mummichog 3) has been successfully migrated to a new GitHub organization, conforms to organizational standards, and executes core workflows correctly on representative metabolomics datasets. This skill ensures relocated bioinformatics packages remain installable, maintainable, and functionally correct after migration.

## When to use

A Python-based metabolomics analysis package has been relocated to a new GitHub organization (e.g., metabolomics-cloud) and you need to confirm that the migration preserved package integrity, installation, and runtime correctness. Use this skill when: (1) package metadata, CI/CD workflows, and module structures may have changed during relocation; (2) you must verify the package installs cleanly in a fresh environment; (3) you need to confirm core metabolomics functionality (e.g., loading feature tables, running functional prediction) still works on real data after migration.

## When NOT to use

- The package has not yet been moved to a new GitHub organization—use initial setup/first-time organization workflow instead.
- You are performing routine maintenance on a package already established in an organization—use incremental testing/CI workflows instead.
- The input is already a verified, installed package in the target organization—use direct functional analysis workflows instead.

## Inputs

- Current Mummichog 3 codebase (Python package structure)
- Configuration files (setup.py, pyproject.toml, requirements.txt, .github/workflows)
- GitHub repository metadata and CI/CD pipeline definitions
- Representative metabolomics test data (TSV feature tables with m/z, rtime, p-value columns)
- Optional: annotation tables (JSON format) and metabolic models (JSON with pathways, reactions, compounds)

## Outputs

- Migrated repository under target GitHub organization (metabolomics-cloud/mummichog)
- Updated package configuration files conforming to organizational standards
- Installation verification report (pip install logs, dependency resolution)
- Functional prediction workflow execution results (pathway/network analysis JSON output, result.html)
- Migration report documenting conformance changes and verification results
- Passed test suite logs

## How to apply

Begin by cloning the relocated repository and auditing its structure against organizational standards—checking setup.py, pyproject.toml, requirements.txt, and .github workflows for conformance. Adapt package metadata, module naming, documentation, and CI/CD workflows to align with the target organization's conventions (e.g., metabolomics-cloud). Create or verify the new repository under the target organization with updated configuration. Install the package in a clean virtual environment using `pip install` to confirm it builds without errors. Execute representative core workflows (e.g., loading feature tables from TSV with m/z, retention time, and p-value columns, and running functional prediction without requiring metabolite identification) on metabolomics test data to verify runtime correctness. Finally, run the full test suite and document all conformance changes and verification results in a migration report.

## Related tools

- **Mummichog 3** (Core metabolomics functional prediction package being validated; leverages metabolic network organization to predict functional activity from feature tables without metabolite identification) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model for structuring metabolomics annotation from authentic standards and MS/MS; ensures consistent annotation format for Mummichog input)
- **JMS** (Performs annotation on metabolomics datasets; generates annotation tables (JSON format) used as optional input to Mummichog) — https://github.com/shuzhao-li-lab/JMS
- **Python 3 virtualenv** (Isolates package installation testing in a clean environment to verify pip install correctness without external dependencies)
- **pytest / unittest** (Runs core Mummichog test suite to validate functional prediction workflows on representative metabolomics data)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Package successfully installs via `pip install` in a clean virtual environment without dependency resolution errors or missing modules.
- Mummichog main script executes without errors on representative test TSV (e.g., `ineurons_ttest_1127.tsv`) containing feature m/z, retention time, and p-value columns.
- Functional prediction output includes both human-readable results (HTML, result tables) and machine-readable JSON (pathway/network module analysis) in expected formats.
- All configuration files (setup.py, pyproject.toml, requirements.txt, .github/workflows) conform to metabolomics-cloud organization standards and pass linting/schema validation.
- Test suite passes 100%; migration report documents all conformance changes (metadata, module naming, CI/CD workflow updates) with no breaking changes to core API or input/output schema.

## Limitations

- Validation requires representative metabolomics test datasets (feature tables with proper m/z, rtime, p-value columns); incomplete or malformed test data will produce false failures.
- Metabolic models must include compound chemical formulas in neutral (not salt) format for accurate adduct calculation; models lacking formulas require external lookup and translation modules, which may not be available or standardized.
- Compound identifiers in models must align with annotation data; inconsistent or unmapped identifiers will cause failures in pathway matching regardless of code correctness.
- No changelog was found in the provided documentation, so full history of changes during relocation may not be transparent.
- Package includes minimal dependencies by design (per organizational guidelines), which may limit functionality if future extensions require heavier libraries.

## Evidence

- [other] 1. Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud organization standards.: "Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud"
- [other] 4. Run installation tests in a clean environment using pip install to verify the package builds without errors.: "Run installation tests in a clean environment using pip install to verify the package builds without errors"
- [other] 5. Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data.: "Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data"
- [readme] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification"
- [readme] Input: 1. User supplied features with m/z, rtime, p-value from a statistical test.: "User supplied features with m/z, rtime, p-value from a statistical test"
- [readme] Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/: "Project is moved to new organization https://github.com/metabolomics-cloud"
- [readme] Outpout are 1. Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use.: "Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use"
- [readme] If formulas are not provided in a model, we need to look them up via compound identifiers.: "If formulas are not provided in a model, we need to look them up via compound identifiers"
