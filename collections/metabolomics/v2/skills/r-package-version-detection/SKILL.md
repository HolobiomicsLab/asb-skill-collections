---
name: r-package-version-detection
description: Use when before launching the DaDIA metabolomics pipeline or any analysis
  that requires specific R package versions. Apply this skill when you have access
  to an R environment and need to verify that R ≥4.0, XCMS ≥3.11.4, and metaMS ≥1.25.1
  are installed and compatible.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - R
  - XCMS
  - metaMS
  - DaDIA
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# r-package-version-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Programmatically detect and validate the installed versions of R and critical R packages (XCMS, metaMS) against minimum version thresholds before executing a dependent analysis pipeline. This skill ensures pipeline readiness by preventing execution when dependencies are unmet.

## When to use

Before launching the DaDIA metabolomics pipeline or any analysis that requires specific R package versions. Apply this skill when you have access to an R environment and need to verify that R ≥4.0, XCMS ≥3.11.4, and metaMS ≥1.25.1 are installed and compatible.

## When NOT to use

- When the R environment or required packages have not yet been installed—use package installation skill first.
- When you only need to run a subset of the DaDIA pipeline that does not depend on all three packages (verify which packages your specific workflow requires before applying this blanket check).

## Inputs

- R runtime environment with installed packages (XCMS, metaMS)
- Semantic version strings extracted from R package metadata

## Outputs

- Structured validation report (JSON or text format) with per-package pass/fail status
- Overall pipeline-ready boolean flag
- Rejection signal if any dependency fails threshold

## How to apply

Query the installed R version using version$major and version$minor; reject execution if major version is <4. Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules. Load the metaMS package and verify its version matches or is compatible with 1.25.1. Generate a structured validation report (JSON or text format) that summarizes pass/fail status for each of the three dependencies and returns an overall pipeline-ready boolean flag. Fail the entire check if any single dependency is below threshold or missing.

## Related tools

- **R** (Runtime and execution environment; version checked via version$major and version$minor)
- **XCMS** (Metabolomics data processing package; minimum version 3.11.4 required and version string extracted and compared semantically)
- **metaMS** (Metabolite identification package; version 1.25.1 required with exact or compatible match verification)
- **DaDIA** (Dependent pipeline that requires all three package versions to be validated before execution) — github.com/HuanLab/DaDIA

## Evaluation signals

- All three dependencies (R, XCMS, metaMS) pass their respective version checks and report pass status in the validation report.
- Overall pipeline-ready flag is TRUE, indicating the environment meets all minimum version requirements.
- Validation report is generated in structured format (JSON or text) with explicit pass/fail status for each dependency.
- Execution is rejected or halted before pipeline launch if any single dependency fails version check.
- Version strings are correctly parsed and compared using semantic versioning rules (e.g., 3.11.5 ≥ 3.11.4 passes; 3.10.0 < 3.11.4 fails).

## Limitations

- Only validates minimum version requirements; does not detect incompatibilities between different packages or with the operating system.
- Does not verify that all other packages are updated to the newest available version, only validates the three primary dependencies.
- Exact match requirement for metaMS version 1.25.1 may be overly strict if minor patches are compatible; no guidance provided on patch-level flexibility.
- Does not verify system-level dependencies (e.g., C++ compilers, library paths) that some R packages may require.

## Evidence

- [intro] DaDIA requires R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1: "DaDIA requires R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1"
- [other] Query the installed R version using version$major and version$minor; verify that the major version is ≥4: "Query the installed R version using version$major and version$minor; verify that the major version is ≥4"
- [other] Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules: "Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules"
- [other] Load the metaMS package and extract its version string; verify exact or compatible match to version 1.25.1; flag any mismatch: "Load the metaMS package and extract its version string; verify exact or compatible match to version 1.25.1; flag any mismatch"
- [other] Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag: "Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag"
- [readme] all other packages should be updated to the newest available version: "all other packages should be updated to the newest available version"
