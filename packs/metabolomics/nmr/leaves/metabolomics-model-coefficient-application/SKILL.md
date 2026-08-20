---
name: metabolomics-model-coefficient-application
description: Use when you have a matrix of Nightingale Health 1H-NMR metabolomics measurements (samples × features) and need to generate predicted metabolic scores published in peer-reviewed studies (MetaboAge, mortality score, cardiovascular event risk, Type-2 diabetes score, COVID-severity score, or surrogate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3373
  tools:
  - R
  - MiMIR
  - R (base stats, caret, matrixStats)
  techniques:
  - NMR
derived_from:
- doi: 10.1093/bioinformatics/btac388
  title: MiMIR
- doi: 10.1038/s41467-019-11311-9
  title: ''
evidence_spans:
- '[![R-CMD-check](https://github.com/DanieleBizzarri/MiMIR/actions/workflows/R-CMD-check.yaml/badge.svg)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimir_cq
    doi: 10.1093/bioinformatics/btac388
    title: MiMIR
  dedup_kept_from: coll_mimir_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac388
  all_source_dois:
  - 10.1093/bioinformatics/btac388
  - 10.1038/s41467-019-11311-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-model-coefficient-application

## Summary

Apply pre-trained linear model coefficients to Nightingale Health 1H-NMR metabolomics feature matrices to compute predicted metabolic biomarker scores (e.g., MetaboAge, mortality risk). This skill bridges published metabolic prediction models with new cohort data by mapping individual metabolite concentrations to scalar risk or age estimates.

## When to use

You have a matrix of Nightingale Health 1H-NMR metabolomics measurements (samples × features) and need to generate predicted metabolic scores published in peer-reviewed studies (MetaboAge, mortality score, cardiovascular event risk, Type-2 diabetes score, COVID-severity score, or surrogate clinical variables). Apply this skill when the model coefficients and feature set are publicly documented and your input metabolites match or can be matched to the model's training feature list.

## When NOT to use

- Input metabolomics data are not from Nightingale Health 1H-NMR assay; coefficients are platform-specific and cannot be applied to mass spectrometry or other NMR platforms.
- The feature set in your dataset does not overlap sufficiently with the model's training features (missing >5–10% of required metabolites); imputation or re-training is required.
- Model coefficients are not published or are proprietary; without explicit coefficients and feature documentation, application is not reproducible.

## Inputs

- Nightingale Health 1H-NMR metabolomics feature matrix (samples × metabolites, CSV or TSV format)
- Pre-trained model coefficients (vector of feature-to-score weights from published study)
- Feature metadata documenting required metabolite names and their column indices in input matrix

## Outputs

- Predicted metabolic score vector (one score per sample)
- Validation statistics: mean absolute error (MAE), Pearson correlation coefficient, residual distribution

## How to apply

First, load the metabolomics feature matrix in the format output by Nightingale Health (CSV or TSV with standard column names). Next, identify and validate the set of metabolomics features required by the published model from MiMIR repository documentation or the original manuscript. Cross-check that your input dataset contains all required metabolites; missing features or column name mismatches will cause model application to fail. Then, apply the pre-trained model coefficients via linear combination: for each sample, multiply each metabolite concentration by its corresponding coefficient and sum across features to obtain the predicted score. Finally, validate predictions by computing mean absolute error (MAE) and Pearson correlation with chronological age (for age-based scores) or mortality/outcome events (for risk scores) on held-out test samples or reference cohorts. Integration into MiMIR package structure ensures reproducibility and compatibility with downstream Shiny-based visualization.

## Related tools

- **MiMIR** (R/Shiny framework that encodes pre-trained metabolic model coefficients and provides graphical interface for coefficient application, validation, calibration, and visualization of predicted scores on Nightingale Health 1H-NMR data) — https://github.com/DanieleBizzarri/MiMIR
- **R (base stats, caret, matrixStats)** (Matrix algebra, linear regression, mean absolute error, correlation computation, and coefficient-based prediction implementation)

## Examples

```
library(MiMIR); MiMIR::startApp()  # or programmatically: predicted_age <- apply_metabolic_coefficients(metabolite_matrix, coefficients_vector, feature_names); mae <- mean(abs(predicted_age - chronological_age))
```

## Evaluation signals

- Output score vector has length equal to the number of samples in the input matrix; no NaN or Inf values except where input metabolites are missing.
- Predicted scores correlate strongly (r > 0.70 for age-based scores, AUROC > 0.70 for risk scores) with chronological age or outcome labels in held-out test cohort, matching or exceeding correlation reported in original model publication.
- Mean absolute error (MAE) between predicted and actual age (or risk) on reference cohort falls within reported bounds from published model validation study.
- Output metabolic scores are continuous and fall within the plausible biological range documented in the original publication (e.g., MetaboAge typically ranges 30–90 years for adult cohorts).
- Feature column names in input matrix exactly match the model's documented feature set; validation step confirms all required metabolites are present and non-missing.

## Limitations

- Model coefficients are fixed and derived from a specific training cohort (e.g., BBMRI-NL for MetaboAge); predictions may be biased if applied to populations with substantially different metabolic profiles or ethnic/geographic ancestry.
- Missing or below-detection-limit metabolite values in the input matrix will cause sample-wise score computation to fail or produce biased estimates; imputation strategy (mean, median, or model-based) must be pre-specified and documented.
- Nightingale Health assay platform has evolved over time (e.g., extended metabolite panels); older coefficient sets may not be compatible with newer platform versions if new metabolites are included or existing ones are renamed.
- Linear coefficient application assumes metabolite concentrations are on the original measurement scale (typically mmol/L) and have not been log-transformed or otherwise normalized; data transformation not documented in the input will yield invalid predictions.

## Evidence

- [other] Implement the MetaboAge prediction function in R that accepts a feature matrix (samples × metabolomics features) and applies the pre-trained model coefficients to compute predicted metabolic age for each sample.: "Implement the MetaboAge prediction function in R that accepts a feature matrix (samples × metabolomics features) and applies the pre-trained model coefficients to compute predicted metabolic age for"
- [other] Validate predictions against held-out test samples or reference cohorts by computing mean absolute error (MAE) and correlation with chronological age.: "Validate predictions against held-out test samples or reference cohorts by computing mean absolute error (MAE) and correlation with chronological age."
- [readme] MiMIR provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health: "provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health"
- [intro] MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository.: "MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository."
- [readme] Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted).: "Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted)."
