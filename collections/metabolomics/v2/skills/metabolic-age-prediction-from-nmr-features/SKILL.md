---
name: metabolic-age-prediction-from-nmr-features
description: Use when you have Nightingale Health 1H-NMR metabolomics data (feature
  matrix with named metabolite columns) and need to compute predicted metabolic age
  for each sample, typically to assess whether individuals' metabolic profiles align
  with or diverge from age-expected trajectories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MiMIR
  techniques:
  - LC-MS
  - NMR
  license_tier: restricted
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

# metabolic-age-prediction-from-nmr-features

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Reconstruct and apply the MetaboAge predictive model to estimate biological metabolic age from Nightingale Health 1H-NMR metabolomics features. This skill maps a curated set of NMR-derived metabolite concentrations through pre-trained linear model coefficients to produce a single predicted metabolic age value per sample, enabling assessment of metabolic aging independent of chronological age.

## When to use

Apply this skill when you have Nightingale Health 1H-NMR metabolomics data (feature matrix with named metabolite columns) and need to compute predicted metabolic age for each sample, typically to assess whether individuals' metabolic profiles align with or diverge from age-expected trajectories. This is useful when screening cohorts for metabolic aging biomarkers or validating metabolic health status.

## When NOT to use

- Nightingale Health metabolomics data is incomplete or missing >5% of the required model features; missing values must be imputed or samples excluded.
- Input is not 1H-NMR metabolomics or is from a different metabolomics platform (e.g., LC-MS); MetaboAge coefficients are platform-specific and not transferable.
- Sample age range is outside the BBMRI-NL training cohort (typically adults 18–100 years); extrapolation beyond training range yields unreliable predictions.

## Inputs

- Nightingale Health 1H-NMR metabolomics feature matrix (samples × named metabolite columns, CSV or TSV format)
- Sample metadata including chronological age (for validation)
- Pre-trained MetaboAge model coefficients and intercept (from MiMIR or published reference)

## Outputs

- Vector of predicted metabolic age values (one per sample)
- Mean absolute error (MAE) and Pearson correlation between predicted metabolic age and chronological age (validation metrics)
- Optional: predicted minus chronological age residuals (metabolic age acceleration)

## How to apply

Load the feature matrix (samples × metabolomics features) from your Nightingale Health output, ensuring all required metabolite columns match those specified in the published MetaboAge model from the BBMRI-NL 1H-NMR Metabolomics Repository. Obtain the pre-trained model coefficients from the MiMIR package documentation or reference publication (van den Akker et al., 2020). Apply the linear prediction function by multiplying the feature matrix by the coefficient vector and adding the intercept term to compute predicted metabolic age for each sample. Validate the predictions by computing mean absolute error (MAE) against chronological age in held-out test samples or external reference cohorts, and confirm predictions lie within physiologically plausible ranges (typically 18–100 years). Integrate the prediction function into your R workflow or use the MiMIR Shiny application for standardized implementation.

## Related tools

- **MiMIR** (Graphical interface to load metabolomics data, execute MetaboAge prediction, compute validation metrics, and export predicted metabolic age scores) — https://github.com/DanieleBizzarri/MiMIR
- **R** (Programming environment for implementing the linear prediction function, calculating MAE and correlation, and integrating MetaboAge into custom analysis workflows)

## Examples

```
library("MiMIR"); MiMIR::startApp()  # Upload Nightingale Health metabolomics CSV with named features, select MetaboAge prediction, view predicted scores and MAE against chronological age, download results.
```

## Evaluation signals

- Predicted metabolic age values are numeric, finite, and fall within physiologically plausible range (e.g., 18–100 years for adult cohorts).
- Mean absolute error (MAE) between predicted and chronological age is ≤10–12 years in held-out test cohorts or published reference datasets, consistent with reported model performance.
- Pearson correlation between predicted metabolic age and chronological age is ≥0.4–0.5 in the validation set, confirming the model captures age-related metabolic variation.
- Input metabolite column names exactly match those in the MetaboAge model specification; missing or incorrectly named features trigger a validation warning.
- Predictions are reproducible when applied to the same input data and model coefficients; deterministic linear computation ensures bit-level consistency.

## Limitations

- MetaboAge coefficients are trained on the BBMRI-NL cohort and may not generalize to populations with different ancestry, age structure, or disease prevalence; recalibration or validation in target cohorts is recommended.
- 1H-NMR batch effects and measurement noise can inflate prediction error; raw Nightingale Health data should be preprocessed (standardized to platform reference) before prediction.
- Predicted metabolic age is a composite score reflecting multiple metabolic pathways but does not attribute aging to specific mechanisms; biological interpretation requires downstream analysis of individual metabolite associations.
- Samples with >5% missing metabolite values cannot be reliably scored; imputation strategy (e.g., mean, k-NN) is not specified in the core methodology and must be decided a priori.

## Evidence

- [other] Identify and validate the set of metabolomics features used in the published MetaboAge model from the MiMIR repository documentation.: "Identify and validate the set of metabolomics features used in the published MetaboAge model from the MiMIR repository documentation."
- [other] Implement the MetaboAge prediction function in R that accepts a feature matrix (samples × metabolomics features) and applies the pre-trained model coefficients to compute predicted metabolic age for each sample.: "Implement the MetaboAge prediction function in R that accepts a feature matrix (samples × metabolomics features) and applies the pre-trained model coefficients to compute predicted metabolic age for"
- [other] Validate predictions against held-out test samples or reference cohorts by computing mean absolute error (MAE) and correlation with chronological age.: "Validate predictions against held-out test samples or reference cohorts by computing mean absolute error (MAE) and correlation with chronological age."
- [intro] MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository.: "MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository."
- [readme] provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health: "provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health"
- [readme] Metabolic Age Based on the BBMRI-NL 1H-NMR Metabolomics Repository as Biomarker of Age-related Disease: "Metabolic Age Based on the BBMRI-NL 1H-NMR Metabolomics Repository as Biomarker of Age-related Disease"
