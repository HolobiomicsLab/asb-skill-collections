---
name: ggplot2-multivariate-scatter-visualization
description: Use when after performing PCA (or other dimensionality reduction) on a metabolite matrix, when you need to visualize whether batch effects are present in uncorrected data, or whether a batch correction method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2501
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - prcomp
  - ggplot2
  - CordBat
  - R
  - dplyr
derived_from:
- doi: 10.1021/acs.analchem.2c05748
  title: CordBat
evidence_spans:
- pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE)
- library(ggplot2)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ggplot2-multivariate-scatter-visualization

## Summary

Create publication-ready 2D scatter plots of multivariate data (e.g., PCA scores) colored by categorical metadata (batch, group) to visually assess sample clustering and batch correction efficacy. This skill enables side-by-side comparison of uncorrected vs. corrected metabolomics data in reduced dimensionality space.

## When to use

After performing PCA (or other dimensionality reduction) on a metabolite matrix, when you need to visualize whether batch effects are present in uncorrected data, or whether a batch correction method (e.g., CordBat) successfully removes batch-driven clustering while preserving biological group structure. Trigger: you have PCA scores (PC1, PC2), sample-level batch annotations, and group annotations.

## When NOT to use

- Input data has not been centered and scaled — prcomp must be run with scale=TRUE before extracting scores for visualization.
- Batch or group metadata contain missing or mismatched sample labels — all samples in PCA scores must have corresponding batch and group assignments.
- More than 2–3 principal components are needed to explain batch/group structure — scatter plot interpretation becomes unreliable; consider interactive 3D plots or other dimensionality reduction methods.

## Inputs

- log2-transformed metabolite matrix (rows = samples, columns = metabolites)
- batch vector (sample-level batch labels)
- group vector (sample-level group labels)
- PCA scores data frame (PC1, PC2, batch, group)

## Outputs

- ggplot2 scatter plot object colored by batch
- ggplot2 scatter plot object colored by group
- paired comparison figures (uncorrected vs. corrected)

## How to apply

Extract PC1 and PC2 scores from a prcomp object and combine them with batch and group metadata into a data frame. Use ggplot2 to map PC1 to the x-axis, PC2 to the y-axis, and color aesthetic to batch or group. Generate two paired plots (uncorrected and corrected data) to visually compare how batch correction redistributes samples in PCA space. The rationale: batch-corrected data should show reduced batch-driven clustering (points colored by batch should overlap more) while retaining group separation if biological signal is preserved. Scale PCA input data (scale=TRUE in prcomp) to ensure all metabolites contribute equally.

## Related tools

- **prcomp** (Performs PCA on scaled metabolite matrix; outputs scores (PC1, PC2, …) to be plotted)
- **ggplot2** (Creates scatter plots mapping PCA scores to aesthetics (x, y, color) to visualize sample clustering by batch or group)
- **CordBat** (Produces corrected metabolite matrix (fit$X.cor) that is back-transformed and re-projected via PCA for comparison with uncorrected PCA plot) — https://github.com/BorchLab/CordBat
- **dplyr** (Data frame manipulation to combine PCA scores with metadata)

## Examples

```
pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE); pca_df <- data.frame(PC1=pca_res$x[,'PC1'], PC2=pca_res$x[,'PC2'], batch=batch_vec, group=group_vec); ggplot(pca_df, aes(x=PC1, y=PC2, color=batch)) + geom_point(size=3) + theme_minimal()
```

## Evaluation signals

- Uncorrected data shows tight clustering of samples by batch in PCA space (e.g., all Batch_A samples occupy one region, Batch_B another), indicating strong batch effects.
- Corrected data shows batch-driven clusters dissolved (samples from different batches intermix) while biological group separation is preserved or enhanced.
- All samples in PCA scores data frame have valid batch and group assignments with no missing values; sample counts match between PCA output and metadata.
- PC1 and PC2 axis labels report the percentage of variance explained (e.g., 'PC1 (35.2%)', 'PC2 (18.9%)'); total variance should be reasonable for metabolomics data.
- Visual inspection confirms that the corrected plot does not collapse all groups into one cluster — biological signal is retained.

## Limitations

- PCA captures only linear variance structure; non-linear batch effects or confounders not aligned with principal components may not be visible.
- Visualization limited to 2D (PC1 vs. PC2); if batch/group structure exists primarily in PC3 or higher, the 2D scatter plot may be misleading.
- CordBat corrects with reference batch 'Ref' and grouping=FALSE; if grouping=TRUE, correction strategy differs and may produce different visual outcomes.
- Batch correction success (visual separation) does not guarantee statistical significance or biological validity; complementary statistical tests (e.g., PERMANOVA) are recommended.

## Evidence

- [methods] Create a data frame combining PCA scores (PC1, PC2) with batch and group metadata, then plot with ggplot2 colored by batch and group to visualize uncorrected data structure.: "Create a data frame combining PCA scores (PC1, PC2) with batch and group metadata, then plot with ggplot2 colored by batch and group to visualize uncorrected data structure."
- [methods] Perform PCA on the back-transformed (2^) corrected metabolite data with scaling, combine scores with metadata, and generate ggplot2 plots colored by batch and group to visualize corrected data structure.: "Perform PCA on the back-transformed (2^) corrected metabolite data with scaling, combine scores with metadata, and generate ggplot2 plots colored by batch and group to visualize corrected data"
- [methods] pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE): "pca_res <- prcomp(cordbat_example[, metabolite_cols], scale. = TRUE)"
