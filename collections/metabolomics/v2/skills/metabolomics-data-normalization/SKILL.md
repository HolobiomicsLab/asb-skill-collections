---
name: metabolomics-data-normalization
description: Use when you have raw metabolomics data (samples × metabolic features matrix) collected across multiple analytical batches or instrument runs, and you observe evidence of technical heterogeneity—such as systematic shifts in metabolite intensities between batches, missing or zero values, or visual.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva
  - ber
  - pcaMethods, limma, impute, BiocParallel, Biobase, mixOmics, statTarget
  - MInfer
  - MetaboAnalyst
  - NormalizeMets
  - RStudio
  - NormQcmets
  - LogTransform
  - MissingValues
  - RlaPlots
  - PcaPlots
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
- doi: 10.1016/j.cmpb.2025.108672
  title: ''
- doi: 10.1007/s11306-018-1347-7
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity'
- ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]
- MInfer is an R package designed for analyzing metabolomics data
- MInfer is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cordbat_cq
    doi: 10.1021/acs.analchem.2c05748
    title: CordBat
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  - build: coll_minfer_cq
    doi: 10.1016/j.cmpb.2025.108672
    title: MInfer
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41598-021-84824-3
  all_source_dois:
  - 10.1038/s41598-021-84824-3
  - 10.1007/s12561-013-9081-1
  - 10.1016/j.cmpb.2025.108672
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-normalization

## Summary

A two-stage computational workflow that removes batch effects and technical heterogeneity from large-scale metabolomics datasets through missing-value imputation, statistical batch correction, and diagnostic visualization. Essential for ensuring that observed metabolite intensity variation reflects biological differences rather than analytical drift across sample batches.

## When to use

Apply this skill when you have raw metabolomics data (samples × metabolic features matrix) collected across multiple analytical batches or instrument runs, and you observe evidence of technical heterogeneity—such as systematic shifts in metabolite intensities between batches, missing or zero values, or visual batch clustering in unsupervised analyses. The skill is most valuable when batch effects would otherwise mask biological signal or inflate false-positive associations.

## When NOT to use

- Input data is already batch-corrected or has no evidence of batch-level systematic drift (check with PCA or ComBat diagnostics first)
- Sample size is very small (<10 samples) relative to number of batches, making parametric batch models unstable
- Metabolomics features exceed ~2000 (computational speed degrades for visualization-heavy functions like Visodbnorm and dbnormSCORE; use non-visualization functions dbnormBer, dbnormPcom, dbnormNPcom instead)

## Inputs

- Raw metabolomics data matrix (CSV): samples/experiments in rows, metabolic features in columns, batch indicator in first column, log2-normalized intensity values
- Batch assignment vector or column indicating analytical batch/run membership for each sample
- Optional: quality control replicates or technical replicates for hierarchical clustering validation

## Outputs

- Batch-corrected metabolomics matrix (CSV): same dimensions and format as input, with batch effects removed
- Diagnostic PDF reports: PCA plots, Scree plots, RLA (Relative Log Abundance) plots, correlation plots, and probability density function (PDF) profile plots for features in raw vs. corrected data
- Model performance CSV: adjusted R² values per feature and per model, and score matrix for maximum adjusted R² detected across models
- Optional: hierarchical clustering dendrogram and distance matrix for QC replicate concordance assessment

## How to apply

First, load the raw metabolomics data matrix in CSV format (independent experiments in rows, metabolic features in columns, with batch level in the first column) after log2-normalization to account for high-abundance features. Apply missing-value estimation functions (emvd to impute across the entire experiment, or emvf to impute feature-by-feature using the lowest detected value per feature) to handle zero and NA entries. Next, apply one of the implemented batch-correction models—ComBat parametric, ComBat non-parametric (both from the sva package), or the two-stage ber procedure—selecting the model via diagnostic comparison using dbnormSCORE (which reports adjusted R² per feature and model-level performance scores) or Visodbnorm (which generates PCA, RLA, and Scree plots for visual model comparison). Export the corrected metabolomics matrix in the same CSV format for downstream analysis.

## Related tools

- **dbnorm** (Primary package implementing all preprocessing, imputation, batch-correction models (ComBat, ber, ber-bagging), and diagnostic plotting functions for metabolomics normalization) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat parametric and non-parametric empirical Bayes batch-effect correction models called by dbnorm)
- **R** (Runtime environment and dependency manager for dbnorm package and all statistical models)
- **ber** (Archived R package (version 4.0) providing the two-stage batch-effect removal procedure adapted from microarray studies for use in metabolomics via dbnorm) — https://cran.r-project.org/src/contrib/Archive/
- **pcaMethods, limma, impute, BiocParallel, Biobase, mixOmics, statTarget** (Bioconductor dependencies for unsupervised clustering, regression, and imputation operations called by dbnorm functions)

## Examples

```
data <- read.csv('path/to/mydata.csv', sep = ',', header = T, row.names = 1); library(dbnorm); df <- data[-1]; f <- emvf(df); dbnormSCORE(cbind(data[1], f)); corrected <- dbnormPcom(data)
```

## Evaluation signals

- Adjusted R² for batch effect (coefficient of determination regressing each feature against batch membership) decreases from raw to corrected data across all or nearly all features, indicating batch variance has been removed
- PCA plot shows no visual separation of samples by batch after correction, whereas raw data exhibits clear batch-level clustering
- Quality-control replicates (identical samples run in different batches) cluster together in hierarchical dendrograms after correction, with inter-batch replicate distances comparable to within-batch technical replicates
- Probability density function (PDF) profile plots of raw features show shifted or multimodal distributions across batches; after correction, distributions are unimodal and overlaid across batches for each feature
- RLA (Relative Log Abundance) plots center near zero median across all samples after correction (indicating no systematic intensity shift) versus offsets from zero in raw data

## Limitations

- Package version 0.2.2 has no formal changelog; reproducibility and breaking changes between versions are not formally tracked
- The two-stage ber procedure and ber-bagging require the archived ber package (version 4.0) from CRAN Archive, which may become unavailable or incompatible with future R versions
- Visualization functions (Visodbnorm, dbnormSCORE) are recommended only for datasets with <2000 features due to computational and rendering overhead; large metabolomics studies may require non-visualization alternatives (dbnormBer, dbnormPcom, dbnormNPcom)
- Input data must be log2-normalized prior to import; unnormalized or differently-scaled data may yield misleading batch-correction results
- Model selection relies on user interpretation of diagnostic plots and adjusted R² scores; no automated recommendation algorithm is provided, requiring domain expertise in batch-effect structure

## Evidence

- [readme] dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values, conventional functions for batch effect correction based on statistical models: "dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values, conventional functions for batch effect correction based on statistical models"
- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked.: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked."
- [readme] The input data must be in .csv format with the independent experiments in the rows and the features (variables) in the columns, with the batch levels considered in the first column.: "The input data must be in .csv format with the independent experiments in the rows and the features (variables) in the columns, with the batch levels considered in the first column."
- [readme] emvd allows you to estimate missing values (Zero or/and NA values) by the lowest detected value in the entire experiment.: "emvd allows you to estimate missing values (Zero or/and NA values) by the lowest detected value in the entire experiment."
- [readme] emvf allows you to estimate missing values (Zero or/and NA values) for each feature (variable) by the lowest value detected for the corresponding feature: "emvf allows you to estimate missing values (Zero or/and NA values) for each feature (variable) by the lowest value detected for the corresponding feature"
- [readme] This function gives a quick notification about the performance of the statistical models, two-stage procedure and/or empirical Bayes methods in two setting of parametric and non-parametric, implemented in the dbnorm package, in accommodating technical variability.: "This function gives a quick notification about the performance of the statistical models, two-stage procedure and/or empirical Bayes methods in two setting of parametric and non-parametric,"
- [readme] Adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data: "Adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed.: "This function is suggested for less than 2000 features (variables) for better computational speed."
- [readme] ComBat(parametric and non-parametric)-model from sva package that was already in use for metabolomics data normalization, and ber function, priorly developed for microarray gene expression data: "ComBat(parametric and non-parametric)-model from sva package that was already in use for metabolomics data normalization, and ber function, priorly developed for microarray gene expression data"
