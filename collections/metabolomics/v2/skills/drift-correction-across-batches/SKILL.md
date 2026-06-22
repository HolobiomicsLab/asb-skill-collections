---
name: drift-correction-across-batches
description: Use when your preprocessed metabolomics matrix (log2-scaled, with rows as features and columns as samples) exhibits batch-dependent signal drift or technical variation across multiple analytical runs or instrument sessions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - dbnorm
  - sva
  - R
  - ber
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]
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

# drift-correction-across-batches

## Summary

Correct systematic signal drift and batch effects in preprocessed metabolomics datasets using statistical models (ComBat parametric/non-parametric or ber function) implemented in dbnorm. Apply this skill when metabolomics features show technical heterogeneity or signal shifts across analytical batches that obscure biological variation.

## When to use

Your preprocessed metabolomics matrix (log2-scaled, with rows as features and columns as samples) exhibits batch-dependent signal drift or technical variation across multiple analytical runs or instrument sessions. Batch assignment metadata is available and independent samples or quality control replicates have been analyzed in different batches. You have fewer than 2000 features for faster computational performance with visualization functions.

## When NOT to use

- Input matrix is not log2-scaled or normalized; apply log2-transformation and intensity normalization first.
- Batch labels are missing or incomplete; batch assignment metadata must be available for all samples.
- Metabolomics matrix has been already corrected for batch effects by another method; applying sequential corrections may introduce artificial structure.

## Inputs

- Preprocessed metabolomics matrix (CSV format: samples × features, log2-scaled)
- Batch assignment vector or metadata (batch labels for each sample)
- Optional: quality control or replicate sample annotations for validation

## Outputs

- Batch-corrected metabolomics matrix (CSV format, same structure as input)
- Adjusted R-squared scores per feature and per model (CSV files)
- Diagnostic visualizations: PCA plots, RLA plots, probability density function (PDF) plots, scree plots, correlation plots (PDF files)
- Model performance score summary table (CSV file)

## How to apply

Load the log2-scaled metabolomics matrix (CSV format: samples in rows, features in columns, batch labels in the first column) and batch assignment vector into R. Estimate missing values (zeros or NAs) using either emvd (dataset-wide minimum) or emvf (feature-wise minimum) imputation. Select a correction model: ComBat parametric or non-parametric (from sva package, suitable for large datasets with complex batch structures) or ber two-stage procedure (suitable when batch effects are prominent and drift must be explicitly modeled). Apply the chosen model via dbnormBer(), dbnormPcom(), or dbnormNPcom(). Evaluate model performance using dbnormSCORE() to compute adjusted R-squared per feature before and after correction, comparing the maximum variability explained by batch level across models. Export the corrected matrix in the same format (rows=features, columns=samples) for downstream analysis.

## Related tools

- **dbnorm** (Primary package providing batch effect correction functions (dbnormBer, dbnormPcom, dbnormNPcom), diagnostic scoring (dbnormSCORE), and visualization (Visodbnorm, ProfPlot*) for metabolomics datasets) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat parametric and non-parametric empirical Bayes models for batch effect correction, called via dbnorm wrapper functions)
- **R** (Statistical computing environment for executing dbnorm functions and data import/export workflows)
- **ber** (Legacy R package implementing two-stage batch effect correction procedure, installable from CRAN archive and integrated into dbnorm)

## Examples

```
library(dbnorm)
data <- read.csv('metabolomics_log2_scaled.csv', sep=',', header=TRUE, row.names=1)
df <- emvf(data[-1])
dbnormSCORE(data)
dbnormPcom(data)
```

## Evaluation signals

- Adjusted R-squared values decrease after correction: batch explains less variance in corrected features than in raw data for each applied model.
- PCA and RLA plots show reduced spatial separation or clustering by batch label in corrected data compared to raw data; samples from the same biological condition cluster similarly regardless of batch.
- Probability density function (PDF) profiles of features shift back toward a common distribution after correction; shifted PDFs in raw data normalize in treated data.
- Model performance score (dbnormSCORE output) shows low and consistent maximum adjusted R-squared across all features for the selected model, indicating homogeneous batch effect removal.
- Hierarchical clustering (hclustdbnorm) shows reduced dissimilarity between quality control replicates or identical samples analyzed in different batches after correction.

## Limitations

- Visualization functions (Visodbnorm, dbnormSCORE, profile plots) are recommended for datasets with fewer than 2000 features; larger datasets may incur computational overhead or slow visualization rendering.
- ComBat and ber models assume that batch effects are additive or multiplicative; non-linear batch interactions or feature-specific batch patterns may not be fully corrected.
- dbnorm version 0.2.2 (current in documentation) has no published changelog; users cannot easily verify which bugs or features are present across versions.
- Input data must be in CSV format with specific structure (samples in rows, features in columns, batch in first column); metadata in other formats requires manual reformatting.
- Correction model selection requires user judgment based on dbnormSCORE and visualizations; no automated model selection or consensus weighting across models is provided by dbnorm.

## Evidence

- [intro] dbnorm allows visualization and removal of technical heterogeneity from large metabolomics datasets: "*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity from large metabolomics dataset"
- [readme] dbnorm implements ComBat (parametric and non-parametric) models from the sva package as conventional functions for batch effect correction: "ComBat(parametric and non-parametric)-model from sva package, that was already in use for metabolomics data normalization"
- [readme] ber function was originally developed for microarray data and is now proposed for metabolomics batch correction via dbnorm: "ber function, priorly developed for microarray gene expression data, that we propose here as a new approach for correction of drift across batch in metabolomics datasets"
- [intro] dbnorm includes 11 distinct functions for pre-processing, missing value estimation, batch correction, and diagnosis plots: "*dbnorm* includes 11 distinct functions for pre-processing of data and estimation of missing values, conventional functions for batch effect correction based on statistical models"
- [readme] Visualization functions are recommended for datasets with fewer than 2000 features: "This function is suggested for less than 2000 features (variables)"
- [readme] dbnormSCORE computes adjusted R-squared for each variable before and after correction to assess model performance: "the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] Input data must be normalized and scaled to log2 and in CSV format with specific column/row structure: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables). The input data must be in **.csv** format with the independent experiments in the"
