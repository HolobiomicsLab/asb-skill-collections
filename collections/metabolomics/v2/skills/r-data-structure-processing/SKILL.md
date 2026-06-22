---
name: r-data-structure-processing
description: Use when you have a peak table matrix with NA values that need to be imputed using cluster statistics, or when a GCIMSDataset object requires filtering by retention time (0–1100 s) and drift time (5–16 ms) ranges, or when you need to apply smoothing, decimation, or baseline correction to raw GCIMS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GCIMS
  - ggplot2
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
---

# R data structure processing

## Summary

Process and transform R data structures (matrices, datasets, objects) through imputation, filtering, and normalization operations to prepare Gas Chromatography–Ion Mobility Spectrometry (GCIMS) sample data for downstream analysis. This skill ensures missing values are filled systematically and data conform to expected schemas.

## When to use

Apply this skill when you have a peak table matrix with NA values that need to be imputed using cluster statistics, or when a GCIMSDataset object requires filtering by retention time (0–1100 s) and drift time (5–16 ms) ranges, or when you need to apply smoothing, decimation, or baseline correction to raw GCIMS sample matrices before peak detection or alignment.

## When NOT to use

- Peak table is already complete with no missing values — imputation is redundant.
- Dataset has already undergone alignment and peak clustering — do not re-apply filtering before these steps.
- Input is not a GCIMSDataset object or numeric matrix (e.g., CSV file alone without R object conversion).

## Inputs

- peak_table_matrix (numeric matrix with NA values)
- dataset (GCIMSDataset object)
- cluster_stats (cluster statistics object from peak clustering)

## Outputs

- imputed_peak_table (numeric matrix with NA values filled)
- filtered_dataset (GCIMSDataset object constrained to specified retention and drift time ranges)
- preprocessed_dataset (GCIMSDataset object after smoothing, decimation, and baseline correction)

## How to apply

Load the peak table matrix, dataset object, and cluster statistics into the R environment. Call the imputePeakTable function with these three arguments to fill NA values in the peak table matrix. Alternatively, construct a GCIMSDataset object from imported sample annotations and raw data, then apply filterRt and filterDt functions to constrain retention and drift time ranges. Use Savitzky–Golay smoothing to reduce noise in drift and retention time dimensions, apply decimation to reduce memory usage and computation time, and perform baseline correction before peak detection. All operations leverage GCIMS's delayed evaluation strategy to minimize RAM overhead during matrix transformations.

## Related tools

- **GCIMS** (R package providing imputePeakTable, filterRt, filterDt, and baseline correction functions for GCIMSDataset object manipulation and preprocessing) — https://github.com/sipss/GCIMS
- **R** (Programming environment for executing data structure transformations and calling GCIMS functions)
- **ggplot2** (Optional visualization of filtered or imputed data structures)

## Examples

```
imputePeakTable(peak_table_matrix, dataset, cluster_stats)
```

## Evaluation signals

- All NA values in the imputed peak table are replaced with numeric values (verify no remaining NA entries).
- Filtered dataset retains only rows where retention time falls within [0, 1100] s and drift time within [5, 16] ms.
- Imputed peak table dimensions and row/column names match the original peak table schema.
- Baseline-corrected and smoothed matrices show reduced noise in drift and retention time dimensions without removing true signal peaks.
- Decimated dataset size is reduced by the specified factor (1 every Nd points in drift time, 1 every Nr in retention time) while preserving alignment integrity.

## Limitations

- Imputation relies on cluster_stats quality; poor or incomplete cluster statistics will yield unreliable imputed values.
- Filtering by fixed retention and drift time ranges may remove legitimate sample peaks if range boundaries are chosen incorrectly for a specific experiment.
- Savitzky–Golay filter smoothing requires manual optimization of the noise_level parameter, particularly when applied to samples with widely varying signal intensities.
- Delayed evaluation in GCIMS improves RAM efficiency but may obscure which intermediate transformations are causing unexpected downstream artifacts; explicit intermediate exports are recommended for debugging.

## Evidence

- [intro] Imputation function and verification method: "Call imputePeakTable function with peak_table_matrix, dataset, and cluster_stats as arguments to impute missing values. Verify that all NA values have been filled"
- [intro] Filtering workflow for retention and drift time: "filterRt(dataset, rt = c(0, 1100)) # in s
filterDt(dataset, dt = c(5, 16)) # in ms"
- [intro] Smoothing and decimation rationale: "You can remove noise from your sample using a Savitzky–Golay filter, applied both in drift time and in retention time. One way to speed up calculations and reduce the memory requirements is to"
- [intro] Delayed evaluation efficiency: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM"
- [intro] GCIMSDataset object creation and preprocessing workflow: "Create a GCIMSDataset object. Filter the retention and drift time of your samples. The alignment will happen first in drift time and afterwards in retention time."
