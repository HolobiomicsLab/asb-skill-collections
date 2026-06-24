---
name: metabolomics-matrix-manipulation-r
description: Use when you have a log2-scaled metabolomics feature matrix in CSV format
  with samples in rows, metabolic features in columns, and batch identifiers in the
  first column, and you need to remove technical heterogeneity or drift across analytical
  batches before estimating biological mechanisms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - dbnorm
  - R
  - sva
  license_tier: restricted
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical
  heterogeneity'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41598-021-84824-3
  all_source_dois:
  - 10.1038/s41598-021-84824-3
  - 10.1007/s12561-013-9081-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-matrix-manipulation-r

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load, preprocess, and apply batch effect correction to metabolomics feature matrices in R using the dbnorm package. This skill enables transformation of raw metabolomics data (log2-scaled, CSV format) into batch-corrected matrices suitable for downstream biological inference.

## When to use

You have a log2-scaled metabolomics feature matrix in CSV format with samples in rows, metabolic features in columns, and batch identifiers in the first column, and you need to remove technical heterogeneity or drift across analytical batches before estimating biological mechanisms underlying disease or medical state.

## When NOT to use

- Data are not log2-scaled or have not been normalized (use normalization step first)
- Input is not in CSV format with samples in rows and features in columns
- Batch identifiers are not provided or annotated in the first column
- Feature count exceeds 2000 (Visodbnorm and dbnormSCORE have computational limits; use individual model functions instead)

## Inputs

- Metabolomics feature matrix (CSV format: log2-scaled, samples×features, batch identifiers in column 1)
- Batch annotation metadata (batch level indicators)
- Missing value indicators (zeros or NA values)

## Outputs

- Batch-corrected metabolomics matrix (CSV format)
- Diagnostic plots (PCA, Scree, RLA, Correlation, Score plots in PDF)
- Adjusted R-squared performance metrics (CSV)
- Model selection recommendation based on score comparison

## How to apply

First, load the preprocessed metabolomics matrix and batch annotation metadata using read.csv() in R, ensuring data is log2-scaled to account for high-abundance features. Estimate missing values (zeros or NAs) using either emvd() (lowest value across entire experiment) or emvf() (lowest value per feature). Then apply one of the statistical models for batch correction—ber (two-stage procedure), ber-bagging, parametric ComBat, or non-parametric ComBat—via corresponding dbnorm functions (dbnormBer, dbnormBagging, dbnormPcom, dbnormNPcom). Use dbnormSCORE() or Visodbnorm() to evaluate model performance via adjusted R-squared and visual inspection (PCA, RLA, correlation plots) before selecting the best-fitting model. Extract and save the corrected metabolomics matrix from the temporary directory output.

## Related tools

- **dbnorm** (Main package providing ber, ber-bagging, ComBat parametric/non-parametric batch correction functions, missing value estimation (emvd, emvf), performance scoring (dbnormSCORE), visualization (Visodbnorm, profile plots), and hierarchical clustering validation (hclustdbnorm)) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat empirical Bayes methods (parametric and non-parametric) used alongside ber within dbnorm)
- **R** (Runtime environment for loading data, executing dbnorm functions, and generating corrected matrices and diagnostics)

## Examples

```
data <- read.csv('path/to/metabolomics.csv', sep=',', header=T, row.names=1); library(dbnorm); df <- data[-1]; f <- emvd(df); dbnormSCORE(data); corrected <- dbnormBer(data)
```

## Evaluation signals

- Adjusted R-squared increases after batch correction relative to raw data (visible in dbnormSCORE CSV output); batch effect no longer explains maximum variance in feature-level regression
- PCA plot shows spatial overlap or separation consistency between samples from different batches after correction (visual inspection of PCA plots in output PDF)
- RLA (Relative Log Abundance) plots show median near zero and reduced spread across batches in corrected data (viewable in RStudio Viewer)
- Hierarchical clustering (hclustdbnorm) shows increased similarity (smaller Pearson distance) between replicate samples analyzed in different batches
- Profile plots (ProfPlot* functions) show shifted probability density functions converging toward common distribution across batches in corrected data

## Limitations

- Visodbnorm and dbnormSCORE recommended for <2000 features only; use individual model functions (dbnormBer, dbnormPcom, etc.) for larger datasets to avoid computational slowdown
- Data must be log2-scaled before input; high-abundance features can otherwise obscure technical heterogeneity
- No changelog available; version 0.2.2 is current but reproducibility across future versions not guaranteed
- ber function originally developed for microarray data; its performance on metabolomics data depends on data structure and should be validated via dbnormSCORE before use
- Output files saved to system temporary directory (Windows: C:\Users\%USERNAME%\AppData\Local\Temp); may be deleted by OS or require manual archival

## Evidence

- [readme] dbnorm contains R functions which allow visualization and removal of technical heterogeneity from large metabolomics datasets: "*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity from large metabolomics dataset"
- [readme] Data preprocessing and missing value estimation requirements: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked"
- [readme] Core workflow: missing value estimation followed by batch correction model selection: "functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure"
- [readme] ber function adaptation to metabolomics and performance evaluation: "ber function [DOI:10.1007/s12561-013-9081-1], priorly developed for microarray gene expression data, that we propose here as a new approach for correction of drift across batch in metabolomics"
- [readme] Computational limits for visualization functions: "This function is suggested for less than 2000 features (variables)"
- [readme] Hierarchical clustering validation approach: "This function allows users to evaluate dissimilarity between identical samples (quality control replicates or analytical replicates) analyzed in different batches, prior and after correction"
