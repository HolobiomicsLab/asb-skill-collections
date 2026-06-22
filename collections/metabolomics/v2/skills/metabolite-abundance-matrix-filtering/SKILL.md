---
name: metabolite-abundance-matrix-filtering
description: 'Use when when you have multiple batches of metabolomics data in SummarizedExperiment format with log-transformed abundance assays and need to: (1) remove poorly-quantified metabolites with >50% missing values within each batch, (2) retain only metabolites present across all batches for cross-batch.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
  - DMwR2
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration... library(dplyr)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
---

# metabolite-abundance-matrix-filtering

## Summary

Filter metabolite abundance matrices by missing-value threshold and feature intersection across batches, then impute missing values using k-nearest neighbour. This skill reduces the feature space to metabolites reliably quantified across all batches while preserving signal integrity through principled imputation.

## When to use

When you have multiple batches of metabolomics data in SummarizedExperiment format with log-transformed abundance assays and need to: (1) remove poorly-quantified metabolites with >50% missing values within each batch, (2) retain only metabolites present across all batches for cross-batch comparisons, and (3) impute remaining scattered missing values before downstream normalisation or statistical analysis.

## When NOT to use

- Input data already has no missing values or has been pre-filtered to a single consistent feature set across batches — the filtering and imputation steps would be redundant.
- You require retention of metabolites present in only a subset of batches (e.g., for batch-specific biomarker discovery) — the intersect method discards batch-specific signals.
- Missing values are believed to be informative (e.g., true biological absence rather than measurement failure) — imputation by k-NN would introduce bias.

## Inputs

- List of SummarizedExperiment objects (one per batch)
- Log-transformed metabolite abundance assay (e.g., 'logRaw' assay within each SummarizedExperiment)

## Outputs

- List of SummarizedExperiment objects with new assay (e.g., 'rawImpute') containing filtered and imputed metabolite abundances
- Reduced metabolite feature set (metabolites retained across all batches)
- Complete abundance matrix with no missing values

## How to apply

Load a list of SummarizedExperiment objects, each representing one batch with a log-transformed abundance assay (e.g., 'logRaw'). Apply hRUV::clean() with threshold=0.5, method='intersect', specifying the source assay and a new assay name (e.g., 'rawImpute'). The function first filters out metabolites with ≥50% missing values per batch, then retains only those quantified (non-missing) in all batches via set intersection, and finally performs k-nearest neighbour imputation on the remaining missing values. Verify the output by confirming metabolite count reduction, zero missing values in the new assay, and consistent dimensions across all batches.

## Related tools

- **hRUV** (Applies clean() function to filter metabolites by missing-value threshold and intersect method, then performs k-NN imputation on the filtered abundance matrix.) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Data container for storing and accessing batch-wise metabolite abundance assays with consistent row/column structure.)
- **DMwR2** (Provides k-nearest neighbour imputation algorithm used by hRUV::clean() to fill remaining missing values.)
- **dplyr** (Supporting utility for data manipulation and verification of filtering results.)

## Examples

```
dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")
```

## Evaluation signals

- Metabolite count in output assay is smaller than input (confirms filtering occurred) and matches the number of features quantified in all batches.
- Output assay contains zero missing values (NA or NaN counts are 0).
- Dimensions (samples × metabolites) are identical across all batches in the output list.
- Metabolites retained are a subset of the input metabolites; no novel metabolites appear in the output.
- Log-transformed abundance values in the imputed assay remain within plausible range (no extreme outliers introduced by k-NN imputation).

## Limitations

- The 50% missing-value threshold is fixed in the workflow; if data has a different missingness pattern, the threshold may need adjustment (not explored in the article).
- The intersect method is conservative — metabolites unique to any single batch are discarded, which may lose batch-specific signals or rare metabolites.
- k-NN imputation relies on abundance similarity among samples; it may perform poorly in low-sample-count batches or when metabolite abundance distribution is non-metric.
- No changelog provided in the hRUV repository, limiting traceability of parameter defaults or imputation algorithm versions.

## Evidence

- [intro] The `clean` function filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation to produce a rawImpute assay containing 61 metabolites quantified across all five batches.: "The `clean` function filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation"
- [intro] We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect): "We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect)"
- [intro] dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute"): "dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")"
- [readme] `hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy: "`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy"
- [intro] assay(dat, "logRaw", withDimnames = FALSE) = log2(assay(dat, "raw") + 1): "assay(dat, "logRaw", withDimnames = FALSE) = log2(assay(dat, "raw") + 1)"
