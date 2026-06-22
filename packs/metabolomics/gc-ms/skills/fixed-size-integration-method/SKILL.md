---
name: fixed-size-integration-method
description: Use when you have aligned and baseline-corrected GC-IMS data with detected and clustered peaks, and you want to extract peak intensities using a consistent integration window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.chemolab.2023.104938
  all_source_dois:
  - 10.1016/j.chemolab.2023.104938
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fixed-size-integration-method

## Summary

A peak integration strategy for GC-IMS data that uses a uniform window size across all detected peaks, rather than adapting to individual peak widths. This method is applied after peak detection and clustering to quantify peak intensities into a sample-by-peak matrix suitable for downstream statistical analysis.

## When to use

Apply this skill when you have aligned and baseline-corrected GC-IMS data with detected and clustered peaks, and you want to extract peak intensities using a consistent integration window. Use fixed-size integration when peak widths are expected to be relatively uniform across your sample set, or when you want to enforce reproducibility by using identical integration parameters across all peaks rather than adapting to individual peak morphology.

## When NOT to use

- Peak widths vary substantially across your dataset; use adaptive integration methods instead.
- Your peaks have already been integrated using a different method and you need to compare or validate against another approach.
- Input data has not yet undergone alignment or baseline correction; preprocess first.

## Inputs

- GCIMSDataset object (post-alignment, post-baseline-correction)
- Detected and clustered peaks (output of peakDetection and clusterPeaks)

## Outputs

- peak_table_matrix (rows=clusters, columns=samples, values=integrated intensities with NA entries)

## How to apply

After loading preprocessed GC-IMS data (post-alignment and baseline correction) into R, call the integratePeaks function with the integration_size_method parameter set to 'fixed_size' and specify the rip_saturation_threshold (typically 0.1 to exclude Reactant Ion Peak saturation artifacts). This produces an integration result object containing intensity values for each peak-sample combination. Then call peakTable on the integration result to extract and format these intensities into a matrix where rows represent peak clusters and columns represent samples. The resulting peak_table_matrix will contain numeric intensity values with some NA entries where peaks were not detected or integration failed; these NA values require downstream imputation before statistical analysis.

## Related tools

- **GCIMS** (R package that implements integratePeaks and peakTable functions; provides the fixed_size integration method and peak clustering prerequisites) — https://github.com/sipss/GCIMS
- **R** (Runtime environment for executing GCIMS workflows and peak integration)

## Examples

```
integration_result <- integratePeaks(dataset, integration_method = 'fixed_size', rip_saturation_threshold = 0.1); peak_table_matrix <- peakTable(integration_result)
```

## Evaluation signals

- peak_table_matrix dimensions are correct: number of rows equals number of detected clusters, number of columns equals number of samples
- All numeric values in the matrix are non-negative intensities or explicitly NA (no NaN, Inf, or negative values except for NA)
- Proportion of NA entries is documented and consistent with expected detection failures; extreme sparsity (>80% NA) may indicate integration parameter misconfiguration
- Intensity values across samples show expected variation (e.g., known positive controls have higher intensities than blanks)
- The matrix structure matches the output of peakTable: one row per cluster, one column per sample, with column names matching sample identifiers

## Limitations

- Fixed-size integration may poorly represent peaks with highly variable widths across the dataset; narrow peaks may be underintegrated and broad peaks overintegrated.
- The choice of fixed integration window size is not detailed in the article; practitioners must calibrate this parameter based on their instrument and sample type.
- NA entries in the resulting matrix require downstream imputation before multivariate statistical analysis; the article does not specify imputation methods.
- The rip_saturation_threshold parameter (e.g., 0.1) filters out saturated RIP signals but may also exclude genuine sample peaks if they exceed this threshold.

## Evidence

- [other] integration_size_method set to 'fixed_size': "Execute integratePeaks function with integration_size_method set to 'fixed_size' and rip_saturation_threshold parameter set to 0.1"
- [other] peakTable output structure: "The peakTable function produces a peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA that require imputation"
- [other] preprocessing prerequisites: "Load the preprocessed GC-IMS dataset (after alignment and baseline correction) into R using the GCIMS package"
- [readme] GCIMS package and R runtime: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples"
- [intro] Pressure and temperature fluctuations alignment problem: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time"
