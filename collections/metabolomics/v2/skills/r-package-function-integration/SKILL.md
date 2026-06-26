---
name: r-package-function-integration
description: Use when you have a published predictive model with known coefficients
  and feature requirements (e.g., MetaboAge from a peer-reviewed study), a target
  R package with an established data pipeline (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MiMIR
  - R (base and stats)
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
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

# R Package Function Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate a predictive model (such as MetaboAge) as a validated R function into an existing package, ensuring compatibility with the package's input/output formats and maintaining reproducibility through pre-trained model coefficients. This skill is essential when extending a package like MiMIR to support new metabolic biomarkers or surrogate predictions.

## When to use

You have a published predictive model with known coefficients and feature requirements (e.g., MetaboAge from a peer-reviewed study), a target R package with an established data pipeline (e.g., MiMIR for Nightingale Health 1H-NMR metabolomics), and you need to make that model available to end users without requiring external dependencies or manual model re-training. Use this skill when the model is already validated and you need to embed it as a reusable function.

## When NOT to use

- The model coefficients are proprietary or cannot be published; use the skill only when coefficients are available in peer-reviewed supplementary material or open repositories.
- Input is already a pre-computed prediction or score; this skill is for embedding the model function itself, not post-processing existing predictions.
- The package already includes the model or an equivalent validated implementation; integrating a duplicate function risks maintenance burden and inconsistency.

## Inputs

- Feature matrix: samples × metabolomics features (numeric matrix or data.frame with column names matching Nightingale Health metabolite naming convention)
- Pre-trained model coefficients (numeric vector or list, with names mapping to feature columns)
- Optional: reference dataset with ground truth labels (e.g., chronological age for MetaboAge validation)
- Optional: package configuration file specifying required features and their roles

## Outputs

- Prediction vector or data.frame with one row per sample and columns for predicted score (e.g., predicted metabolic age), confidence/error estimates, and feature completeness flags
- Validation report (MAE, correlation coefficient, sample counts) comparing predictions to reference cohort
- R function object exported from the package namespace, callable as `function_name(feature_matrix)`

## How to apply

First, identify and validate the complete set of metabolomics features and model coefficients from the published source or package documentation (e.g., MetaboAge coefficients from the BBMRI-NL repository). Second, implement the prediction function in R to accept a feature matrix (samples × metabolomics features) and apply the pre-trained coefficients to compute predictions (e.g., predicted metabolic age). Third, ensure the function validates that all required metabolite columns are present in the input and match the naming convention of the package's canonical example dataset. Fourth, integrate the function into the package structure (e.g., as an exported function in the MiMIR namespace) and test compatibility against the package's standard output formats (CSV, TSV). Finally, validate predictions against held-out test samples or published reference cohorts by computing error metrics (mean absolute error, correlation with ground truth) and confirm the results align with the original publication.

## Related tools

- **MiMIR** (Host R package providing Shiny GUI and data pipeline for 1H-NMR metabolomics; integration target for metabolic score functions) — https://github.com/DanieleBizzarri/MiMIR
- **R (base and stats)** (Language and runtime for implementing prediction function and validation metrics (MAE, correlation))

## Examples

```
library(MiMIR); metabo_data <- read.csv('metabolites.csv', row.names=1); predictions <- predict_metabolic_age(metabo_data); head(predictions)
```

## Evaluation signals

- All required metabolite columns are present in the input and match the canonical Nightingale Health naming scheme; the function returns NA or raises an informative error if any are missing.
- Mean absolute error (MAE) of predictions on a held-out test set matches or falls within the range reported in the original publication (e.g., within ±5% of published MAE for MetaboAge).
- Correlation between predicted scores and ground truth (e.g., chronological age for MetaboAge) on a reference cohort is consistent with the original study (r > 0.80 for MetaboAge).
- Predictions output in the same format as other MiMIR scores: one row per sample, with named columns, compatible with CSV/TSV export and Shiny table rendering.
- Function signature and behavior are documented in the package manual and example invocations run without errors on the downloadable synthetic example dataset.

## Limitations

- The model is fixed to the published coefficients; recalibration to a new cohort requires a separate skill (MiMIR supports this via a 'calibrate' function, but integration of a new calibrated model is outside the scope of this skill).
- Predictions depend entirely on the availability and quality of the required metabolite features; missing or miscalibrated features will degrade predictions but are not detected unless explicit validation is added.
- The skill assumes the model is linear or additive (feature × coefficient); non-linear models or those requiring interaction terms may require additional implementation and validation steps not described in the MiMIR README.
- Nightingale Health metabolomics platform updates or changes in assay methodology may invalidate pre-trained coefficients; users must verify compatibility with their specific assay batch.

## Evidence

- [other] Identify and validate the set of metabolomics features used in the published MetaboAge model from the MiMIR repository documentation.: "Identify and validate the set of metabolomics features used in the published MetaboAge model from the MiMIR repository documentation."
- [other] Implement the MetaboAge prediction function in R that accepts a feature matrix (samples × metabolomics features) and applies the pre-trained model coefficients to compute predicted metabolic age for each sample.: "Implement the MetaboAge prediction function in R that accepts a feature matrix (samples × metabolomics features) and applies the pre-trained model coefficients to compute predicted metabolic age for"
- [other] Validate predictions against held-out test samples or reference cohorts by computing mean absolute error (MAE) and correlation with chronological age.: "Validate predictions against held-out test samples or reference cohorts by computing mean absolute error (MAE) and correlation with chronological age."
- [other] Integrate the function into the MiMIR package structure and verify compatibility with Nightingale Health output formats.: "Integrate the function into the MiMIR package structure and verify compatibility with Nightingale Health output formats."
- [intro] MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository.: "MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository."
- [readme] provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health: "provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health"
- [readme] Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted).: "Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted)."
