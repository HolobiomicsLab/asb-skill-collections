---
name: dependency-requirement-validation
description: Use when before launching the DaDIA pipeline or any multi-package R workflow that has strict version constraints. Use this skill when you have access to an R environment and need to confirm that R ≥4.0, XCMS ≥3.11.4, and metaMS ≥1.25.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - XCMS
  - metaMS
  - DaDIA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.0c05022
  title: DaDIA
evidence_spans:
- R Version 4.0 or above
- XCMS Development Version 3.11.4 or above
- metaMS Version 1.25.1
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dadia_cq
    doi: 10.1021/acs.analchem.0c05022
    title: DaDIA
  dedup_kept_from: coll_dadia_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c05022
  all_source_dois:
  - 10.1021/acs.analchem.0c05022
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dependency-requirement-validation

## Summary

Verify that installed software versions meet minimum thresholds before executing a bioinformatics pipeline. This skill systematically checks R, XCMS, and metaMS versions against documented requirements and generates a structured validation report to prevent runtime failures due to incompatible dependencies.

## When to use

Before launching the DaDIA pipeline or any multi-package R workflow that has strict version constraints. Use this skill when you have access to an R environment and need to confirm that R ≥4.0, XCMS ≥3.11.4, and metaMS ≥1.25.1 are installed and compatible before beginning data processing on DIA mzXML files.

## When NOT to use

- Input data is already in processed feature table or quantification matrix format; version validation is only needed before pipeline initialization, not for analyzing existing outputs.
- Using a containerized or pre-built environment (Docker image, conda lock file) where dependency versions are already pinned and immutable.
- Running a different pipeline or tool suite that does not depend on R, XCMS, or metaMS.

## Inputs

- R installation (environment variable $R_HOME or local R binary)
- installed packages: XCMS, metaMS, and all other DaDIA dependencies

## Outputs

- structured validation report (JSON or text) with version check results
- pipeline-ready boolean flag (true if all three dependencies pass; false otherwise)
- detailed per-dependency pass/fail status with version strings

## How to apply

Query the installed R version using version$major and version$minor; reject execution if major version is less than 4. Load the XCMS package and extract its version string; parse and compare against minimum requirement 3.11.4 using semantic versioning rules (comparing major.minor.patch numerically). Load the metaMS package and verify that its version matches 1.25.1 or is compatible with that specification. Generate a structured validation report in JSON or text format that documents pass/fail status for each of the three dependencies and outputs an overall pipeline-ready boolean flag. Rationale: version mismatches cause silent failures or unpredictable behavior in mass spectrometry data processing; early validation prevents wasted compute and confusing downstream errors.

## Related tools

- **R** (runtime environment and version extraction; must be ≥4.0 to execute DaDIA)
- **XCMS** (mass spectrometry data processing package; minimum development version 3.11.4 required for DaDIA compatibility)
- **metaMS** (metabolomics data analysis package; version 1.25.1 required for DaDIA pipeline)
- **DaDIA** (parent pipeline that depends on validated versions of R, XCMS, and metaMS) — https://github.com/HuanLab/DaDIA

## Examples

```
# In R:
version$major >= 4 && packageVersion('XCMS') >= '3.11.4' && packageVersion('metaMS') == '1.25.1'
```

## Evaluation signals

- R version $major ≥ 4 and $minor ≥ 0 (semantic comparison confirms R ≥4.0)
- XCMS version string parses to numeric components; major.minor.patch ≥ 3.11.4 when compared semantically
- metaMS version string exactly matches or is marked compatible with 1.25.1
- Validation report is produced in valid JSON or structured text format with no parsing errors
- Overall pipeline-ready flag is true if and only if all three dependency checks pass; false if any single check fails

## Limitations

- This skill only validates versions; it does not check whether packages are functionally correct or whether system-level dependencies (e.g., compilation toolchains, C libraries) are available.
- Semantic versioning comparison assumes standard major.minor.patch format; non-standard version strings may cause parsing failures.
- The skill does not validate the number of samples or agreement with line 38 configuration; that check is handled separately in the DaDIA setup workflow.
- If metaMS or XCMS are installed from development branches or forks, version strings may not conform to the expected format and validation may produce false negatives.

## Evidence

- [readme] R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required: "R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required"
- [readme] all other packages should be updated to the newest available version: "all other packages should be updated to the newest available version"
- [intro] Query the installed R version using version$major and version$minor; verify that the major version is ≥4: "Query the installed R version using version$major and version$minor; verify that the major version is ≥4"
- [intro] Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules: "Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules"
- [intro] Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag: "Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag"
