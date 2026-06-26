---
name: linear-score-calculation-from-coefficients
description: Use when when you have 1H-NMR metabolite measurements from Nightingale
  Health assayed on a new cohort and wish to compute risk scores (e.g., all-cause
  mortality, cardiovascular event, type 2 diabetes) using published metabolic biomarker
  weights from a reference study.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0625
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

# Linear Score Calculation from Coefficients

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply published regression coefficients to a feature matrix of metabolomic measurements to compute risk scores for individual samples. This skill enables projection of previously validated metabolic risk models onto new 1H-NMR data assayed by Nightingale Health.

## When to use

When you have 1H-NMR metabolite measurements from Nightingale Health assayed on a new cohort and wish to compute risk scores (e.g., all-cause mortality, cardiovascular event, type 2 diabetes) using published metabolic biomarker weights from a reference study. Typical trigger: feature matrix with metabolite columns matching reference model specification and sample identifiers in rows.

## When NOT to use

- Your metabolite measurements are from a different analytical platform (e.g., LC-MS, GC-MS, targeted assays) — coefficient mappings are specific to Nightingale 1H-NMR assay
- Your dataset lacks one or more of the required metabolites specified in the reference model — missing features violate the linear model assumption
- You intend to re-train or calibrate coefficients rather than project a fixed model — use calibration workflows instead

## Inputs

- 1H-NMR metabolite feature matrix (CSV or TSV format; samples × metabolites)
- Sample metadata (identifiers, phenotype labels)
- Published regression coefficients and reference model specification

## Outputs

- Risk score vector (numeric, one value per sample)
- Score paired with sample identifiers
- Optional: visualization and diagnostic figures (heatmaps, ROC curves)

## How to apply

Load your Nightingale Health 1H-NMR feature matrix (samples × metabolites) and sample metadata into R. Retrieve the published regression coefficients and reference model specification (e.g., from Deelen et al. for all-cause mortality or other MiMIR-supported models). Verify that all required metabolites are present in your dataset and consistently named with the reference model. Apply the linear combination by multiplying each sample's metabolite vector by the coefficient vector and summing across metabolites to yield a single risk score per sample. Export the resulting numeric vector paired with sample identifiers. MiMIR automates this workflow within a Shiny interface, providing validation checks and visualization outputs.

## Related tools

- **MiMIR** (Shiny application providing graphical interface for 1H-NMR metabolomics analysis, coefficient projection, and score computation) — https://github.com/DanieleBizzarri/MiMIR
- **R** (Statistical computing environment for loading data, applying linear combinations, and exporting results)

## Examples

```
library("MiMIR"); MiMIR::startApp()  # Then upload 1H-NMR CSV, select 'Mortality Score' model, and download projected scores
```

## Evaluation signals

- All required metabolites from the reference model are successfully identified and mapped in the input dataset (automated check in MiMIR)
- Output score vector has length equal to number of samples and contains no missing or infinite values
- Score distribution and range align with published reference study expectations (e.g., mortality scores should show expected separation by outcome status)
- Sample identifiers in output match input metadata exactly with no loss or reordering
- ROC curve and survival curve visualizations (if applicable) show expected discrimination patterns for the risk model

## Limitations

- Coefficients are specific to Nightingale Health 1H-NMR assay platform; cannot be applied directly to other metabolomics platforms without re-calibration
- Missing or below-detection metabolites will fail validation; imputation is not automatic and should be handled prior to projection
- Projected scores assume the same technical and biological preprocessing (e.g., normalization, batch correction) as the reference cohort; unexplained batch effects may bias scores
- Linear model assumes additive effects; non-linear metabolite interactions or platform-specific signal artifacts are not modeled

## Evidence

- [other] Workflow step 3: "Project the mortality score onto the 1H-NMR feature space by applying the published linear combination of metabolite weights to each sample"
- [other] Article title and research question: "MiMIR provides functionality to project the mortality score from Deelen et al.'s observational study of 44,168 individuals, which identified a metabolic profile of all-cause mortality risk, onto new"
- [readme] README capability summary: "provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health"
- [readme] README key feature: "project previously published metabolic scores"
- [other] Workflow step 1: "Load the Nightingale Health 1H-NMR metabolite measurements (feature matrix) and sample metadata into R"
