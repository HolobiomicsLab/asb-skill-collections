---
name: qc-coefficient-of-variation-calculation
description: Use when after extracting NMR spectra and designating replicate QC samples (typically 10 samples run throughout the study), calculate CV for each metabolite feature to assess which signals are reproducible enough for downstream metabolite-phenotype association testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Bioconductor
  - MWASTools
  techniques:
  - NMR
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC Coefficient-of-Variation Calculation

## Summary

Compute the coefficient of variation (CV = sd/mean) for each metabolic feature across quality control (QC) samples to quantify signal reproducibility in NMR metabolomics data. This metric identifies features with poor instrumental stability and guides feature filtering before association analysis.

## When to use

After extracting NMR spectra and designating replicate QC samples (typically 10 samples run throughout the study), calculate CV for each metabolite feature to assess which signals are reproducible enough for downstream metabolite-phenotype association testing. Use this when you have a SummarizedExperiment object with assay data and need to filter out features with high instrumental drift.

## When NOT to use

- QC samples are not available or not replicated (CV requires ≥2 replicates per feature).
- Input is already a quality-filtered feature table or pre-computed CV scores.
- Data are from non-instrumental sources (e.g., already log-normalized counts) where CV has different interpretation.

## Inputs

- SummarizedExperiment assay matrix containing NMR signal intensities
- Vector of QC sample column indices or names
- Metabolite feature names (assay rownames)

## Outputs

- Named numeric vector of CV values (metabo_CV)
- Optional: filtered feature set after CV-based thresholding

## How to apply

Extract the QC sample columns from the assay matrix of the metabo_SE SummarizedExperiment object. For each metabolite feature (row), calculate the mean and standard deviation across all QC samples. Compute CV as the ratio sd/mean for each feature. Store the resulting CV values in a named numeric vector with feature names as vector names. Use this CV vector to identify and potentially filter out high-CV features (those with poor reproducibility) before proceeding to association modeling; features with CV below a pre-specified threshold (commonly 0.30 or 20–30%) are retained for analysis.

## Related tools

- **MWASTools** (R/Bioconductor package implementing QC_CV function and quality control analysis for metabolomics data) — https://github.com/AndreaRMICL/MWASTools
- **R** (Runtime environment (≥3.3) for executing QC_CV calculations)
- **Bioconductor** (Framework providing SummarizedExperiment class and associated utilities for storing and manipulating assay data)

## Examples

```
metabo_CV <- apply(assay(metabo_SE)[, qc_sample_cols], 1, function(x) sd(x) / mean(x)); metabo_CV_filtered <- metabo_CV[metabo_CV < 0.30]
```

## Evaluation signals

- metabo_CV vector length equals number of features in assay; no missing or NaN values (except for features with zero mean).
- All CV values are non-negative; CV = 0 only for features with zero variance across QC samples.
- CV values are typically in range 0–1 for well-behaved instrumental data; extreme values (CV > 2) suggest outliers or poor QC consistency.
- Features filtered by CV threshold show improved p-value distribution and reduced noise in downstream association tests (e.g., OPLS-DA or generalized linear models).
- CV calculations are reproducible when re-run on the same QC subset; metadata match between assay colnames and QC sample designations.

## Limitations

- CV is undefined or unreliable for features with mean ≈ 0 (common in sparse NMR spectra); a small pseudocount or floor threshold may be needed.
- CV does not account for systematic drift or batch effects across QC runs; supplementary quality control plots (e.g., QC signal intensity over time) are recommended.
- Threshold selection (e.g., CV < 0.30) is empirical and dataset-dependent; no universal cutoff is provided in the article.
- Small numbers of QC replicates (< 5) yield unreliable CV estimates; the workflow assumes ≥10 QC samples as in FGENTCARD study.

## Evidence

- [other] Extract the 10 QC sample columns from the metabo_SE SummarizedExperiment assay matrix. For each metabolite feature (row), calculate the mean and standard deviation across the 10 QC samples. Compute CV for each feature as sd/mean.: "Extract the 10 QC sample columns from the metabo_SE SummarizedExperiment assay matrix. For each metabolite feature (row), calculate the mean and standard deviation across the 10 QC samples. Compute"
- [other] The QC_CV function calculates the coefficient of variation (sd/mean) for each NMR signal across the QC samples, producing a metabo_CV output vector that quantifies signal reproducibility.: "The QC_CV function calculates the coefficient of variation (sd/mean) for each NMR signal across the QC samples, producing a metabo_CV output vector that quantifies signal reproducibility."
- [intro] quality control (QC) analysis; metabolite-phenotype association models: "quality control (QC) analysis; metabolite-phenotype association models"
- [abstract] MWASTools provides quality control analysis, metabolite-phenotype association models, data visualization tools, and metabolite assignment using STOCSY: "MWASTools provides quality control analysis, metabolite-phenotype association models, data visualization tools, and metabolite assignment using STOCSY"
- [intro] <sup>1</sup>H NMR plasma spectra were acquired on a Bruker Avance III 600 MHz spectrometer: "<sup>1</sup>H NMR plasma spectra were acquired on a Bruker Avance III 600 MHz spectrometer"
