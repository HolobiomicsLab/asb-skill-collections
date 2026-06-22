---
name: compound-database-lookup-and-curation
description: Use when after feature extraction from LC–MS raw data (via XCMS, MS-Dial, or equivalent) has yielded a feature intensity table (samples × features) and feature metadata table (m/z, retention time, feature ID).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - XCMS
  - MS-Dial
  - GetFeatistics
  - patRoon
  techniques:
  - LC-MS
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- open source tools such as XCMS and MS-Dial
- after obtaining a feature table using open source tools such as XCMS and MS-Dial.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-database-lookup-and-curation

## Summary

Match detected metabolomic features against a reference compound database using two-dimensional m/z and retention time criteria to assign confirmed molecular identities (AnnoLevel 1). This skill integrates feature intensity and metadata tables with known molecule lists to produce annotated feature information tables suitable for downstream statistical analysis.

## When to use

After feature extraction from LC–MS raw data (via XCMS, MS-Dial, or equivalent) has yielded a feature intensity table (samples × features) and feature metadata table (m/z, retention time, feature ID). Use this skill when you have a curated reference compound database with known m/z, retention time, and annotation metadata, and you wish to identify and mark features with high-confidence molecular assignments for targeted or non-targeted metabolomics workflows.

## When NOT to use

- Input feature table has not been processed through feature extraction and alignment; raw MS spectra or extracted ion chromatograms alone are insufficient.
- Reference compound database is missing m/z, retention time, or other critical metadata required for two-dimensional matching.
- Instrument calibration quality is unknown or untested; m/z and retention time error distributions have not been characterized.

## Inputs

- Feature intensity table (samples × features, numeric matrix or data frame)
- Feature info table (feature ID, m/z, retention time, and optional metadata)
- Reference compound database (compound name, m/z, retention time, and annotation metadata)

## Outputs

- Annotated featINFO table with columns: feature ID, matched compound name, m/z, retention time, annotation level (AnnoLevel 1 for confirmed, NA or lower for unconfirmed), and reference metadata

## How to apply

Load the feature intensity table, feature info table with m/z and retention time per feature, and a reference compound database. For each feature, perform two-dimensional matching: calculate the mass difference (Δm/z in ppm or Da) and retention-time difference (ΔRT in minutes or seconds) between the feature and each reference compound. Apply user-defined tolerance windows for m/z (e.g., 5 ppm, 10 mDa) and retention time (e.g., ±0.5 min) based on instrument calibration and method validation. Assign AnnoLevel 1 (confirmed identity) only to features with exactly one match within both tolerance windows; transfer the compound name, m/z, retention time, and reference metadata to the output featINFO table. For features with zero or multiple matches, mark annotation level as NA or lower confidence and retain feature ID. Export the annotated featINFO table with columns for feature ID, matched compound name, m/z, retention time, annotation level, and reference metadata.

## Related tools

- **XCMS** (Feature extraction and alignment for generating the input feature intensity and metadata tables)
- **MS-Dial** (Feature extraction and alignment for generating the input feature intensity and metadata tables)
- **GetFeatistics** (R package containing or wrapping checkmolecules_in_feat_table function for database lookup and AnnoLevel 1 assignment) — https://github.com/FrigerioGianfranco/GetFeatistics
- **patRoon** (Comprehensive NTA workflow platform that can orchestrate feature extraction, compound annotation, and formula/library-based identity assignment) — https://github.com/rickhelmus/patRoon
- **R** (Programming language for implementing database lookup and annotation logic (version ≥ 4.3.1 recommended))

## Examples

```
checkmolecules_in_feat_table(feat_intensity_table = samples_x_features, feat_info_table = feature_metadata, known_molecules = reference_db, mz_tol = 5, rt_tol = 0.5, return_as_featinfo_lev1 = TRUE)
```

## Evaluation signals

- Output featINFO table contains no null or malformed values in feature ID, m/z, or retention time columns for all input features.
- AnnoLevel 1 assignments occur only when exactly one reference compound falls within both specified m/z and retention time tolerance windows; features with zero or multiple matches are marked NA or lower confidence level.
- m/z and retention time values in the output match the reference database values (within rounding); no cross-contamination or mis-assignment between reference compounds.
- All features from the input feature table are represented in the output; no features are dropped during matching.
- Downstream statistical analysis (e.g., univariate tests, PCA, linear models via lme4 or AER) on confirmed (AnnoLevel 1) compounds produces consistent results across replicates and QC samples.

## Limitations

- Accuracy depends critically on instrument calibration and the accuracy of m/z and retention time values in the reference database; poorly calibrated instruments or outdated reference databases will produce false negatives or false positives.
- Two-dimensional matching alone cannot distinguish between isomeric compounds or structural isomers that share m/z and retention time; additional MS/MS fragmentation data or chemical context is required for disambiguation.
- Tolerance window thresholds (ppm/Da, minutes) must be user-specified based on instrument and method; no universal optimal values exist and inappropriate thresholds will either over- or under-annotate features.
- Features with retention time drift due to column degradation, temperature variation, or method changes may fail to match otherwise correct reference compounds if retention time tolerances are too narrow.
- Reference databases may be incomplete or contain duplicates, outdated, or incorrect m/z or retention time entries, leading to missed or erroneous identifications.

## Evidence

- [other] The checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified error tolerances.: "checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified"
- [other] For each feature in the table, perform two-dimensional matching: calculate mass difference and retention-time difference between the feature and each reference compound.: "For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound"
- [other] For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer compound metadata to the featINFO table.: "For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table"
- [readme] The GetFeatistics package provides functions for elaboration of targeted and non-targeted metabolomics data including feature table elaboration.: "Getting streamlined elaboration of targeted and non-targeted metabolomics data, including elaboration of feature tables"
- [readme] Non-targeted feature extraction from XCMS or MS-Dial output is the starting point for GetFeatistics analysis.: "This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial"
