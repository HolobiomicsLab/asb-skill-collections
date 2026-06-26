---
name: nightingale-1h-nmr-data-integration
description: Use when you have newly assayed 1H-NMR metabolomics data from Nightingale
  Health (CSV or TSV format) and need to apply one or more published metabolic risk
  scores (Deelen et al. all-cause mortality, van den Akker MetaboAge, Würtz cardiovascular
  event risk, etc.).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MiMIR
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

# nightingale-1h-nmr-data-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate and standardize Nightingale Health 1H-NMR metabolomics measurements into a feature matrix compatible with MiMIR's pre-trained metabolic scoring models. This skill enables projection of published metabolic biomarkers (mortality risk, MetaboAge, cardiovascular risk, etc.) onto new cohorts by aligning raw metabolite data to expected column nomenclature and validating feature completeness.

## When to use

You have newly assayed 1H-NMR metabolomics data from Nightingale Health (CSV or TSV format) and need to apply one or more published metabolic risk scores (Deelen et al. all-cause mortality, van den Akker MetaboAge, Würtz cardiovascular event risk, etc.). Use this skill before any downstream projection or calibration to ensure your feature matrix matches the exact metabolite names and counts required by the pre-trained models.

## When NOT to use

- Your metabolomics data is already in a pre-processed feature matrix format and metabolite names have already been validated against MiMIR's expected columns.
- Your 1H-NMR data is from a vendor other than Nightingale Health (e.g., Bruker, Chenomx) without documented Nightingale-compatible harmonization.
- You only need to perform exploratory analysis or statistical association testing; projection of pre-trained scores is not your goal.

## Inputs

- Nightingale Health 1H-NMR metabolomics table (CSV or TSV format with metabolite concentrations as columns)
- Sample metadata table (sample IDs, chronological age, cohort labels, etc.)
- MiMIR package documentation (MANUAL.pdf) or example dataset for feature name reference

## Outputs

- Validated feature matrix (samples × metabolites, numeric, with row names = sample IDs)
- Data quality report (count of detected vs. expected metabolites, missing-value summary)
- Ready-to-upload data object compatible with MiMIR Shiny app or downstream R projection functions

## How to apply

Load your Nightingale Health-assayed metabolite table (CSV or TSV) into R alongside sample metadata. Validate that your dataset contains all required metabolite columns by cross-referencing against the MiMIR package's documented feature list (available in the MANUAL.pdf or via package inspection). Rename or reorder columns if necessary to match the canonical Nightingale nomenclature. Check for missing values and apply imputation or exclusion per your analysis protocol. Once feature alignment is confirmed, structure the data as a samples × metabolites numeric matrix with sample identifiers paired as row names. The MiMIR application will automatically detect compatible metabolites during upload; if the app reports missing metabolites, inspect the README example datasets to reconcile naming conventions, then re-upload.

## Related tools

- **MiMIR** (Shiny graphical interface that ingests validated Nightingale Health metabolomics matrices and projects pre-trained metabolic scores (mortality, MetaboAge, cardiovascular risk, etc.); handles feature matching, missing-metabolite detection, and model application) — https://github.com/DanieleBizzarri/MiMIR
- **R** (Data manipulation, feature validation, and matrix construction; use dplyr, data.table, or base functions to load, rename, and align Nightingale metabolite columns)

## Examples

```
library('MiMIR'); metabolites <- read.csv('nightingale_data.csv', row.names=1); MiMIR::startApp()  # upload metabolites.csv via GUI; verify feature detection passes
```

## Evaluation signals

- All expected metabolite columns are present in your feature matrix and match the canonical Nightingale Health names documented in the MiMIR MANUAL or example dataset.
- Feature matrix has no row or column names containing special characters or spaces that would cause parsing errors in MiMIR upload.
- MiMIR application successfully detects 100% of metabolites required for at least one pre-trained score (e.g., all metabolites in Deelen et al. mortality model are found); if metabolites are missing, the app reports their names explicitly.
- Row names (sample IDs) are unique and non-null; sample count and metabolite count match your source data.
- Numeric matrix contains no unexpected missing values (NaN, Inf, or negative concentrations where biologically implausible); missing-value counts are documented and justified.

## Limitations

- MiMIR requires exact nomenclature alignment; metabolite names that differ even slightly from Nightingale Health's official column names will not be recognized and will cause score projection to fail or exclude those features.
- Only Nightingale Health 1H-NMR measurements are officially supported; data from other vendors or using different assay protocols may not align with pre-trained model coefficients, leading to invalid score estimates.
- The skill does not automatically impute missing metabolite values; cohorts with incomplete metabolite panels must be handled via exclusion or external imputation before upload.
- Pre-trained scores are calibrated on specific cohorts (BBMRI-NL for MetaboAge, UK Biobank for COVID-severity); projection onto very different populations may reduce predictive validity.

## Evidence

- [readme] MiMIR (Metabolomics-based Models for Imputing Risk), is a a unique graphical user interface that provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale Health.: "MiMIR (Metabolomics-based Models for Imputing Risk), is a a unique graphical user interface that provides an intuitive framework for ad-hoc statistical analysis of 1H-NMR metabolomics by Nightingale"
- [readme] It allows to easily explore new metabolomics measurements assayed by Nightingale Health; project previously published metabolic scores; and calibrate the metabolic surrogate values to a desired dataset.: "allows to easily explore new metabolomics measurements assayed by Nightingale Health; project previously published metabolic scores"
- [readme] Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted).: "Upload your metabolites with the same column names as in the example dataset (both CSV and TSV are accepted)."
- [readme] Check if the App could find all the necessary metabolites in your dataset.: "Check if the App could find all the necessary metabolites in your dataset."
- [intro] MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository.: "MiMIR enables projection of previously published metabolic scores, which includes MetaboAge based on the BBMRI-NL 1H-NMR Metabolomics Repository."
