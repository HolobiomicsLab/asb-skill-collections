---
name: cross-sample-metabolite-matching
description: Use when after feature extraction (MS1 peak picking, MS2 recognition, or targeted list extraction) from multiple individual samples and before annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - JPA
  - R
  - XCMS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
---

# cross-sample-metabolite-matching

## Summary

Align metabolic features detected across multiple LC-MS samples by clustering on retention time and m/z values to produce a unified feature table. This consolidation step is essential for comparative metabolomics studies where the same metabolite may appear at slightly different retention times or m/z values across samples due to instrument drift or measurement noise.

## When to use

After feature extraction (MS1 peak picking, MS2 recognition, or targeted list extraction) from multiple individual samples and before annotation. Apply this skill when you have per-sample feature tables and need to determine which features across samples represent the same metabolite, accounting for expected retention time and m/z variation within your instrument's tolerance.

## When NOT to use

- Input is already an aligned or consolidated feature table from another tool
- Single-sample analysis where cross-sample matching is not applicable
- Full-scan or DIA (data-independent acquisition) datasets without prior MS1 feature extraction

## Inputs

- Per-sample feature tables (CSV or dataframe format with columns: m/z, retention time, rtmin, rtmax, intensity)
- Extracted feature tables from MS1 peak picking, MS2 recognition, or targeted list extraction
- Retention time tolerance window (user-specified, in seconds)
- m/z tolerance threshold (user-specified, in ppm or absolute Da)

## Outputs

- Unified aligned feature table (dataframe with mz, rt, rtmin, rtmax, maxo, sample, level columns)
- Alignment statistics (number of aligned features, sample-to-feature coverage matrix)
- Alignment quality metrics

## How to apply

Load extracted feature tables from individual samples (each containing m/z, retention time, rtmin, rtmax, and intensity columns in seconds). Apply retention time-based clustering to group putatively identical features across samples within a specified retention time tolerance window. Refine grouping by applying m/z-based clustering to merge features with matching mass-to-charge ratios within the instrument's m/z tolerance (typically 5–10 ppm for accurate-mass instruments). Generate alignment statistics including the number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics to assess consolidation success. Export the unified aligned feature table in standardized format (dataframe with mz, rt, rtmin, rtmax, maxo, sample, and level columns) compatible with downstream annotation modules.

## Related tools

- **JPA** (Performs retention time and m/z-based clustering to align features across samples and generate unified feature table with alignment statistics) — https://github.com/HuanLab/JPA.git
- **XCMS** (Upstream peak picking and feature extraction prior to alignment) — https://rdrr.io/bioc/xcms/man/
- **R** (Programming environment in which JPA alignment workflow is implemented)

## Evaluation signals

- All features in the unified table are represented by consistent mz and rt values across samples with minimal drift
- Sample-to-feature coverage matrix shows expected patterns (high coverage for abundant features, lower for rare ones)
- Number of aligned features is reasonable relative to input sample count and expected metabolome complexity
- Alignment quality metrics (e.g., clustering consistency, feature merging success rate) meet expected thresholds
- Exported aligned feature table schema matches downstream annotation module expectations (Part 6: CAMERA annotation compatibility)

## Limitations

- Retention time drift and m/z calibration issues in raw data can compromise clustering accuracy; pre-alignment QC of individual feature tables is recommended
- Tolerance windows (rt and m/z) must be empirically determined for each instrument and method; overly strict windows may fragment true features, while loose windows may merge distinct metabolites
- Features present in only one or few samples may be lost or misaligned if their abundance is low relative to instrument noise
- Alignment does not disambiguate isomers or isobars with identical m/z and similar retention times

## Evidence

- [intro] JPA includes an alignment workflow step (Part 5: Alignment) as part of its comprehensive metabolomics data processing pipeline that operates after feature extraction and before annotation.: "JPA includes an alignment workflow step (Part 5: Alignment) as part of its comprehensive metabolomics data processing pipeline that operates after feature extraction and before annotation."
- [other] Load extracted feature tables from individual samples (output from MS1 peak picking, MS2 recognition, or targeted list extraction). Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows. Apply m/z-based clustering to refine grouping and merge features with matching mass-to-charge ratios.: "Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows. Apply m/z-based clustering to refine grouping and merge features with"
- [other] Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics.: "Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics."
- [readme] For multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5.: "For multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5."
- [readme] The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity.: "The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity."
