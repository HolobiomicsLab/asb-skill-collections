---
name: metabolite-feature-m-z-matching
description: Use when you have (1) a benchmark dataset of known molecules with accurate m/z values, retention time boundaries, and isotopologue identifiers for all enviPat-predicted adducts;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - mzRAPP
  - R
  - enviPat
  - XCMS
  - MZmine 2
  - Skyline
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
---

# metabolite-feature-m/z-matching

## Summary

Match peaks from a benchmark dataset (with known m/z and retention time boundaries) to features detected by non-targeted pre-processing (NPP) tools, producing a record table that classifies each benchmark peak as found, split, missing, or misaligned. This skill enables quantitative reliability assessment of NPP tool performance by pairing theoretical isotopologue signatures with empirical feature detections.

## When to use

Apply this skill when you have (1) a benchmark dataset of known molecules with accurate m/z values, retention time boundaries, and isotopologue identifiers for all enviPat-predicted adducts; (2) unaligned and aligned feature tables exported from one or more NPP tools (XCMS, MZmine 2, MS-DIAL, etc.) run on the same mzML files; and (3) a need to quantify what fraction of known peaks were detected, how many were split across multiple features, and whether isotopologue ratios were preserved — i.e., to audit NPP reliability rather than perform exploratory feature discovery.

## When NOT to use

- Input is a feature table without known benchmark peaks with confirmed RT boundaries and isotopologue annotations — use exploratory feature detection instead.
- NPP outputs are not in tabular format (m/z, RT, feature ID) or lack sufficient metadata to perform m/z and RT matching.
- Benchmark molecules lack multi-isotopologue validation data (i.e., only single isotopologues are available); matching will be less stringent and cannot assess isotopologue ratio degradation.

## Inputs

- Benchmark dataset CSV containing: molecule identifiers, m/z values, retention time boundaries (start/end in seconds), isotopologue identifiers, adduct type (main_adduct), and optional additional columns
- Unaligned feature table from NPP tool (m/z, retention time, feature ID, peak intensity/area)
- Aligned feature table from NPP tool (m/z, retention time, feature ID, peak intensity/area)
- Instrument resolution parameters (R value at half height, m/z calibration points) for isotopologue prediction accuracy

## Outputs

- Matched record CSV table with columns: benchmark_peak_identifier, matching_status (found/split/missing/misaligned), matched_NPP_feature_ID, confidence_score, isotopologue_validation_flags
- Performance summary metrics: % peaks found, % split peaks, % missing peaks, % peaks with degenerated isotopologue ratio (IR > 30% bias)
- Alignment error count: number of peaks where RT boundary mismatch occurs between unaligned and aligned feature tables

## How to apply

Load benchmark peaks (m/z, retention time boundaries, isotopologue identifiers, adduct types) and NPP output feature tables into memory. For each benchmark peak, apply m/z matching using a precision tolerance of 6 ppm and accuracy threshold of 5 ppm to filter candidate NPP features. Narrow candidates further by applying retention-time windowing to the boundaries provided in the benchmark. For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter out isotopologues where the isotopologue ratio bias exceeds 30%. Classify each benchmark peak into one of four categories — 'found' (single match), 'split' (multiple NPP peaks matched), 'missing' (no match), or 'misaligned' (match outside RT boundary) — across both unaligned and aligned feature tables. Output a matched record CSV table linking each benchmark peak to its matching status, matched NPP feature ID (if applicable), confidence scores, and isotopologue validation flags.

## Related tools

- **mzRAPP** (Primary implementation tool that automates benchmark-to-NPP matching, isotopologue validation, and performance metric generation) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Isotopologue pattern prediction for all adducts and molecular formulas; provides m/z and relative abundance signatures for matching)
- **XCMS** (Example NPP tool producing unaligned and aligned feature tables to be matched against benchmark)
- **MZmine 2** (Example NPP tool producing unaligned and aligned feature tables to be matched against benchmark)
- **Skyline** (Manual peak curation and RT boundary export for benchmark dataset generation)
- **R** (Environment for running mzRAPP library and generating benchmark/assessment reports)

## Examples

```
library(mzRAPP); assessment_result <- performReliabilityAssessment(benchmark = 'benchmark_MTBLS267.csv', npp_unaligned = 'xcms_features_unaligned.csv', npp_aligned = 'xcms_features_aligned.csv', ppm_tolerance = 6, rt_window_sec = c(30, 600))
```

## Evaluation signals

- Matched record table has one row per benchmark peak and no duplicate benchmark peak IDs across unaligned and aligned assessments.
- All benchmark peaks are assigned a valid classification: 'found', 'split', 'missing', or 'misaligned' with supporting feature IDs and RT boundaries noted.
- For 'found' and 'split' matches, the matched NPP m/z values lie within ±6 ppm of benchmark m/z; for 'misaligned' peaks, RT falls outside user.rtmin/user.rtmax.
- Isotopologue ratio bias is calculated as (observed_abundance − predicted_abundance) / predicted_abundance; peaks flagged as degraded have |bias| > 30%.
- Peak shape correlation with most abundant isotopologue (Pearson correlation coefficient) is ≥ 0.85 for retained isotopologues; those < 0.85 are filtered.
- Performance metrics are consistent across replicate runs (e.g., 30 mzML files should yield stable detection rates and IR degradation percentages).

## Limitations

- Matching accuracy depends on accurate provision of RT boundaries in the benchmark; peaks with user.rtmin/user.rtmax outside the true chromatographic window will be incorrectly classified as missing.
- m/z matching assumes instrument calibration within ±5 ppm accuracy; miscalibrated data will produce false misalignments.
- Isotopologue ratio filtering (30% bias threshold) is data-dependent; low-abundance isotopologues may be rejected in high-noise samples regardless of true biological presence.
- NPP tools with different feature de-duplication or alignment strategies may yield varying numbers of 'split' classifications; direct tool comparison requires consistent export settings.
- Only isotopologues for which the theoretically most abundant isotopologue and at least one additional isotopologue are detected pass benchmark inclusion, so rare/trace isotopologues are excluded from assessment.

## Evidence

- [other] For each benchmark peak, apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features.: "For each benchmark peak, apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features."
- [other] Apply retention-time windowing to narrow candidate matches to the expected chromatographic boundaries provided in the benchmark.: "Apply retention-time windowing to narrow candidate matches to the expected chromatographic boundaries provided in the benchmark."
- [other] For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%.: "For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%."
- [other] Classify each benchmark peak as 'found', 'split' (matched to multiple NPP peaks), 'missing', or 'misaligned' based on the matching result in both unaligned and aligned feature tables.: "Classify each benchmark peak as 'found', 'split' (matched to multiple NPP peaks), 'missing', or 'misaligned' based on the matching result in both unaligned and aligned feature tables."
- [other] Generate a matched record CSV table containing benchmark peak identifier, matching status, matched NPP feature ID (if found), confidence scores, and isotopologue validation flags.: "Generate a matched record CSV table containing benchmark peak identifier, matching status, matched NPP feature ID (if found), confidence scores, and isotopologue validation flags."
- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [readme] Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark.: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark."
