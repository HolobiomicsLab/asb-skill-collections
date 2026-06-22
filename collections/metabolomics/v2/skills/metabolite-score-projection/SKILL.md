---
name: metabolite-score-projection
description: Use when you have Nightingale Health 1H-NMR metabolomics assay output (metabolite concentrations in a samples × features matrix) and you want to compute a published metabolic risk score or surrogate biomarker (mortality risk, metabolic age, cardiovascular event risk, type-2 diabetes risk, COVID-19.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MiMIR
  - R (base stats, dplyr, matrixStats)
derived_from:
- doi: 10.1093/bioinformatics/btac388
  title: MiMIR
- doi: 10.1038/s41467-019-11311-9
  title: ''
evidence_spans:
- '[![R-CMD-check](https://github.com/DanieleBizzarri/MiMIR/actions/workflows/R-CMD-check.yaml/badge.svg)]'
- github.com/DanieleBizzarri/MiMIR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-score-projection

## Summary

Project pre-trained metabolic risk scores (e.g., all-cause mortality, MetaboAge) onto new Nightingale Health 1H-NMR metabolomics datasets by applying published linear coefficient models to feature matrices. This skill enables rapid risk stratification and metabolic phenotyping of cohorts using validated, externally-derived metabolite weights.

## When to use

You have Nightingale Health 1H-NMR metabolomics assay output (metabolite concentrations in a samples × features matrix) and you want to compute a published metabolic risk score or surrogate biomarker (mortality risk, metabolic age, cardiovascular event risk, type-2 diabetes risk, COVID-19 severity, or clinical variable surrogates) for each sample without retraining. The published score coefficients, reference cohort specifications, and metabolite-to-coefficient mappings must be documented and available (e.g., in peer-reviewed literature or a pre-configured package like MiMIR).

## When NOT to use

- Your metabolomics data are NOT from Nightingale Health 1H-NMR assays (e.g., LC-MS, GC-MS, alternative NMR platforms may have different metabolite sets and units; projection will fail or produce invalid scores).
- You have incomplete metabolite coverage: if core metabolites required by the published model are missing and cannot be imputed, projection should not proceed without documented recalibration.
- You need to derive a new metabolic score or re-weight coefficients from your own cohort (this is model development/calibration, not projection; use regression or machine-learning training instead).

## Inputs

- Nightingale Health 1H-NMR metabolomics feature matrix (CSV or TSV format: samples × metabolites with column names matching model specification)
- Sample metadata (identifiers, optional covariates for validation)
- Published metabolic score coefficient vector and model reference specification (from literature or MiMIR package)

## Outputs

- Numeric vector of projected metabolic risk scores (one per sample)
- Sample identifiers paired with scores
- Optional: validation metrics (e.g., mean absolute error vs. chronological age for MetaboAge; correlation or C-statistic for mortality or event risk scores)
- Optional: data quality report (metabolites found/missing, feature completeness per sample)

## How to apply

Load your Nightingale Health 1H-NMR metabolite matrix (samples × metabolites) into R, ensuring column names and units match the published model specification. Retrieve or load the pre-trained coefficient vector and model metadata from MiMIR (or equivalent repository). Validate that all required metabolites are present in your feature set; MiMIR will flag missing metabolites automatically. Apply the linear projection by multiplying each sample's metabolite vector by the published coefficient weights, summing to produce a single risk score per sample. Export the resulting numeric vector of scores paired with sample identifiers. Optionally, calibrate or standardize scores to your cohort using reference quantiles if the published model included calibration guidance.

## Related tools

- **MiMIR** (R package providing graphical user interface and pre-configured coefficient vectors for projection of published metabolic scores (mortality, MetaboAge, cardiovascular, type-2 diabetes, COVID-19 severity, clinical surrogates) onto Nightingale Health 1H-NMR data; handles metabolite validation, missing-value flagging, and output export) — https://github.com/DanieleBizzarri/MiMIR
- **R (base stats, dplyr, matrixStats)** (Linear algebra and data manipulation for matrix operations, coefficient application, and output formatting)

## Examples

```
library(MiMIR); MiMIR::startApp()  # Then upload Nightingale 1H-NMR CSV with metabolites, select 'Project Mortality Score' or 'MetaboAge', download results with projected scores for each sample.
```

## Evaluation signals

- All required metabolites from the published model are present in the input feature matrix; MiMIR reports 100% metabolite match or documents which optional metabolites are missing.
- Projected scores are numeric, finite, and without NaN or Inf values; no sample has a score if any required metabolite is missing or non-numeric.
- Scores fall within expected ranges: for example, all-cause mortality scores should correlate positively with observed mortality in hold-out or external validation cohorts (e.g., hazard ratio > 1 per SD increase in score, C-statistic > 0.55); MetaboAge scores should correlate with chronological age (r > 0.5, MAE < 5–10 years for typical cohorts).
- Sample identifiers are preserved and match the input metadata in a 1:1 manner; no samples are dropped or duplicated.
- Outputs match the published model's units and direction: e.g., higher mortality scores indicate higher risk (not inverse).

## Limitations

- Projection is only valid if metabolite measurements are from Nightingale Health 1H-NMR assays; alternative platforms (LC-MS, GC-MS, other NMR vendors) may have different metabolite lists, units, or standardizations, leading to invalid scores.
- Missing or low-quality metabolite values in the input will propagate as missing or unreliable scores; no imputation is performed by default. Samples with >5–10% missing metabolites should be flagged or excluded.
- The projected score is a linear combination and assumes the published coefficient vector remains valid in your cohort; if your cohort differs substantially in age, sex, disease status, or ethnic background from the discovery cohort (e.g., Deelen et al.'s 44,168 individuals), score calibration or recalibration may be necessary.
- Projection does not account for batch effects, drift, or assay platform updates; if your Nightingale assay was performed at a different time or facility than the discovery study, standardization or batch-correction steps may be needed before projection.
- The skill provides point estimates (scores) only; it does not compute confidence intervals or adjustment for individual uncertainty in metabolite measurements.

## Evidence

- [other] MiMIR provides functionality to project the mortality score from Deelen et al.'s observational study of 44,168 individuals, which identified a metabolic profile of all-cause mortality risk, onto new 1H-NMR metabolomics data assayed by Nightingale Health.: "MiMIR provides functionality to project the mortality score from Deelen et al.'s observational study of 44,168 individuals, which identified a metabolic profile of all-cause mortality risk, onto new"
- [other] Project the mortality score onto the 1H-NMR feature space by applying the published linear combination of metabolite weights to each sample.: "Project the mortality score onto the 1H-NMR feature space by applying the published linear combination of metabolite weights to each sample."
- [other] MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository.: "MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository."
- [readme] provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health: "provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health"
- [readme] Check if the App could find all the necessary metabolites in your dataset.: "Check if the App could find all the necessary metabolites in your dataset."
- [other] MiMIR enables calibration of metabolic surrogate values to a desired dataset: "MiMIR enables calibration of metabolic surrogate values to a desired dataset"
