---
name: statistical-model-selection-assessment
description: Use when after loading preprocessed metabolomics data (log-transformed feature abundance matrices with samples as rows, features as columns, and batch annotations) but before applying batch-effect correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva
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

# statistical-model-selection-assessment

## Summary

Assess which batch-effect correction statistical model (parametric ComBat, non-parametric ComBat, or two-stage ber procedure) best fits metabolomics data structure by generating diagnostic visualizations and performance scores. This skill enables data-driven model selection before committing to full batch correction.

## When to use

After loading preprocessed metabolomics data (log-transformed feature abundance matrices with samples as rows, features as columns, and batch annotations) but before applying batch-effect correction. Use this skill when you have multiple candidate statistical models and need to determine which one removes batch drift most effectively without introducing artifacts specific to your dataset's structure, drift pattern, and feature distribution.

## When NOT to use

- Input data is already known to contain true biological batch structure (e.g., intended treatment groups confounded with batch); use caution as model selection may remove biological signal.
- Dataset contains fewer than ~20 samples or fewer than ~50 features; diagnostic plots and score distributions become unreliable with very sparse data.
- Batch effects have already been corrected or batch metadata is unavailable; model selection assessment requires both uncorrected data and batch annotations.

## Inputs

- Preprocessed metabolomics data matrix (CSV format: samples as rows, features as columns, batch identifiers in first column)
- Log-transformed feature abundance table (log2 scale to normalize high-abundance features)
- Batch annotation metadata (batch level identifiers for all samples)

## Outputs

- PCA plots (showing sample-batch clustering before and after correction)
- Scree plots (variance explained by principal components)
- RLA (Relative Log Abundance) plots (distribution of log-ratios across samples)
- Correlation plots (pairwise feature correlations pre- and post-correction)
- Probability density function (PDF) profile plots (feature distribution shifts by batch)
- Adjusted R-squared scores for each feature under each model (CSV)
- Model performance score table (maximum Adjusted R-squared and consistency metrics)
- PDF files compiled with all diagnostic visualizations (saved to working directory)

## How to apply

Load corrected and uncorrected metabolomics data matrices into R, then invoke diagnostic functions (Visodbnorm, dbnormSCORE, or individual ProfPlot* functions) that generate PCA plots, Scree plots, RLA (Relative Log Abundance) plots, correlation plots, and probability density function (PDF) profile plots comparing raw versus model-corrected data. For each candidate model (ber, ber-bagging, parametric ComBat, non-parametric ComBat), calculate the adjusted coefficient of determination (Adjusted R-squared) to quantify how much batch-level variance each model removes from each feature. Examine score tables that rank model performance by maximum Adjusted R-squared across all features and consistency of performance. Select the model that achieves the highest and most consistent Adjusted R-squared values while showing clear visual separation of batch clusters in PCA space and minimal over-correction artifacts in PDF profiles. This function is recommended for datasets with fewer than 2000 features for optimal computational speed.

## Related tools

- **dbnorm** (Implements diagnostic plot functions (Visodbnorm, dbnormSCORE, ProfPlot* suite) and batch-effect correction models for metabolomics; generates visual and quantitative comparison of parametric ComBat, non-parametric ComBat, ber, and ber-bagging models) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat parametric and non-parametric empirical Bayes methods for batch effect correction; models evaluated by dbnorm diagnostic functions) — http://bioconductor.org/packages/sva
- **R** (Execution environment for dbnorm functions; supports graphics rendering (ggplot2) and statistical computations underlying diagnostic assessment)

## Examples

```
library(dbnorm); data <- read.csv('metabolomics_batch_annotated.csv', sep=',', header=T, row.names=1); dbnormSCORE(data)
```

## Evaluation signals

- Diagnostic PCA plots show clear batch cluster separation and reduction in batch-driven clustering after model correction, indicating effective batch removal.
- Adjusted R-squared values decrease from raw to corrected data (batch explains less variance post-correction) and are consistent (low standard deviation) across features for the selected model, indicating stable and uniform batch removal.
- PDF profile plots of corrected data show overlapping feature distributions across batches (reduced shift), whereas raw data exhibits batch-specific distribution shifts.
- RLA plots demonstrate reduced log-ratio variability across samples post-correction, with no systematic drift or outlier artifacts introduced by the model.
- Model performance score table identifies one model with highest maximum Adjusted R-squared and highest consistency rank; visualizations support this ranking without contradictory patterns.

## Limitations

- Diagnostic assessment is computationally intensive and recommended for ≤2000 features; performance degrades and runtime increases significantly beyond this threshold.
- Visual inspection of plots is subjective; automated ranking by Adjusted R-squared may not capture all aspects of data quality (e.g., preservation of biological structure or reproducibility of quality control replicates evaluated by hclustdbnorm).
- Adjusted R-squared metric assumes batch effects are linear and additive; non-linear or multiplicative batch interactions may not be fully captured by statistical diagnostics.
- Model selection is data-structure-specific; a model ranking well on one metabolomics dataset may not generalize to datasets with different drift patterns, feature distributions, or batch designs.

## Evidence

- [readme] functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure: "functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure"
- [other] Generate diagnosis plots comparing corrected versus uncorrected data to highlight the effect of batch-effect correction methods (parametric and non-parametric ComBat models).: "Generate diagnosis plots comparing corrected versus uncorrected data to highlight the effect of batch-effect correction methods (parametric and non-parametric ComBat models)."
- [readme] the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data via either of those models: "the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] the performance of applied models are presented by a score calculated based on the maximum variability explained by the batch level, notify the consistency of model performance for all detected features (variables), facilitating quick comparison of the models for selecting one of those models, which is more appropriate to the data structure: "the performance of applied models are presented by a score calculated based on the maximum variability explained by the batch level, notify the consistency of model performance for all detected"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed.: "This function is suggested for less than 2000 features (variables) for better computational speed."
- [other] Load corrected and uncorrected metabolomics data matrices (e.g., log-transformed feature abundance tables with samples as rows and metabolic features as columns) into R.: "Load corrected and uncorrected metabolomics data matrices (e.g., log-transformed feature abundance tables with samples as rows and metabolic features as columns) into R."
