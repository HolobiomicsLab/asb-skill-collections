---
name: relative-mass-defect-window-filtering
description: Use when apply this filter when working with MS-DIAL peak lists (feature tables with m/z, retention time, and intensity) that contain features with anomalous mass defects—particularly when you have prior knowledge of the expected RMD range for your sample type or analytical method, or when you want.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-DIAL
  - MS-FINDER
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
---

# relative-mass-defect-window-filtering

## Summary

Filter LC-MS features by removing those whose relative mass defect (RMD) values fall outside user-defined window bounds. This step removes spurious or chemically implausible features from MS-DIAL peak lists during untargeted metabolomics preprocessing.

## When to use

Apply this filter when working with MS-DIAL peak lists (feature tables with m/z, retention time, and intensity) that contain features with anomalous mass defects—particularly when you have prior knowledge of the expected RMD range for your sample type or analytical method, or when you want to remove features unlikely to represent organic metabolites.

## When NOT to use

- Input data lack MS/MS fragmentation information—MS-CleanR will crash in the first filtering step if data contain only MS1 scans without MS/MS spectra.
- You are working with targeted metabolomics data where features are pre-selected based on known standards—RMD filtering is designed for discovery in untargeted analyses.
- Your data have already been heavily curated or filtered by other preprocessing tools; additional RMD filtering may over-filter and lose true signals.

## Inputs

- MS-DIAL peak list (feature table with m/z, retention time, intensity, sample assignments)
- RMD window bounds (lower and upper threshold values, user-specified)

## Outputs

- Filtered MS-DIAL peak list with features outside RMD window removed
- Feature table ready for downstream feature clustering or annotation

## How to apply

After loading an MS-DIAL peak list into MS-CleanR, specify the lower and upper bounds of the acceptable RMD window based on your sample chemistry and ionization mode (positive or negative). The filter calculates or retrieves the RMD value for each feature and discards any feature whose RMD falls outside the specified bounds. This is typically applied as part of MS-CleanR's first generic filtering stage, after blank subtraction and background ion removal but before or alongside RSD-based filtering. The exact RMD bounds are tunable by the user and should be justified by the expected mass defect distribution of your metabolites.

## Related tools

- **MS-DIAL** (Source of peak list (feature table with m/z, RT, intensity) that serves as input to RMD filtering) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Wrapper and orchestrator of RMD window filtering as part of the generic filtering workflow) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-FINDER** (Downstream annotation tool that receives filtered feature list for in silico metabolite annotation) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- Feature count before and after RMD filtering should show a clear reduction; document the number of features removed.
- Verify that all remaining features have RMD values strictly within the specified window bounds by examining the min/max RMD of the output feature table.
- Inspect the mass defect distribution of retained features to confirm it matches expected chemical ranges for organic metabolites in your sample type.
- Cross-check that no features with biologically relevant m/z or known metabolite identities were inadvertently filtered out by the RMD window.
- Confirm the RMD window bounds used are documented and justified (e.g., literature range, empirical pilot data from your instrument/method).

## Limitations

- RMD filtering relies on accurate m/z calibration from MS-DIAL; systematic m/z bias will propagate into incorrect mass defect calculation.
- The optimal RMD window bounds are sample- and method-dependent; users must define these parameters a priori or conduct sensitivity analysis to avoid over-filtering or under-filtering.
- RMD filtering alone cannot distinguish between true biological features and instrumental artifacts; it should be combined with other filters (blank subtraction, RSD thresholding, background removal).
- MS-CleanR requires at least 3 blank samples and 3 QC samples identified in the MS-DIAL sample list for proper operation; the first filtering step will fail if these are absent.
- All features lacking MS/MS fragmentation are discarded during the first MS-CleanR step, regardless of RMD filtering, if data are DDA or DIA mode without MS1-only data.

## Evidence

- [intro] Apply relative mass defect (RMD) window filtering: "Apply relative mass defect (RMD) window filtering to remove features with RMD values outside the specified window bounds."
- [intro] Generic filters including RMD: "MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on"
- [readme] Tunable parameters: "MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on"
- [intro] Workflow stage: "First, MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based"
- [readme] MS/MS requirement: "MSCleanR handle LCMS acquired in DIA or DDA mode. All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
