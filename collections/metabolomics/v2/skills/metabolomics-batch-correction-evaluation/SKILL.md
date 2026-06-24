---
name: metabolomics-batch-correction-evaluation
description: Use when when you have log2-transformed metabolomics data with known
  batch assignments and biological groupings, and you need to validate that a batch
  correction method (such as CordBat) has successfully removed batch-driven variation
  without collapsing true group differences in metabolite.
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

# metabolomics-batch-correction-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate the efficacy of batch correction in metabolomics data by comparing PCA visualizations of uncorrected versus corrected metabolite matrices, assessing whether batch effects are removed while preserving biologically meaningful group structure.

## When to use

When you have log2-transformed metabolomics data with known batch assignments and biological groupings, and you need to validate that a batch correction method (such as CordBat) has successfully removed batch-driven variation without collapsing true group differences in metabolite composition.

## When NOT to use

- Input metabolite matrix is not log2-transformed or appropriately normalized before batch correction
- Batch and group assignments are missing, mismatched in length to samples, or contain undefined/inconsistent labels
- Biological group structure is absent or homogeneous (no true group effects expected); batch correction evaluation requires group-level signal to preserve

## Inputs

- log2-transformed metabolite abundance matrix (rows=samples, columns=metabolites)
- batch assignment vector (matching sample order)
- group assignment vector (matching sample order)
- reference batch label (string)

## Outputs

- PCA score data frame for uncorrected data (PC1, PC2, batch, group metadata)
- PCA score data frame for corrected data (PC1, PC2, batch, group metadata)
- ggplot2 visualization objects showing uncorrected vs. corrected PCA space colored by batch
- ggplot2 visualization objects showing uncorrected vs. corrected PCA space colored by group

## How to apply

Perform PCA with scaling (scale=TRUE) on the original metabolite matrix and record the PC1/PC2 scores and variance explained. Log2-transform the metabolite matrix, apply CordBat batch correction with appropriate batch vector, group vector, and reference batch specification, then back-transform the corrected matrix (2^corrected_mat). Re-perform PCA on the back-transformed data with scaling and compare PC1/PC2 scores, variance explained, and sample clustering patterns between the two projections. Visualize both PCA spaces side-by-side with ggplot2, coloring points by batch to assess batch mixing and by group to verify group separation is retained. Success is indicated by reduced within-batch variance and improved between-group separation after correction.

## Related tools

- **CordBat** (Applies concordance-based batch effect correction to log2-transformed metabolite matrices with specified batch, group, and reference batch parameters to produce corrected matrix fit$X.cor) — https://github.com/BorchLab/CordBat
- **prcomp** (Performs scaled principal component analysis on both uncorrected and back-transformed corrected metabolite data to generate comparable PCA score projections for evaluation)
- **ggplot2** (Creates side-by-side PCA scatter plots colored by batch and group to visualize the separation and clustering patterns in uncorrected versus corrected metabolomics data)
- **dplyr** (Combines PCA scores with batch and group metadata into tidy data frames for visualization and downstream comparison)

## Examples

```
fit <- CordBat(X = as.matrix(log2(cordbat_example[, met_cols])), batch = batch_vec, group = group_vec, ref.batch = 'Ref', grouping = FALSE); pca_uncor <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE); pca_cor <- prcomp(2^fit$X.cor, scale. = TRUE); ggplot(data.frame(pca_uncor$x, batch=batch_vec), aes(x=PC1, y=PC2, color=batch)) + geom_point()
```

## Evaluation signals

- PCA plot colored by batch shows reduced spatial clustering of same-batch samples after correction (batch effects diminished), whereas uncorrected plot shows clear batch-driven separation
- PCA plot colored by group retains or improves group-level separation after correction; group centroids should not collapse or shift adversely
- Within-batch variance (distance among samples labeled with the same batch) decreases after correction; between-group variance (distance among samples in different groups) is maintained or increases
- PC1 and PC2 loadings and variance explained per component show qualitatively different structure between uncorrected and corrected space, with corrected space exhibiting reduced batch-driven PC structure
- No systematic clustering of corrected samples by batch remains visible in the corrected PCA plot, while corrected samples retain identifiable grouping by biological group label

## Limitations

- Evaluation is limited to 2D PCA visualization; higher-dimensional batch structure or non-linear batch effects may not be fully apparent in PC1/PC2 space alone
- CordBat correction assumes multiplicative batch effects in log2-space; if batch effects are additive or non-linear in the original scale, correction efficacy may be compromised
- PCA evaluation assumes group signal is sufficiently strong relative to residual noise after correction; weak or subtle group effects may be masked or lost
- Visualization quality depends on having sufficient biological replicates and batch replicates; sparse designs may yield unreliable or misleading PCA patterns

## Evidence

- [other] CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor) that can be back-transformed and re-projected via PCA: "CordBat processes log2-transformed metabolite matrices by applying batch and group corrections, producing a corrected matrix (fit$X.cor) that can be back-transformed and re-projected via PCA (prcomp"
- [other] Create a data frame combining PCA scores (PC1, PC2) with batch and group metadata, then plot with ggplot2 colored by batch and group to visualize uncorrected data structure.: "Create a data frame combining PCA scores (PC1, PC2) with batch and group metadata, then plot with ggplot2 colored by batch and group to visualize uncorrected data structure."
- [methods] The batch effect is applied as a multiplicative factor to the baseline metabolite values: "The batch effect is applied as a multiplicative factor to the baseline metabolite values"
- [readme] Concordance-Based Batch Effect Correction for Large-Scale Metabolomics: "Concordance-Based Batch Effect Correction for Large-Scale Metabolomics"
- [methods] pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE): "pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE)"
- [methods] new_pca_res <- prcomp(2^corrected_mat, scale. = TRUE): "new_pca_res <- prcomp(2^corrected_mat, scale. = TRUE)"
