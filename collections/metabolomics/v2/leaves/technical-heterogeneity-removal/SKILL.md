---
name: technical-heterogeneity-removal
description: Use when your metabolomics matrix (log2-scaled, samples × features in
  .csv format) exhibits spatial or distributional separation by batch/analytical run,
  visible in PCA or RLA plots.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - dbnorm
  - R
  - sva
  - ber
  license_tier: restricted
  provenance_tier: literature
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

# Technical Heterogeneity Removal from Metabolomics Datasets

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill removes batch effects and drift across analytical runs in metabolomics datasets using statistical correction models (two-stage procedure, parametric/non-parametric ComBat, or bagging-based regression). It is essential when metabolomics data span multiple batches or time periods and technical variation threatens the validity of biological inference.

## When to use

Apply this skill when your metabolomics matrix (log2-scaled, samples × features in .csv format) exhibits spatial or distributional separation by batch/analytical run, visible in PCA or RLA plots. Use it after missing-value imputation and before differential abundance or association testing, especially if batches contain identical quality-control replicates that should cluster together regardless of analytical run.

## When NOT to use

- Data are not log2-scaled or do not account for high-abundance feature dominance; preprocessing must precede correction.
- Single batch or no evidence of batch effect (PCA/RLA shows no batch clustering); correction is unnecessary and risks overfitting.
- Feature count > 2000 and computational speed is critical; Visodbnorm and dbnormSCORE functions will be slow and are not recommended by the authors.

## Inputs

- Metabolomics data matrix (samples × features, .csv format)
- Log2-scaled intensity or abundance values
- Batch/analytical-run identifiers (first column)
- Missing values imputed (zero or NA replaced with feature or global minimum)

## Outputs

- Batch-corrected metabolomics matrix (.csv file)
- Adjusted R² scores for each feature and model comparison table (.csv)
- Diagnostic plots (PCA, scree, RLA, correlation, probability density function profiles) in PDF
- Hierarchical clustering dendrograms of original vs. corrected data (optional)

## How to apply

Load log2-scaled, batch-annotated metabolomics data (first column = batch identifier, remaining columns = features). Choose a batch correction model: the two-stage procedure (ber function) for microarray-derived drift patterns, parametric ComBat for normally distributed features, non-parametric ComBat for skewed distributions, or ber-bagging for robust partial bootstrap correction (n=150 samples). Run the corresponding dbnorm function (dbnormBer, dbnormPcom, dbnormNPcom, or dbnormBagging). Evaluate model fit using dbnormSCORE, which calculates adjusted R² for each feature's dependence on batch before and after correction; select the model maximizing consistency across features. Generate diagnostic plots (PCA, RLA, correlation, distribution profiles) to confirm batch signal removal without introducing artificial clustering.

## Related tools

- **dbnorm** (Primary R package providing 11 functions for missing-value imputation, batch correction (ber, ComBat variants, bagging), and diagnostic visualization for metabolomics drift normalization) — https://github.com/NBDZ/dbnorm
- **sva** (Source of parametric and non-parametric ComBat empirical Bayes methods, wrapped and extended in dbnorm for metabolomics use)
- **ber** (Two-stage batch-effect regression model from microarray literature, ported to metabolomics via dbnorm)

## Examples

```
data <- read.csv('metabolomics_raw_log2.csv', sep=',', header=TRUE, row.names=1)
library(dbnorm)
dbnormSCORE(data)  # Evaluate model fit
dbnormBer(data)    # Apply two-stage batch correction and generate diagnostics
```

## Evaluation signals

- Adjusted R² for each feature decreases after correction, indicating reduced batch dependence; check dbnormSCORE output table for consistency across features.
- PCA and RLA plots show elimination of batch-driven clustering or drift; samples from the same biological group cluster together regardless of batch assignment.
- Hierarchical clustering of quality-control replicates analyzed in different batches shows reduced dissimilarity (Pearson distance, average linkage) post-correction compared to raw data.
- Probability density function plots (ProfPlot* functions) show alignment of feature distributions across batches, with no artificial multimodality or distortion.
- No systematic loss of biological signal: effect sizes for known biological associations (if available) remain unchanged or improve; feature variance explained by non-batch covariates is preserved.

## Limitations

- Requires batch-level annotation in first column of input matrix; missing or mislabeled batch assignments will cause incorrect correction.
- Assumes linear batch effects; non-linear drift or instrument malfunction in a single run may not be fully captured.
- Parametric ComBat assumes approximate normality; highly skewed features may require log transformation or non-parametric variant.
- Bagging approach (ber-bagging) uses partial bootstrap (n=150); convergence and stability for very small sample counts (n < 30 per batch) not reported.
- No automatic model selection; users must interpret diagnostic plots and adjusted R² scores to choose between ber, bagging, and ComBat variants—suboptimal choice risks over- or under-correction.
- Performance degrades for > 2000 features; computational speed not reported for large feature sets.

## Evidence

- [readme] dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values, conventional functions for batch effect correction based on statistical models: "dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values, conventional functions for batch effect correction based on statistical models"
- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked.: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked."
- [intro] It allows users to efficiently correct drift across batch and to adjust large metabolomics datasets for technical variation which helps improving the estimation of the biological mechanisms underlying disease condition: "It allows users to efficiently correct drift across batch and to adjust large metabolomics datasets for technical variation which helps improving the estimation"
- [readme] Adjusted R-squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data via either of those models.: "Adjusted R-squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed.: "This function is suggested for less than 2000 features (variables) for better computational speed."
