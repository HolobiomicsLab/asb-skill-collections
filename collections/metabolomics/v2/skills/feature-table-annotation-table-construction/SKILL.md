---
name: feature-table-annotation-table-construction
description: Use when after feature extraction from XCMS or MS-Dial when you have a feature intensity table (samples × features), a feature info table with m/z and retention time measurements, and access to a reference compound database with known m/z, retention time, and compound metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - XCMS
  - MS-Dial
  - GetFeatistics
  - patRoon
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

# feature-table-annotation-table-construction

## Summary

Construct an annotated feature information table by matching detected mass spectrometry features against a reference compound database using two-dimensional m/z and retention time criteria, assigning confidence levels (AnnoLevel) based on match uniqueness. This skill bridges raw feature detection and downstream statistical analysis by systematically transferring compound identity, metadata, and annotation certainty into a structured featINFO table.

## When to use

After feature extraction from XCMS or MS-Dial when you have a feature intensity table (samples × features), a feature info table with m/z and retention time measurements, and access to a reference compound database with known m/z, retention time, and compound metadata. Apply this skill before statistical analysis when you need to annotate features with confirmed or candidate compound identities and assign annotation confidence levels.

## When NOT to use

- Input feature table has already undergone compound annotation by another tool and you only need to import existing annotations
- Reference compound database is unavailable or does not contain retention time information (two-dimensional matching cannot proceed)
- Features lack reliable m/z or retention time values due to poor peak quality or instrumental calibration issues

## Inputs

- feature intensity table (samples × features matrix)
- feature info table (with feature ID, m/z, retention time)
- reference compound database (with m/z, retention time, compound name, and metadata)

## Outputs

- annotated featINFO table (with columns: feature ID, matched compound name, m/z, retention time, AnnoLevel, reference metadata)

## How to apply

Load the feature intensity table, feature info table (containing m/z and retention time for each feature), and reference compound list into the checkmolecules_in_feat_table function. Set user-defined m/z tolerance (in ppm or Da, typically based on instrument calibration) and retention time tolerance windows. For each feature, calculate Δm/z and ΔRT against all reference compounds and apply tolerance windows to identify candidate matches. Features with exactly one match within both tolerance windows are marked AnnoLevel 1 (confirmed identity); features with zero or multiple matches are marked NA or lower confidence level. Set return_as_featinfo_lev1 = TRUE to transfer matched compound names and metadata into the output featINFO table alongside feature IDs, m/z values, retention times, and annotation levels.

## Related tools

- **GetFeatistics** (Provides checkmolecules_in_feat_table function for two-dimensional feature-to-reference matching and AnnoLevel assignment) — https://github.com/FrigerioGianfranco/GetFeatistics
- **XCMS** (Upstream feature extraction and grouping producing raw feature tables and m/z/retention time values)
- **MS-Dial** (Alternative upstream feature extraction tool producing feature tables compatible with annotation workflow)
- **patRoon** (Comprehensive NTA platform integrating feature extraction, annotation workflows, and compound identification across multiple algorithms) — https://github.com/rickhelmus/patRoon

## Examples

```
# Load GetFeatistics and call checkmolecules_in_feat_table
library(GetFeatistics)
featINFO_annotated <- checkmolecules_in_feat_table(feat_table = intensity_matrix, feat_info = feature_info_df, molecules_db = reference_compounds, mz_tolerance = 5, mz_tolerance_unit = 'ppm', RT_tolerance = 0.5, return_as_featinfo_lev1 = TRUE)
```

## Evaluation signals

- Output featINFO table contains no duplicate feature IDs and row count matches input feature count
- Features with exactly one match within both m/z and retention time tolerance windows are marked AnnoLevel 1; features with zero or multiple matches show NA or lower confidence level
- Compound name, m/z, retention time, and reference metadata columns are fully populated for AnnoLevel 1 features; NA or empty for unconfirmed features
- m/z and retention time values in output table match input feature table exactly (no transformation or rounding applied)
- User-specified m/z tolerance (ppm or Da) and retention time window parameters are applied consistently across all features

## Limitations

- Matching accuracy depends critically on reference database completeness and accuracy; missing or misidentified reference compounds will lower match rates
- Two-dimensional matching requires both m/z and retention time to be present and reliable; features lacking retention time information cannot be annotated
- m/z and retention time tolerance windows must be carefully calibrated for each instrument and chromatographic method; inappropriate tolerances lead to false negatives (missed matches) or false positives (non-specific matches)
- AnnoLevel 1 (confirmed identity) is assigned only to features with exactly one match; features matching multiple reference compounds are marked lower confidence, limiting confirmation of true isomers or analogs without additional MS/MS data

## Evidence

- [other] The checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified error tolerances (in ppm or Da) and retention time windows.: "checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified"
- [other] For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound. Apply m/z tolerance and retention-time tolerance windows (specific tolerances to be set by the user based on instrument calibration and method) to identify candidate matches.: "For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound. Apply m/z"
- [other] For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table. For features with zero or multiple matches, mark annotation level as NA or lower confidence level and retain feature ID in the featINFO table.: "For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table. For features with zero or"
- [intro] This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial: "This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial"
- [other] Export the annotated featINFO table with columns for feature ID, matched compound name, m/z, retention time, annotation level, and any additional reference metadata.: "Export the annotated featINFO table with columns for feature ID, matched compound name, m/z, retention time, annotation level, and any additional reference metadata"
