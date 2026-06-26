---
name: published-metabolic-profile-implementation
description: Use when you have Nightingale Health 1H-NMR metabolomics measurements
  for a new cohort and wish to compute one or more established metabolic risk scores
  (mortality, MetaboAge, cardiovascular event, type-2 diabetes, COVID-19 severity)
  without recalibration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - R
  - MiMIR
  techniques:
  - LC-MS
  - GC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# published-metabolic-profile-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill projects previously published metabolic risk scores—such as Deelen et al.'s all-cause mortality metabolic profile derived from 44,168 individuals—onto new 1H-NMR metabolomics data assayed by Nightingale Health. It enables rapid risk stratification of new cohorts using validated, externally derived metabolite-weight combinations without retraining.

## When to use

You have Nightingale Health 1H-NMR metabolomics measurements for a new cohort and wish to compute one or more established metabolic risk scores (mortality, MetaboAge, cardiovascular event, type-2 diabetes, COVID-19 severity) without recalibration. This is appropriate when the metabolite panel and assay platform match the reference study, and you want to leverage external validation rather than deriving novel scores.

## When NOT to use

- Your metabolomics data is from a different assay platform (e.g., LC-MS/MS, GC-MS) or vendor—coefficients are specific to Nightingale Health 1H-NMR measurement protocols and metabolite definitions.
- You aim to develop a novel metabolic score or recalibrate an existing score to your cohort; this skill is for applying fixed, externally validated models, not model fitting.
- Your feature matrix is already a computed metabolic score (not raw metabolite measurements)—you would be projecting a projection.

## Inputs

- Nightingale Health 1H-NMR metabolite measurements (CSV or TSV feature matrix with samples as rows, metabolites as columns)
- Sample metadata (identifiers and phenotypic covariates, optional)
- Published metabolic score specification (coefficient vector and model reference from Deelen et al. or other source studies)

## Outputs

- Predicted metabolic risk score vector (numeric, one score per sample, paired with sample identifiers)
- Validation report indicating which metabolites were detected and any missing features
- Optional: figures (e.g., score distributions, survival curves) and downloadable result tables

## How to apply

Load your Nightingale Health 1H-NMR feature matrix (metabolite columns must match the reference study's naming convention) and sample metadata into R. Retrieve the pre-computed metabolic score coefficients and reference model specification from MiMIR, which encodes the published linear combination of metabolite weights. Apply the linear model by matrix multiplication: multiply each sample's metabolite vector by the published coefficient vector to yield a single risk score per sample. Pair each score with its sample identifier and export as a numeric vector. MiMIR automates this projection workflow and validates that required metabolites are present in your dataset before computation; refer to the example datasets in the Quick Start to ensure your column naming matches expected conventions.

## Related tools

- **MiMIR** (Implements the projection framework and provides pre-configured metabolic score coefficients, automatic metabolite matching, and a graphical interface for ad-hoc analysis of Nightingale Health 1H-NMR data.) — https://github.com/DanieleBizzarri/MiMIR
- **R** (Host language for MiMIR and underlying matrix operations (linear algebra) used to compute the metabolic score projections.)

## Examples

```
library("MiMIR")
MiMIR::startApp()
# Then: (1) Upload metabolites CSV with Nightingale column names; (2) Select 'All-cause mortality score' from available scores; (3) Click 'Compute'; (4) Download results.
```

## Evaluation signals

- Metabolite presence check: MiMIR confirms that all required metabolites for the target score are present in your input dataset (see 'Check if the App could find all the necessary metabolites' in Quick Start).
- Score output is a single numeric vector with length equal to the number of input samples, with no missing values for samples that have complete metabolite profiles.
- Scores fall within the expected range relative to the reference study distribution (e.g., visualization by boxplot or histogram should resemble published risk score distributions or reference percentiles).
- Sample identifiers are correctly preserved and paired with their corresponding scores in the output table.
- Downstream associations (e.g., all-cause mortality, disease incidence) match the direction and approximate effect size reported in the source publication when applied to a validation cohort.

## Limitations

- Metabolite measurement units, normalization, and quality control must match Nightingale Health's standard assay pipeline; non-standard preprocessing or batch effects in your data may compromise score validity.
- The projected score is only as valid as the external cohort it was derived from; generalization to populations with very different demographic, genetic, or lifestyle profiles is not guaranteed.
- Missing metabolite measurements are not imputed by MiMIR; samples with incomplete metabolite profiles cannot be scored and are excluded from analysis.
- The linear projection assumes that the relationship between metabolites and risk is stable across populations; if your cohort has known interactions or non-linearities, a fixed linear model may be suboptimal.
- Multiple scores (mortality, MetaboAge, cardiovascular, diabetes, COVID-severity) are offered, but they were derived from different reference cohorts and may not be independent; simultaneous use and interpretation requires care.

## Evidence

- [other] MiMIR provides functionality to project the mortality score from Deelen et al.'s observational study of 44,168 individuals, which identified a metabolic profile of all-cause mortality risk, onto new 1H-NMR metabolomics data assayed by Nightingale Health.: "MiMIR provides functionality to project the mortality score from Deelen et al.'s observational study of 44,168 individuals, which identified a metabolic profile of all-cause mortality risk, onto new"
- [readme] provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health; allows to easily explore new metabolomics measurements assayed by Nightingale Health; project previously published metabolic scores; and calibrate the metabolic surrogate values to a desired dataset: "MiMIR (Metabolomics-based Models for Imputing Risk), is a a unique graphical user interface that provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale"
- [other] Project the mortality score onto the 1H-NMR feature space by applying the published linear combination of metabolite weights to each sample.: "Project the mortality score onto the 1H-NMR feature space by applying the published linear combination of metabolite weights to each sample"
- [readme] Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted). Check if the App could find all the necessary metabolites in your dataset.: "Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted). Check if the App could find all the necessary metabolites in your dataset."
- [other] Generate and export the mortality risk score for all samples as a numeric vector paired with sample identifiers.: "Generate and export the mortality risk score for all samples as a numeric vector paired with sample identifiers"
