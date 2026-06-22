---
name: pipeline-prerequisite-checking
description: Use when before launching the DaDIA metabolomics pipeline or any multi-package workflow, when you have an R environment with potentially mixed or unknown package versions and need to confirm that R ≥4.0, XCMS ≥3.11.4, metaMS ≥1.25.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - R
  - XCMS
  - metaMS
  - DaDIA
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

# pipeline-prerequisite-checking

## Summary

Validate software dependencies and version requirements before executing a scientific pipeline, ensuring all critical tools meet minimum thresholds to prevent runtime failures. This skill reconstructs environment prerequisites through systematic version extraction, semantic comparison, and structured reporting.

## When to use

Before launching the DaDIA metabolomics pipeline or any multi-package workflow, when you have an R environment with potentially mixed or unknown package versions and need to confirm that R ≥4.0, XCMS ≥3.11.4, metaMS ≥1.25.1, and all other dependencies are current before processing DIA mzXML files.

## When NOT to use

- When the pipeline has already begun executing (prerequisite checks must run before workflow starts, not mid-execution).
- If you only need to check R version in isolation without verifying dependent packages; use lightweight version checks instead.
- When working with a pre-validated or containerized environment (Docker/Conda lock file) where versions are already guaranteed.

## Inputs

- R installation with loaded package metadata (version object, XCMS package, metaMS package)
- System environment or .libPaths() pointing to installed R packages

## Outputs

- Structured validation report (JSON or text) with per-package version status
- Overall pipeline-ready boolean flag (TRUE/FALSE)
- Pass/fail status for R, XCMS, and metaMS individual checks
- Execution allow/reject decision

## How to apply

Execute four sequential checks in the R environment: (1) query the installed R version using version$major and version$minor, verifying major version ≥4 and rejecting execution if not met; (2) load the XCMS package, extract its version string, and parse it using semantic versioning rules to confirm ≥3.11.4; (3) load metaMS, extract its version string, and verify exact or compatible match to version 1.25.1, flagging any mismatch; (4) confirm all other packages are updated to the newest available version. Generate a structured validation report (JSON or text format) that summarizes all version checks with pass/fail status for each dependency and returns an overall pipeline-ready boolean flag. Reject pipeline execution if any critical dependency fails its threshold check.

## Related tools

- **R** (Environment runtime and version control system; must be ≥4.0 for DaDIA compatibility)
- **XCMS** (Metabolomics data processing package; development version 3.11.4 or above required for DaDIA peak detection and alignment)
- **metaMS** (Mass spectrometry metabolite annotation package; version 1.25.1 required for DaDIA compound identification)
- **DaDIA** (Parent pipeline that depends on prerequisite checking before execution) — https://github.com/HuanLab/DaDIA

## Evaluation signals

- R major version integer extracted and compared to threshold ≥4; execution halted if major < 4.
- XCMS version string parsed and semantic version tuple (major, minor, patch) computed; confirmed ≥3.11.4 before proceeding.
- metaMS version string extracted and matched to version 1.25.1; any mismatch flagged in report.
- All three checks aggregated into boolean pipeline-ready flag; flag = TRUE only if all three pass their thresholds.
- Validation report is generated and contains explicit pass/fail status for each of R, XCMS, metaMS, and overall readiness decision.

## Limitations

- The skill validates only the three named critical dependencies (R, XCMS, metaMS) and does not exhaustively check all transitive dependencies or system-level prerequisites (e.g., C libraries, compiler versions).
- metaMS version is checked for exact or compatible match to 1.25.1; minor version drift in other packages may introduce subtle runtime incompatibilities not caught by this check.
- The skill assumes all packages are already installed in the R library path; it does not handle package installation or download failures.

## Evidence

- [readme] R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required: "R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required"
- [intro] Query R version using version$major and version$minor; verify major ≥4 and reject if not: "Query the installed R version using version$major and version$minor; verify that the major version is ≥4 and reject execution if not"
- [intro] Load XCMS, extract version string, parse and compare against ≥3.11.4 using semantic versioning: "Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules"
- [intro] Generate structured validation report with pass/fail status and overall pipeline-ready flag: "Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag"
- [readme] Number of samples must agree with real number of DIA mzXML files in input configuration: "The number of samples in line 38 has to agree with the real number of DIA mzXML files"
