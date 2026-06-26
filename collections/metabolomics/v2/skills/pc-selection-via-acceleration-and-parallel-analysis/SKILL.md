---
name: pc-selection-via-acceleration-and-parallel-analysis
description: Use when when preparing metabolomic or multivariate count data for outlier
  detection in PC space, or when you need to reduce dimensionality while retaining
  only statistically significant components.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot2
  - metaboprep
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
- library(ggplot2)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac059/6522114
  all_source_dois:
  - 10.1093/bioinformatics/btac059/6522114
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pc-selection-via-acceleration-and-parallel-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Determine the optimal number of informative principal components (PCs) in metabolomic data by applying acceleration analysis and parallel analysis to identify where variance explanation plateaus. This skill gates downstream PC-based outlier detection and dimensionality reduction by eliminating spurious high-variance noise dimensions.

## When to use

When preparing metabolomic or multivariate count data for outlier detection in PC space, or when you need to reduce dimensionality while retaining only statistically significant components. Apply this skill before performing PC-based sample outlier enumeration at standard deviation thresholds (e.g., 3 SD, 4 SD, 5 SD on top PCs), or when the number of available PCs exceeds the number of informative (non-noise) components.

## When NOT to use

- Input data is already a pre-computed PC score matrix or loadings matrix (not raw features)—in that case, dimensionality is already selected.
- Sample size is very small (n < 5–10) relative to number of features, making parallel analysis unreliable due to sparse permutation distributions.
- Data is already known to be low-rank or have a fixed dimensionality (e.g., from a targeted assay with a known set of analytes); PC selection is redundant.

## Inputs

- Metabolomic data matrix (samples × features) with possible missing values
- Metaboprep object containing imputed or raw abundance data in a specified source_layer (e.g., 'input')
- Optional: sample_ids and feature_ids filters to subset the analysis

## Outputs

- Vector of variance explained by each PC (up to min(n_samples, n_features) PCs)
- Acceleration factor result (numeric, indicating the elbow/inflection point)
- Parallel analysis result (data.frame or list with permuted PC variance thresholds and significance decisions)
- Scalar count of significant PCs (used to cap downstream analyses)
- PC eigenvectors for the top 10 PCs or top N significant PCs (whichever is smaller)

## How to apply

First, impute missing values to the median to create a complete data matrix. Then compute the full principal component decomposition and extract the variance explained by each PC. Apply acceleration analysis to identify the 'elbow' or inflection point where variance explanation rate decelerates sharply, indicating the transition from signal to noise. In parallel, run parallel analysis by permuting (randomizing) the input data structure and computing PC variances on the permuted data; PCs whose observed variance exceeds the permuted (95th percentile) variance are retained as statistically significant. The intersection or consensus of these two criteria (acceleration elbow + parallel analysis threshold) defines the final count of significant PCs. This count is then used to limit PC space for downstream outlier detection—e.g., only the top N significant PCs are used to identify sample outliers at 3 SD, 4 SD, and 5 SD thresholds, avoiding spurious outlier flagging from noise dimensions.

## Related tools

- **metaboprep** (R package that encapsulates pc_and_outliers() function, which internally performs acceleration analysis and parallel analysis to determine significant PC count and return eigenvectors and outlier counts) — https://github.com/MRCIEU/metaboprep
- **R** (Statistical computing environment in which acceleration and parallel analysis are implemented)
- **ggplot2** (R visualization package used to plot variance explained, scree plots, or acceleration curves to inspect PC selection results)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", pc_outlier_sd = 5); pc_result <- attr(mydata@feature_summary, "qc_pca_result"); n_sig_pcs <- length(pc_result$acceleration_factor)
```

## Evaluation signals

- Acceleration factor result is a single interpretable numeric value or inflection index (not NA or error); inspect the elbow visually or programmatically.
- Parallel analysis returns a comparison table with observed PC variances vs. permuted 95th percentile thresholds; number of 'significant' PCs is a positive integer ≤ min(n_samples, n_features).
- Variance explained vector is monotonically decreasing and sums to ≤ 100% (or the trace of the covariance matrix).
- Final count of significant PCs is less than or equal to the full dimensionality; when used downstream (e.g., pc_outlier_sd = 5), outlier counts do not increase spuriously because noise dimensions are excluded.
- Eigenvectors and variance explained are reproducible when the same random seed and input data are used for parallel analysis.

## Limitations

- Acceleration analysis is sensitive to noise structure and may not detect a sharp elbow in high-dimensional, heavily correlated data.
- Parallel analysis assumes the permutation null (i.i.d. randomization) is valid; violations (e.g., temporal or spatial structure in samples) can inflate or deflate significance thresholds.
- If max_num_pcs (e.g., 10) is set smaller than the number of available informative PCs, the algorithm will cap at max_num_pcs and log a warning but may miss latent structure.
- Missing data imputation (median) is a simple strategy that may not preserve correlation structure in highly skewed or multimodal metabolomic distributions; more sophisticated imputation (e.g., KNN, EM) may alter PC selection.
- Parallel analysis relies on permutation sampling and may be computationally expensive for very large datasets (n, p > 10,000).

## Evidence

- [other] The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs: "The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs"
- [other] The metaboprep package provides data filtering capabilities using a standard pipeline with user-defined thresholds, which includes outlier detection mechanisms applied to principal components at configurable standard deviation cutoffs.: "The metaboprep package provides data filtering capabilities using a standard pipeline with user-defined thresholds, which includes outlier detection mechanisms applied to principal components at"
- [other] Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result.: "Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result."
- [readme] Running sample data PCA outlier analysis at +/- 5 Sdev ... The stated max PCs [max_num_pcs=10] to use in PCA outlier assessment is greater than the number of available informative PCs [2]: "The stated max PCs [max_num_pcs=10] to use in PCA outlier assessment is greater than the number of available informative PCs [2]"
