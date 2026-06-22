---
name: metabolite-data-log-transformation
description: Use when you have raw or baseline-corrected metabolite abundance measurements from mass spectrometry and need to prepare them for batch effect correction (e.g., CordBat) or multivariate analysis (e.g., PCA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - prcomp
  - CordBat
  - R
  - ggplot2
derived_from:
- doi: 10.1021/acs.analchem.2c05748
  title: CordBat
evidence_spans:
- pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE)
- fit <- CordBat( X = X_mat, batch = batch_vec, group = group_vec, ref.batch = "Ref", grouping = FALSE, print.detail = FALSE )
- '%\VignetteEngine{knitr::rmarkdown}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cordbat_cq
    doi: 10.1021/acs.analchem.2c05748
    title: CordBat
  dedup_kept_from: coll_cordbat_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05748
  all_source_dois:
  - 10.1021/acs.analchem.2c05748
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-data-log-transformation

## Summary

Log2-transform raw metabolite abundance matrices prior to batch correction or statistical analysis in metabolomics. This preprocessing step stabilizes variance across the wide dynamic range typical of mass spectrometry data and prepares the matrix for concordance-based batch correction algorithms like CordBat.

## When to use

Apply this skill when you have raw or baseline-corrected metabolite abundance measurements from mass spectrometry and need to prepare them for batch effect correction (e.g., CordBat) or multivariate analysis (e.g., PCA). Log2 transformation is especially important when the metabolite matrix spans multiple orders of magnitude in intensity and batch-correction algorithms expect log-scale input.

## When NOT to use

- Data already in log-scale (log2, log10, or natural log) — double-transformation will invert the correction.
- Metabolite abundances contain zero or negative values — log2 will produce -Inf or NaN; impute or add pseudocounts first.
- Abundance matrix is already normalized by a method that assumes linear scale (e.g., quantile normalization without log-scale assumption).

## Inputs

- data frame with metabolite abundance columns (numeric, non-negative)
- character vector of metabolite column names or numeric indices

## Outputs

- log2-transformed metabolite matrix (numeric matrix, log2-scale)

## How to apply

Extract the metabolite abundance columns (e.g., Metabolite1–Metabolite25) from your data frame into a numeric matrix. Apply log2 transformation to the entire matrix using R's log2() function, converting it to a matrix if needed: X_mat <- as.matrix(log2(data[, metabolite_cols])). The resulting log2-scale matrix becomes the input X parameter to batch-correction tools like CordBat(). After batch correction and extraction of the corrected matrix (fit$X.cor), back-transform via exponentiation (2^corrected_mat) before downstream visualization or statistical analysis. This preserves the mathematical properties expected by the batch-correction algorithm while allowing intuitive interpretation of corrected abundances.

## Related tools

- **CordBat** (Batch-correction algorithm that accepts log2-transformed metabolite matrices as input (X parameter) and outputs corrected abundance matrices in log2 scale) — https://github.com/BorchLab/CordBat
- **prcomp** (R function for PCA; applied to back-transformed (2^) corrected metabolite data to visualize batch-correction efficacy)
- **ggplot2** (Visualization library used to plot PCA scores derived from log2-transformed and batch-corrected metabolite data)

## Examples

```
X_mat <- as.matrix(log2(cordbat_example[, c('Metabolite1', 'Metabolite2', 'Metabolite25')]))
```

## Evaluation signals

- Output matrix has same dimensions (rows, columns) as input before log transformation.
- All values in the output are finite (no -Inf, +Inf, or NaN); if present, raw data contained zeros or negative values.
- Distribution of log2-transformed values is approximately symmetric (roughly normal) compared to right-skewed raw abundances.
- PCA performed on log2-transformed corrected data (after 2^ back-transformation) shows batch clusters resolved better than uncorrected data, indicating successful preprocessing.
- Back-transformed corrected matrix (2^fit$X.cor) values are positive and within the expected biological range for metabolite abundances.

## Limitations

- Log2 transformation requires all input abundances to be strictly positive; zeros or negative values must be handled (e.g., pseudocount addition) before transformation.
- Log2 scale assumes multiplicative batch effects; if batch effects are additive on the raw scale, log transformation may not linearize them optimally.
- Back-transformation (2^) can amplify rounding errors from batch correction, especially for low-abundance metabolites near the detection limit.
- CordBat batch correction is designed for log-scale input; applying it to untransformed data or other log bases may produce unreliable or unstable fits.

## Evidence

- [methods] Log2-transform the metabolite matrix and prepare batch and group vectors from metadata.: "Log2-transform the metabolite matrix and prepare batch and group vectors from metadata."
- [other] CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor).: "CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor)"
- [other] Perform PCA on the back-transformed (2^) corrected metabolite data with scaling.: "Perform PCA on the back-transformed (2^) corrected metabolite data with scaling"
- [methods] X_mat <- as.matrix(log2(cordbat_example[met_cols])): "X_mat      <- as.matrix(log2(cordbat_example[met_cols]))"
- [readme] Concordance-Based Batch Effect Correction for Large-Scale Metabolomics: "Concordance-Based Batch Effect Correction for Large-Scale Metabolomics"
