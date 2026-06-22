---
name: computational-environment-configuration
description: Use when at the start of any DaDIA pipeline execution, or whenever you are preparing to run a complex multi-package R workflow on a new system or after updating package managers.
license: CC-BY-4.0
metadata:
  edam_topics: []
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
---

# computational-environment-configuration

## Summary

Validate and document software version dependencies before executing a data processing pipeline, ensuring that R, XCMS, metaMS, and all dependent packages meet minimum thresholds. This skill prevents runtime failures by establishing a reproducible computational environment contract upfront.

## When to use

Apply this skill at the start of any DaDIA pipeline execution, or whenever you are preparing to run a complex multi-package R workflow on a new system or after updating package managers. Use it specifically when you have a set of DIA mzXML files ready for processing and need to guarantee that the computational environment will not fail mid-analysis due to version incompatibilities.

## When NOT to use

- You are running a standalone analysis that does not depend on XCMS, metaMS, or the DaDIA pipeline.
- You have already validated the environment in the current R session and have documented proof that all versions meet requirements.
- Your input data are already processed feature tables or summary statistics, not raw mzXML files that require the full DaDIA dependency stack.

## Inputs

- Current R installation (queried at runtime)
- Installed XCMS package (if present)
- Installed metaMS package (if present)
- System package repository state

## Outputs

- Structured validation report (JSON or text) with per-dependency version check status
- Overall pipeline-ready boolean flag
- Pass/fail status for R version check
- Pass/fail status for XCMS version check
- Pass/fail status for metaMS version check

## How to apply

Execute a structured four-step validation workflow: (1) Query the installed R version using version$major and version$minor; reject pipeline execution if the major version is below 4. (2) Load the XCMS package, extract its version string, and compare against the minimum requirement (≥3.11.4) using semantic versioning rules; fail if below threshold. (3) Load the metaMS package and extract its version string; verify exact or compatible match to version 1.25.1 and flag any mismatch. (4) Generate a structured validation report (JSON or text format) that summarizes all three version checks with individual pass/fail status for each dependency and an overall pipeline-ready boolean flag. The rationale is that mismatched versions can silently alter algorithm behavior or cause load-time errors; documenting this contract ensures transparency and reproducibility.

## Related tools

- **R** (Runtime environment and version query engine; minimum version 4.0 required)
- **XCMS** (Mass spectrometry data processing package; minimum development version 3.11.4 required)
- **metaMS** (Metabolomics data analysis package; exact version 1.25.1 required)
- **DaDIA** (Data-dependent acquisition pipeline that orchestrates XCMS and metaMS; subject to validated environment) — github.com/HuanLab/DaDIA

## Evaluation signals

- All three version checks (R, XCMS, metaMS) complete without errors or exceptions.
- The overall pipeline-ready flag is true; if false, the specific failing dependency is clearly identified.
- The validation report is machine-readable (JSON or structured text) and can be version-controlled or logged for audit.
- Subsequent DaDIA pipeline execution succeeds without version-related warnings or silent algorithmic changes.
- The number of samples declared in line 38 of the DaDIA configuration matches the count of real DIA mzXML files in the input directory.

## Limitations

- This skill only validates declared version thresholds; it does not detect transitive dependency conflicts or missing optional packages.
- Exact version matching for metaMS (1.25.1) may be overly strict if newer patch versions are backward-compatible; compatibility rules are not documented.
- The skill does not validate R library paths, disk space, memory availability, or other environmental factors that could cause runtime failure.
- If all other packages are updated to newest available versions as recommended, there is no explicit check that these newer versions remain compatible with the specified XCMS and metaMS versions.

## Evidence

- [readme] R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required; all other packages should be updated to the newest available version.: "R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required; all other packages should be updated to the newest available version."
- [other] Query the installed R version using version$major and version$minor; verify that the major version is ≥4 and reject execution if not.: "Query the installed R version using version$major and version$minor; verify that the major version is ≥4 and reject execution if not."
- [other] Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules; fail if below threshold.: "Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules; fail if below threshold."
- [other] Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag.: "Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag."
- [readme] The number of samples in line 38 has to agree with the real number of DIA mzXML files: "The number of samples in line 38 has to agree with the real number of DIA mzXML files"
