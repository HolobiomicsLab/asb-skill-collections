---
name: semantic-version-parsing-comparison
description: Use when before executing a bioinformatics pipeline that depends on multiple
  R packages with strict version constraints (e.g., DaDIA, which requires R ≥4.0,
  XCMS ≥3.11.4, and metaMS =1.25.1).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3391
  tools:
  - R
  - XCMS
  - metaMS
  techniques:
  - mass-spectrometry
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

# semantic-version-parsing-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and compare software package version strings against minimum semantic versioning requirements to validate pipeline dependencies before execution. This skill ensures that all critical packages meet or exceed specified thresholds, preventing downstream failures caused by incompatible or outdated libraries.

## When to use

Before executing a bioinformatics pipeline that depends on multiple R packages with strict version constraints (e.g., DaDIA, which requires R ≥4.0, XCMS ≥3.11.4, and metaMS =1.25.1). Apply this skill when you need to programmatically validate environment readiness rather than relying on manual checks or runtime errors.

## When NOT to use

- Input is a conda/pip lock file or container image manifest — use dedicated dependency managers instead.
- Packages are version-agnostic or have no documented minimum requirements.
- Runtime version mismatches are acceptable (e.g., for exploratory or backward-compatible workflows).

## Inputs

- R environment with loaded packages (R, XCMS, metaMS)
- Minimum version specification document (e.g., README or configuration file)

## Outputs

- Structured validation report (JSON or text format) with per-dependency pass/fail status
- Overall pipeline-ready boolean flag
- Semantic version tuples (major, minor, patch) for each dependency

## How to apply

Extract the installed version string from each required package using language-specific introspection (e.g., `version$major` and `version$minor` in R, or `packageVersion()` for packages). Parse version strings using semantic versioning rules (major.minor.patch), then compare each parsed version against the documented minimum requirement using tuple comparison (e.g., (4, 0, 0) ≥ (3, 11, 4)). For packages with exact version pins (e.g., metaMS 1.25.1), flag any mismatch as a validation failure. Aggregate results into a structured report (JSON or text) with pass/fail status for each dependency and an overall pipeline-ready boolean flag. Reject pipeline execution if any critical dependency fails validation.

## Related tools

- **R** (Runtime environment; provides version introspection via version$major and version$minor; host for package version extraction)
- **XCMS** (Mass spectrometry data processing package; requires Development Version ≥3.11.4 for DaDIA compatibility) — github.com/HuanLab/DaDIA
- **metaMS** (Metabolomics peak annotation package; requires exact or compatible version match to 1.25.1) — github.com/HuanLab/DaDIA

## Examples

```
# R command to validate DaDIA dependencies
if(as.numeric(R.version$major) >= 4 && packageVersion('XCMS') >= '3.11.4' && packageVersion('metaMS') == '1.25.1') { pipeline_ready <- TRUE } else { stop('Dependency validation failed') }
```

## Evaluation signals

- All parsed version tuples satisfy their respective minimum/exact requirements without raising exceptions.
- Overall pipeline-ready flag is TRUE only when all three dependencies (R, XCMS, metaMS) pass validation.
- Version comparison logic correctly handles semantic versioning rules (e.g., 3.11.4 > 3.9.0 even though string '3.9.0' > '3.11.4' lexically).
- Validation report is generated in valid JSON (if format selected) and includes timestamp and environment metadata.
- Pipeline execution is blocked or warned if any dependency fails, with clear messaging indicating which package and threshold were violated.

## Limitations

- Exact version pins (e.g., metaMS 1.25.1) do not account for compatible patch releases or maintenance updates; may reject valid installations.
- Version strings with non-standard formats (e.g., 'devel', 'nightly', Git commit hashes) may not parse correctly using simple semantic versioning rules.
- Does not validate transitive dependencies (e.g., XCMS's own R package dependencies); only checks direct requirements.
- Assumes all packages are available in the current R library path; does not verify package installation completeness.

## Evidence

- [intro] DaDIA requires R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1, with all other packages updated to the newest available version.: "DaDIA requires R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1, with all other packages updated to the newest available version."
- [other] Query the installed R version using version$major and version$minor; verify that the major version is ≥4 and reject execution if not.: "Query the installed R version using version$major and version$minor; verify that the major version is ≥4 and reject execution if not."
- [other] Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules; fail if below threshold.: "Load the XCMS package and extract its version string; parse and compare against the minimum requirement (≥3.11.4) using semantic versioning rules; fail if below threshold."
- [other] Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag.: "Generate a structured validation report (JSON or text format) summarizing all three version checks with pass/fail status for each dependency and an overall pipeline-ready boolean flag."
- [readme] R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required; all other packages should be updated to the newest available version.: "R Version 4.0 or above, XCMS Development Version 3.11.4 or above, and metaMS Version 1.25.1 are required; all other packages should be updated to the newest available version."
