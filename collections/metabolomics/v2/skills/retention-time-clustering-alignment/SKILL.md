---
name: retention-time-clustering-alignment
description: Use when you have extracted feature tables (via MS1 peak picking, MS2 recognition, or targeted list extraction) from two or more individual LC-MS samples and need to identify which features represent the same metabolite across samples before generating a unified, sample-aligned feature table for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - JPA
  - R
  - XCMS
  - CAMERA
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

# retention-time-clustering-alignment

## Summary

Group putatively identical metabolic features detected across multiple LC-MS samples by clustering on retention time within specified tolerance windows, as a preliminary step before m/z-based refinement in multi-sample metabolomics alignment. This skill consolidates redundant or near-duplicate feature detections into unified feature identities for downstream annotation.

## When to use

You have extracted feature tables (via MS1 peak picking, MS2 recognition, or targeted list extraction) from two or more individual LC-MS samples and need to identify which features represent the same metabolite across samples before generating a unified, sample-aligned feature table for adduct and metabolite annotation.

## When NOT to use

- Input is already an aligned feature table from a prior alignment run; re-clustering will introduce redundancy or degrade existing alignments.
- Single-sample analysis where no cross-sample consolidation is needed; retention time clustering is designed for multi-sample workflows.
- Full-scan or DIA (data-independent acquisition) datasets where retention time variability may exceed typical tolerance windows; consider broader tolerance or alternative alignment strategies.

## Inputs

- Per-sample feature tables (CSV or data frame format with columns: m/z, retention time (seconds), rtmin, rtmax, intensity)
- Retention time tolerance window (seconds; typical range 10–30 s)
- m/z tolerance (ppm; typical range 5–10 ppm)

## Outputs

- Unified aligned feature table (standardized CSV or data frame)
- Sample-to-feature coverage matrix (rows = features, columns = samples, entries = intensity or presence/absence)
- Alignment statistics (e.g., number of aligned features, coverage distribution, alignment quality metrics)

## How to apply

Load the extracted per-sample feature tables (each containing m/z, retention time, rtmin, rtmax, intensity columns in seconds). Apply retention time-based clustering by grouping features within a specified retention time tolerance window (e.g., ±10–30 seconds, user-configurable). Within each retention time cluster, apply secondary m/z-based clustering to refine grouping and merge features with matching mass-to-charge ratios within ppm tolerance. Generate alignment statistics including the number of aligned features, sample-to-feature coverage matrix (indicating how many samples each feature appears in), and alignment quality metrics. Export the unified aligned feature table in a standardized format (e.g., CSV with columns: aligned_feature_id, mz, rt, sample_count, intensity_per_sample) compatible with JPA's downstream CAMERA annotation and MS2 annotation modules.

## Related tools

- **JPA** (Primary R package implementing the alignment workflow (Part 5: Alignment) that orchestrates retention time and m/z clustering and exports aligned feature tables) — https://github.com/HuanLab/JPA.git
- **XCMS** (Embedded XCMS functions used within JPA for feature extraction (MS1 peak picking) prior to alignment; XCMS algorithms handle m/z tolerance and peak detection parameters) — https://rdrr.io/bioc/xcms/man/
- **CAMERA** (Downstream annotation module (Part 6: CAMERA annotation) that uses the aligned feature table to assign adduct annotations and refine metabolite grouping)

## Examples

```
# Assuming featureTable is a per-sample feature table loaded in R via XCMS.featureTable() or custom.featureTable()
# JPA's alignment function (conceptually shown; exact function name from Part 5 of manual):
aligned_ft <- alignment.function(featureTable, rt.tol = 15, mz.ppm = 10)
```

## Evaluation signals

- Aligned feature count matches expected metabolite complexity; each aligned feature should have a single m/z and rt pair (or narrow range) across samples.
- Sample-to-feature coverage matrix shows expected sparsity: high-abundance features should appear in most/all samples; low-abundance features may be sample-specific.
- Retention time deviation within clusters should be ≤ the specified tolerance window (e.g., ±10 s); outliers indicate either misalignment or genuine biological sample-to-sample drift.
- Aligned feature intensity distributions are non-zero across specified samples; zero-intensity entries indicate missing features in certain samples (acceptable if biologically relevant).
- Export file contains all required columns (feature_id, mz, rt, rtmin, rtmax, per-sample intensity) and is readable by downstream CAMERA annotation functions without format errors.

## Limitations

- Retention time can vary between samples due to instrument drift, column aging, or differing mobile phase conditions; fixed tolerance windows may miss true alignments in high-drift scenarios or incorrectly merge unrelated features.
- m/z measurement error depends on instrument resolution and calibration; ppm tolerance must be tuned to the mass spectrometer's typical accuracy (e.g., 5 ppm for high-resolution Orbitrap, 10 ppm for lower-resolution instruments).
- Features with identical m/z and rt but different ionization states or adducts may be incorrectly merged; post-alignment CAMERA annotation (Part 6) is required to deconvolute adducts and assign correct molecular identities.
- Clustering performance degrades if per-sample feature extraction parameters (peak picking, noise thresholds, integration settings) are inconsistent across samples; users must standardize extraction parameters before alignment.

## Evidence

- [other] Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows.: "Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows."
- [other] Apply m/z-based clustering to refine grouping and merge features with matching mass-to-charge ratios.: "Apply m/z-based clustering to refine grouping and merge features with matching mass-to-charge ratios."
- [other] Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics.: "Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics."
- [readme] JPA also performs sample alignment, adduct and metabolite annotations.: "JPA also performs sample alignment, adduct and metabolite annotations."
- [readme] for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5.: "for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5."
