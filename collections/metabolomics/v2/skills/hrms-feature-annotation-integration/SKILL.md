---
name: hrms-feature-annotation-integration
description: Use when you have LC- or GC-HRMS data in mzML format and a feature list
  (CSV/TSL/Excel) from external feature detection software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pyOpenMS
  - PFΔScreen
  - MSConvert
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HRMS Feature Annotation Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate custom HRMS feature lists (from external feature-finding procedures) into PFΔScreen's prioritization pipeline, validating metadata and applying MD/C-m/C, KMD, and MS2 fragment diagnostics to features regardless of detection source. This skill enables use of vendor-specific or alternative feature detection algorithms while retaining standardized PFAS prioritization.

## When to use

You have LC- or GC-HRMS data in mzML format and a feature list (CSV/TSL/Excel) from external feature detection software (e.g., vendor tools, xcms, MZmine) that you want to prioritize for PFAS using PFΔScreen's MD/C-m/C, KMD, and MS2 fragment analysis without re-running pyOpenMS feature detection. Indicates this skill when feature finding has already been completed upstream and you need to inject those results into the standardized prioritization workflow.

## When NOT to use

- Input feature list lacks required columns (m/z, retention time, intensity) or is in an unsupported format — preprocess the feature table first
- mzML file(s) are not provided or do not correspond to the custom feature list — MS2 alignment and diagnostic fragment detection will fail
- Features are already fully annotated and prioritized; integration is redundant and will not add value

## Inputs

- Custom feature list (CSV, TSV, or Excel format) with required columns: m/z, retention time, intensity
- mzML file(s) (data-dependent acquisition with centroided spectra) corresponding to the custom feature list
- Optional: blank control mzML file for background correction

## Outputs

- Prioritized feature table (Excel format) with MD/C-m/C scores, KMD clustering assignments, and MS2 diagnostic fragment matches
- Interactive HTML plots: MD/C-m/C plot, m/z vs. RT plot (with and without MS2 raw data), KMD vs. m/z with linked m/z vs. RT plot, m/C histogram
- Comparison report indicating which custom features pass each prioritization filter (MD/C-m/C thresholding, KMD analysis, MS2 diagnostics)

## How to apply

Load the custom feature list from a user-supplied CSV/TSV/Excel file, validate that required columns (m/z, retention time, intensity) are present and properly formatted, then parse feature metadata and convert to PFΔScreen's internal feature object format. Apply MD/C-m/C ratio filtering to identify features with elevated mass defects characteristic of PFAS, perform Kendrick mass defect (KMD) clustering to group potential homologues, and cross-reference filtered features against MS2 fragment data (aligned from the corresponding mzML file) to detect diagnostic fragment mass differences indicative of PFAS structure. The mzML file(s) must be provided in parallel; data evaluation only works when corresponding mzML files are given, otherwise MS2 data would be missing. Generate a prioritized feature table and comparison report showing which custom features pass each prioritization filter stage.

## Related tools

- **PFΔScreen** (Primary execution environment for feature list integration and PFAS prioritization; provides GUI, feature object model, and prioritization filter implementation) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Upstream feature detection alternative; provides Python interface to MS raw data processing (feature finding, MS2 alignment) if not using custom feature lists)
- **MSConvert** (Data format conversion tool to generate vendor-independent mzML input files required for MS2 data retrieval during feature integration)

## Evaluation signals

- Custom feature list successfully loads without parse errors and all required columns (m/z, retention time, intensity) are present and non-empty
- Converted feature objects are compatible with downstream prioritization modules (MD/C-m/C filtering, KMD analysis) without type or schema violations
- MD/C-m/C scores are calculated for all features; filtered subset shows elevated mass defect ratios consistent with PFAS-like chemistry
- KMD clustering assigns features to homologue groups with systematic m/z and/or retention time differences indicative of repeating units (e.g., CF₂)
- MS2 diagnostic fragment detection highlights fragment mass differences and known PFAS diagnostic fragments in spectra; comparison report documents pass/fail status per filter stage
- Output Excel table and HTML plots are generated and display expected visualizations (e.g., MD/C-m/C scatter, KMD vs. m/z heatmap) without missing data

## Limitations

- Custom feature list must include m/z, retention time, and intensity columns; missing or malformed metadata will cause parsing failure or silent data loss
- mzML files must be measured under data-dependent acquisition (ddMS2) with centroided spectra and ideally one collision energy per precursor; other MS acquisition modes or profile-mode data will not yield expected MS2 diagnostics
- Feature integration workflow does not re-detect or re-align features; upstream feature detection quality (e.g., false positives, missed features, RT drift) is inherited and not corrected by PFΔScreen
- Blank correction step requires both sample and blank mzML files; absence of blank data limits ability to distinguish signal from contaminant background

## Evidence

- [readme] Optionally, custom feature lists can be included: "Optionally, custom feature lists can be included"
- [readme] custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be included in PFΔScreen. This is done by the "Browse SampleFeatures.xlsx" and "Browse BlankFeatures.xlsx" buttons, which are preprocessed by the "Run ExternalFeatureTable" button. Note that data evaluation only works when the corresponding mzML files are also given; otherwise MS2 data would be missing.: "custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be included in PFΔScreen... Note that data evaluation only works when the corresponding mzML"
- [other] Load custom feature list from user-supplied CSV/TSV file, validating required columns (m/z, retention time, intensity). Parse feature metadata and convert to internal PFΔScreen feature object format compatible with downstream prioritization modules.: "Load custom feature list from user-supplied CSV/TSV file, validating required columns (m/z, retention time, intensity). Parse feature metadata and convert to internal PFΔScreen feature object format"
- [other] Apply MD/C-m/C ratio filtering to identify PFAS-like features with elevated mass defects. Perform Kendrick mass defect (KMD) analysis on filtered features to cluster potential PFAS homologues. Cross-reference features against MS2 fragment data to detect diagnostic fragment mass differences indicative of PFAS structure.: "Apply MD/C-m/C ratio filtering to identify PFAS-like features with elevated mass defects. Perform Kendrick mass defect (KMD) analysis on filtered features to cluster potential PFAS homologues."
- [readme] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
