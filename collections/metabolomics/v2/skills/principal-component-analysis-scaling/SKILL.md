---
name: principal-component-analysis-scaling
description: Use when you have a log2-transformed metabolite abundance matrix and
  need to visualize sample clustering patterns, batch structure, or the effect of
  batch correction. Scaling is essential because metabolites often have widely different
  absolute concentrations;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - prcomp
  - CordBat
  - R
  - ggplot2
  - dplyr
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c05748
  title: CordBat
evidence_spans:
- pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE)
- fit <- CordBat( X = X_mat, batch = batch_vec, group = group_vec, ref.batch = "Ref",
  grouping = FALSE, print.detail = FALSE )
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# principal-component-analysis-scaling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Perform scaled principal component analysis (PCA) on metabolomics data matrices to project high-dimensional metabolite measurements into a lower-dimensional space while standardizing features to unit variance. This technique is used to visualize batch effects, group separation, and the efficacy of batch correction methods like CordBat on metabolomic samples.

## When to use

Apply this skill when you have a log2-transformed metabolite abundance matrix and need to visualize sample clustering patterns, batch structure, or the effect of batch correction. Scaling is essential because metabolites often have widely different absolute concentrations; without scaling, high-abundance metabolites would dominate the principal components and mask biologically meaningful separation.

## When NOT to use

- Input is already a pre-computed PCA object or projection (do not re-scale).
- Metabolite matrix is not log-transformed and contains zero or negative values (log transformation will fail).
- You need to identify specific metabolite contributors to batch effects (use loadings analysis or feature importance instead).

## Inputs

- log2-transformed metabolite abundance matrix (numeric data frame or matrix)
- sample metadata (batch labels, group labels)

## Outputs

- prcomp object containing eigenvalues, loadings, and scores
- data frame of PCA scores (PC1, PC2, … PCn) with sample metadata
- ggplot2 scatter plot(s) of principal components colored by batch and/or group

## How to apply

Extract metabolite abundance columns from your data frame into a numeric matrix. Log2-transform the matrix if not already transformed (e.g., log2(cordbat_example[, metabolite_cols])). Pass the matrix to prcomp() with scale.=TRUE to center and standardize each metabolite to unit variance before computing principal components. Extract the scores (sample coordinates in PC space) from the prcomp object and combine with metadata (batch, group, sample ID). Create scatter plots of PC1 vs PC2 colored by batch and group to assess clustering patterns. When evaluating batch correction, repeat this workflow on the back-transformed corrected matrix (e.g., 2^corrected_mat) and compare the resulting PCA plots visually — corrected data should show reduced batch clustering and preserved group separation.

## Related tools

- **prcomp** (Compute scaled PCA on log2-transformed metabolite matrix; scale.=TRUE standardizes each metabolite to unit variance before eigendecomposition)
- **ggplot2** (Visualize PCA scores as scatter plots; map PC1 and PC2 to x and y axes, color by batch and group metadata to assess clustering)
- **CordBat** (Generate corrected metabolite matrix (fit$X.cor) that can be back-transformed and re-projected via scaled PCA to evaluate batch correction efficacy) — https://github.com/BorchLab/CordBat
- **dplyr** (Prepare and manipulate PCA scores and metadata for downstream visualization and comparison)

## Examples

```
pca_res <- prcomp(log2(cordbat_example[, metabolite_cols]), scale. = TRUE); pca_df <- data.frame(pca_res$x[, 1:2], batch = batch_vec, group = group_vec); ggplot(pca_df, aes(PC1, PC2, color = batch, shape = group)) + geom_point(size = 3)
```

## Evaluation signals

- PCA scores data frame has one row per sample and columns for PC1, PC2, batch, group (schema check).
- Uncorrected PCA plot shows batch-driven clustering (samples from same batch cluster together); corrected plot shows reduced batch clustering with preserved group separation (visual comparison before/after).
- Scree plot or eigenvalue inspection shows that PC1 and PC2 explain a meaningful fraction of variance (e.g., >30% combined) for interpretability.
- Back-transformed corrected metabolite values are numeric and within the expected abundance range (e.g., no negative or NaN values after 2^X operation).
- Loadings (prcomp$rotation) reveal which metabolites drive separation; metabolites with large loadings on early PCs should be biologically interpretable or known batch markers.

## Limitations

- PCA assumes linear relationships between metabolites; non-linear batch effects or batch–group interactions may not be fully captured.
- Scaling to unit variance gives equal weight to all metabolites regardless of biological relevance or measurement noise; low-abundance or high-noise metabolites may contribute spurious signal.
- PCA is sensitive to outlier samples; extreme values can distort eigenvalues and loadings. Consider outlier detection or robust PCA variants for noisy metabolomics data.
- Two-dimensional visualization (PC1 vs PC2) captures only a subset of total variance; additional PCs or alternative visualization methods (e.g., UMAP, t-SNE) may reveal additional structure.

## Evidence

- [methods] prcomp with scale=TRUE standardizes metabolite features before PCA: "Perform PCA on metabolite data with scaling using prcomp. 2. Create a data frame combining PCA scores (PC1, PC2) with batch and group metadata, then plot with ggplot2 colored by batch and group"
- [methods] Log2-transform metabolite matrix before PCA: "Log2-transform the metabolite matrix, apply CordBat batch correction with reference batch 'Ref' and grouping=FALSE, then extract the corrected matrix"
- [methods] Back-transform corrected data and re-project via scaled PCA: "Perform PCA on the back-transformed (2^) corrected metabolite data with scaling, combine scores with metadata, and generate ggplot2 plots colored by batch and group"
- [methods] Scaled PCA visualizes batch effect separation and correction efficacy: "CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor) that can be back-transformed and re-projected via PCA (prcomp"
- [methods] Research question motivates scaled PCA comparison workflow: "How does CordBat batch correction affect the separation of samples in PCA space when applied to metabolomics data with simulated batch effects?"
