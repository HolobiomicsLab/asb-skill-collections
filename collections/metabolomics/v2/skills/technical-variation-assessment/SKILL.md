---
name: technical-variation-assessment
description: Use when when you have a preprocessed metabolomics matrix (log2-scaled, CSV format with batch identifiers in the first column) and need to determine whether technical variation is present, which correction model (ber, ber-bagging, parametric ComBat, or non-parametric ComBat) performs on your.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - dbnorm
  - R
  - sva
  - ber
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
---

# technical-variation-assessment

## Summary

Quantify and diagnose technical heterogeneity (batch effects and drift) in large metabolomics datasets using statistical models and unsupervised clustering visualization. This skill helps identify which batch-correction model best fits the data structure before applying normalization.

## When to use

When you have a preprocessed metabolomics matrix (log2-scaled, CSV format with batch identifiers in the first column) and need to determine whether technical variation is present, which correction model (ber, ber-bagging, parametric ComBat, or non-parametric ComBat) performs best on your specific data structure, and how much batch-driven variability each model removes from individual features.

## When NOT to use

- Input data is not log2-scaled or normalized; dbnorm requires scaled data to avoid overlooking high-abundance feature effects.
- Dataset contains >2000 features and you need real-time interactive visualization; Visodbnorm and dbnormSCORE are recommended for <2000 features for better computational speed.
- Batch identifiers are missing or inconsistent; batch annotation must be complete and unambiguous in the first column.

## Inputs

- Preprocessed metabolomics data matrix (CSV format, log2-scaled, rows=samples, columns=features)
- Batch annotation vector (batch identifiers, first column of input matrix or separate metadata)
- Optional: quality control (QC) replicates or analytical replicates with known batch assignments

## Outputs

- Adjusted R² table per feature per model (CSV)
- Model comparison score table with maximum Adjusted R² per model (CSV)
- PCA, Scree, Correlation, and RLA plots (PDF)
- Hierarchical clustering dendrograms for QC replicates before/after correction (PDF or Viewer output)
- Corrected metabolomics matrices for each tested model (CSV)

## How to apply

Load the log2-scaled metabolomics matrix (rows = samples, columns = features, batch column first) into R via dbnorm. Apply dbnormSCORE to compute adjusted R² for each feature under each correction model, generating a score table ranking model performance by maximum variability explained by batch; this identifies the best-fit model. Optionally visualize drift via Visodbnorm (PCA, Scree, RLA plots) for datasets with <2000 features to inspect spatial separation of batches and feature distribution before/after correction. Compare the Adjusted R-squared distributions across models: higher R² reduction indicates better batch removal. Use hclustdbnorm to evaluate dissimilarity between quality control replicates across batches before and after correction via hierarchical clustering with Pearson distance, confirming that identical samples cluster tightly after the selected correction model is applied.

## Related tools

- **dbnorm** (Primary package providing dbnormSCORE, Visodbnorm, hclustdbnorm, and individual model functions (dbnormBer, dbnormBagging, dbnormPcom, dbnormNPcom) for batch effect diagnostics and multi-model comparison) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat (parametric and non-parametric) models implemented within dbnorm for batch effect correction comparison) — http://bioconductor.org/packages/sva
- **R** (Execution environment for dbnorm functions and data I/O)
- **ber** (Legacy R package containing the ber function (two-stage procedure) for batch effect correction, archived and installed via devtools from CRAN archive) — https://cran.r-project.org/src/contrib/Archive/

## Examples

```
dbnormSCORE(data); dbnormBer(data); dbnormPcom(data); dbnormNPcom(data); hclustdbnorm(data)
```

## Evaluation signals

- Adjusted R² values decrease substantially (e.g., >50% reduction) after applying the selected correction model, indicating batch-driven variance has been removed from most features.
- Model comparison score table shows consistent ranking: one model achieves highest mean/median Adjusted R² across features, identifying the best-fit correction approach for that dataset structure.
- PCA plots show clear spatial separation of batches in raw data (distinct clusters per batch) that collapse or become homogeneous after correction, with PC1 or PC2 no longer correlating with batch.
- RLA (Relative Log Abundance) plots shift from biased (median far from zero) to centered distributions (median near zero) after correction, confirming removal of systematic drift.
- Hierarchical clustering dendrograms show that identical QC replicates analyzed in different batches cluster together (low Pearson distance) after correction but were dispersed before correction.

## Limitations

- Computational speed decreases for datasets with >2000 features; Visodbnorm and dbnormSCORE designed for <2000 features; use individual model functions (dbnormBer, dbnormPcom, etc.) for larger datasets.
- ber function originally developed for microarray gene expression; performance on metabolomics data must be validated empirically with dbnormSCORE before deployment.
- Requires complete batch metadata; missing or mislabeled batch identifiers invalidate assessment and correction.
- No changelog available for dbnorm package versions, limiting reproducibility across versions; version specification (V-0.2.2) should be documented.
- Assessment assumes data are already preprocessed, normalized, and log2-scaled; raw or inadequately scaled data may yield misleading batch effect estimates.

## Evidence

- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables)"
- [readme] dbnormSCORE computes adjusted coefficient of determination for features under each model and generates a performance score: "the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] Visodbnorm generates visual inspection via PCA, Scree, and RLA plots for datasets with <2000 features: "This function is suggested for less than 2000 features (variables). Graphical check such as *PCA* plot and *Scree* plot"
- [readme] hclustdbnorm evaluates dissimilarity between QC replicates across batches before and after correction: "This function allows users to evaluate dissimilarity between identical samples (quality control replicates or analytical replicates) analyzed in different batches, prior and after correction"
- [intro] dbnorm implements ber function alongside ComBat models for batch effect correction in metabolomics: "dbnorm package implements the ber function as one of several statistical models for batch effect correction, alongside ComBat parametric and non-parametric models"
