---
name: parametric-nonparametric-model-selection
description: Use when you have preprocessed, log₂-scaled metabolomics data in CSV
  format (samples × features) with batch assignment labels and need to decide which
  batch effect correction model to apply.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - sva
  - R
  - ber
  license_tier: restricted
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]
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

# parametric-nonparametric-model-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select between parametric ComBat, non-parametric ComBat, two-stage (ber), and bagging-based batch correction models by comparing their performance on metabolomics data using adjusted R² scores and diagnostic plots. This skill enables practitioners to choose the statistical model that best fits their dataset's batch structure before applying correction.

## When to use

You have preprocessed, log₂-scaled metabolomics data in CSV format (samples × features) with batch assignment labels and need to decide which batch effect correction model to apply. Use this skill when you want to compare how well parametric ComBat, non-parametric ComBat, ber, and ber-bagging models explain batch-induced variance before committing to one for downstream analysis.

## When NOT to use

- Input data is not log₂-scaled or not normalized; preprocessing must precede model selection.
- Metabolomics dataset contains >2000 features; dbnormSCORE and Visodbnorm are recommended for <2000 features for computational speed.
- Batch assignment is unknown or ambiguous; model selection requires clear batch labels in the input data.

## Inputs

- preprocessed metabolomics matrix (CSV format: rows=samples, columns=features)
- batch assignment vector (first column of input CSV)
- log₂-scaled abundance data

## Outputs

- adjusted R² coefficient matrix for each model and feature
- performance score table ranking models by maximum adjusted R²
- diagnostic PDF (PCA, Scree, RLA, Correlation plots)
- batch-corrected CSV matrices for each tested model

## How to apply

Load your normalized, log₂-scaled metabolomics matrix (rows=samples, columns=features, batch labels in first column) into dbnorm. Run dbnormSCORE() to compute adjusted R² for each feature under each of the four models (parametric ComBat, non-parametric ComBat, ber, ber-bagging) in both raw and batch-corrected data. Inspect the resulting Score table to identify which model achieves the highest and most consistent adjusted R² across features, indicating best fit to your batch structure. For datasets with <2000 features, also run Visodbnorm() to visually compare PCA, Scree, and RLA plots across models. Select the model that maximizes variance explained by batch removal while minimizing feature-to-feature inconsistency in performance.

## Related tools

- **dbnorm** (primary package providing dbnormSCORE and Visodbnorm functions for model comparison and batch correction) — https://github.com/NBDZ/dbnorm
- **sva** (source package providing parametric and non-parametric ComBat models integrated into dbnorm)
- **R** (execution environment for dbnorm functions and statistical model evaluation)
- **ber** (archived R package (v4.0) providing two-stage batch effect removal procedure implemented in dbnorm) — http://cran.us.r-project.org

## Examples

```
dbnormSCORE(data); # Generates adjusted R² scores and performance comparison table for all four models
Visodbnorm(data);  # Generates PCA, Scree, and RLA diagnostic plots for model visual comparison (features < 2000)
```

## Evaluation signals

- Adjusted R² should decrease substantially in batch-corrected data compared to raw data, indicating batch variance removal.
- One model should show consistently high adjusted R² across >80% of features, indicating stable model fit.
- PCA plots should show reduced batch clustering and improved inter-batch sample mixing after correction with selected model.
- Score table should identify a clear winner (model with highest maximum adjusted R²) with <20% performance variance across features.
- RLA (Relative Log Abundance) plots should show centered distributions around zero median log-fold-change post-correction.

## Limitations

- Model selection is empirical and data-dependent; no single model is universally optimal across all batch structures.
- Computational speed degrades substantially for >2000 features; dbnormSCORE and Visodbnorm are not recommended at that scale.
- Selection depends on correct batch label specification; mislabeled or misaligned batch assignments will produce misleading scores.
- Adjusted R² alone does not account for biological signal preservation; visual inspection of diagnostic plots is essential.
- ber and ber-bagging models were originally developed for microarray data; performance on metabolomics may differ from parametric/non-parametric ComBat.

## Evidence

- [readme] dbnormSCORE function provides adjusted coefficient of determination for each variable estimated in a regression model for its dependency to the batch level: "This function gives a quick notification about the performance of the statistical models, two-stage procedure [DOI:10.1007/s12561-013-9081-1] and/or empirical Bayes methods in two setting of"
- [readme] Score table facilitates quick comparison of models for selecting the most appropriate: "Immediately, the performance of applied models are presented by a score calculated based on the maximum variability explained by the batch level, notify the consistency of model performance for all"
- [readme] Visodbnorm visualizes three batch correction models via PCA, Scree, and RLA plots for datasets with <2000 features: "This function performs batch effect adjustment via three statistical models implemented in the *dbnorm*, namely two-stage procedure as described by Giordan (2013)[DOI:10.1007/s12561-013-9081-1]"
- [readme] Input data must be normalized and log₂-scaled to account for high-abundance features: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked."
- [readme] dbnorm implements four distinct batch correction models for model selection comparison: "*dbnorm* includes several statistical models such as, ComBat(parametric and non-parametric)-model [PMID:16632515]  from sva package [PMID:22257669] ,that was already in use for metabolomics data"
