---
name: batch-effect-visualization-pca
description: Use when after applying CordBat batch correction to a log2-transformed metabolite matrix from multi-batch metabolomics data, you want to quantitatively and visually assess whether the correction successfully reduced batch effects.
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
---

# Batch-effect visualization via PCA

## Summary

Visualize the impact of batch correction on metabolomics sample clustering by performing PCA on uncorrected and corrected log2-transformed metabolite matrices, then comparing their principal component projections colored by batch and group metadata. This skill enables direct assessment of whether batch correction reduces batch-driven separation while preserving group structure.

## When to use

After applying CordBat batch correction to a log2-transformed metabolite matrix from multi-batch metabolomics data, you want to quantitatively and visually assess whether the correction successfully reduced batch effects. Compare PCA plots of the same samples before and after correction to evaluate clustering homogeneity within groups and separation between batches.

## When NOT to use

- Your metabolite matrix has already been batch-corrected by another method; this skill is designed to evaluate CordBat specifically
- You lack batch and group metadata or cannot assign samples to experimental batches and groups
- Your data has not been log-transformed prior to CordBat application; the workflow assumes log2 scale for input to CordBat

## Inputs

- metabolite matrix (samples × metabolites, numeric)
- batch assignment vector (factor or character, length = n_samples)
- group assignment vector (factor or character, length = n_samples)
- reference batch identifier (character, single value)
- uncorrected metabolite measurements (raw or normalized but not batch-corrected)

## Outputs

- PCA scores data frame (uncorrected: PC1, PC2, batch, group metadata)
- PCA scores data frame (corrected: PC1, PC2, batch, group metadata)
- ggplot2 scatter plot (uncorrected PCA colored by batch)
- ggplot2 scatter plot (uncorrected PCA colored by group)
- ggplot2 scatter plot (corrected PCA colored by batch)
- ggplot2 scatter plot (corrected PCA colored by group)

## How to apply

Extract metabolite columns from your dataset and perform PCA with scaling (prcomp with scale=TRUE) on the raw (uncorrected) metabolite matrix to establish the baseline clustering structure. Log2-transform the metabolite matrix, apply CordBat batch correction with reference batch and grouping parameters appropriate to your experimental design, then extract the corrected matrix (fit$X.cor). Back-transform the corrected matrix (2^corrected_mat), perform PCA with scaling on the back-transformed data, and create paired ggplot2 visualizations coloring points by batch and group. Compare the two PCA plots: successful batch correction should show reduced clustering by batch in the corrected plot while group separation is maintained or improved. Use PC1 and PC2 as the primary visualization axes unless variance explained suggests otherwise.

## Related tools

- **CordBat** (Applies concordance-based batch effect correction to log2-transformed metabolite matrix; produces corrected matrix fit$X.cor for downstream PCA) — https://github.com/BorchLab/CordBat
- **prcomp** (Performs scaled principal component analysis on both uncorrected and back-transformed corrected metabolite matrices to generate PC scores)
- **ggplot2** (Creates side-by-side scatter plots of PCA scores colored by batch and group to enable visual comparison of uncorrected vs. corrected sample clustering)
- **dplyr** (Data manipulation utility for combining PCA scores with metadata into visualization-ready data frames)

## Examples

```
pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE); X_mat <- as.matrix(log2(cordbat_example[met_cols])); fit <- CordBat(X = X_mat, batch = batch_vec, group = group_vec, ref.batch = "Ref", grouping = FALSE); new_pca_res <- prcomp(2^fit$X.cor, scale. = TRUE)
```

## Evaluation signals

- Uncorrected PCA plot should show distinct clustering by batch; corrected PCA plot should show reduced batch-driven separation with samples from same batch now more dispersed
- Group structure (if present) should remain visible or be enhanced in corrected plot; group samples should cluster together even after batch correction
- Variance explained by PC1 and PC2 combined should be similar between uncorrected and corrected plots; if corrected plot has much lower variance on first two components, investigate dimensionality reduction artifacts
- Visual inspection confirms that corrected samples from different batches no longer form distinct clusters in PCA space, indicating successful batch removal
- Back-transformed corrected matrix (2^corrected_mat) should have similar mean and variance structure to original uncorrected matrix, confirming data integrity after correction and back-transformation

## Limitations

- PCA visualization is limited to 2–3 dimensions; batch effects and group structure in higher PCs may not be visible. Inspect scree plot to confirm PC1 and PC2 capture sufficient variance.
- CordBat applies multiplicative batch and group corrections; if your batch effects are non-linear or dataset-specific, the corrected matrix may not fully remove all batch-driven variation visible in PCA.
- The skill assumes log2-transformed input to CordBat; other transformations (e.g., square root, Box–Cox) are not covered by the documented workflow and may produce incorrect results when back-transformed.
- Visual assessment of batch correction is subjective; formal quantitative metrics (e.g., silhouette score, batch correction metrics from tools like ComBat_Seq) may provide additional rigor but are not included in this skill.

## Evidence

- [other] CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor) that can be back-transformed and re-projected via PCA: "CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor) that can be back-transformed and re-projected via PCA (prcomp"
- [other] Log2-transform the metabolite matrix, apply CordBat batch correction with reference batch and grouping parameters, then extract and back-transform the corrected matrix for PCA re-projection: "Log2-transform the metabolite matrix, apply CordBat batch correction with reference batch 'Ref' and grouping=FALSE, then extract the corrected matrix. Perform PCA on the back-transformed (2^)"
- [other] Create PCA visualizations colored by batch and group to compare uncorrected vs. corrected sample structure: "Create a data frame combining PCA scores (PC1, PC2) with batch and group metadata, then plot with ggplot2 colored by batch and group to visualize uncorrected data structure"
- [methods] The synthetic dataset is engineered to mirror realistic mass spectrometry outputs by simulating 25 metabolites across six distinct batches: "The synthetic dataset is engineered to mirror realistic mass spectrometry outputs by simulating 25 metabolites across six distinct batches"
- [readme] CordBat is a R package implementation of Concordance-Based Batch Effect Correction for Large-Scale Metabolomics: "This is a R package implementation of the Concordance-Based Batch Effect Correction for Large-Scale Metabolomics (CordBat)"
