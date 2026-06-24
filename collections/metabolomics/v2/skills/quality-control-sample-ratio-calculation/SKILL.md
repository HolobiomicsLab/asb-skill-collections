---
name: quality-control-sample-ratio-calculation
description: Use when you have preprocessed metabolomics data stored in a SummarizedExperiment
  object containing QC sample measurements, assigned internal standards for compounds,
  and evidence of batch effects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  - xcms
  license_tier: open
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-sample-ratio-calculation

## Summary

Calculate Relative Standard Deviation (RSD) of batch-corrected compound-to-internal-standard ratios in QC samples to identify and remove outlier QC measurements and to guide internal standard selection. This skill is essential for detecting systematic quality issues and recommending the most stable internal standard for each compound in metabolomics studies.

## When to use

Apply this skill when you have preprocessed metabolomics data stored in a SummarizedExperiment object containing QC sample measurements, assigned internal standards for compounds, and evidence of batch effects. Use it to flag unreliable QC samples (high outlier ratios) before downstream analysis and to systematically identify which internal standard minimizes measurement variability for each compound.

## When NOT to use

- Input data lacks QC samples or internal standards are not assigned — the method requires replicate QC measurements and a reference compound for ratio calculation.
- Metabolomics data has not been preprocessed (feature detection, alignment, peak integration) — mzQuality requires input from xcms or equivalent preprocessing pipelines.
- Study design lacks pooled QC samples for batch correction — batch-corrected ratios cannot be computed without a reference matrix effect baseline.

## Inputs

- SummarizedExperiment object with preprocessed metabolomics assay data (peak areas or intensities)
- Compound annotations with assigned internal standards
- QC sample identifiers and batch labels
- Internal standard peak area measurements for QC samples

## Outputs

- Tab-delimited table: compound, recommended_internal_standard, min_rsdqc, outlier_qc_samples
- Updated SummarizedExperiment with batch-corrected ratio assay and outlier flags in colData
- SummarizedExperiment subset excluding flagged outlier QC samples

## How to apply

Load the preprocessed SummarizedExperiment from mzQuality. For each compound, extract all QC sample measurements and their corresponding internal standard peak areas. Calculate batch-corrected compound-to-internal-standard ratios for each QC replicate, accounting for batch effects using pooled study quality control (SQC) samples as reference. Compute the Relative Standard Deviation (RSD) of these batch-corrected ratios for each compound–internal-standard pair. Identify QC samples with outlier ratios using the Rosner Test for statistical outliers, and flag these for removal. For internal standard recommendation, select the internal standard yielding the minimum RSDQC for each compound. Export results as a tab-delimited table with columns: compound, recommended_internal_standard, min_rsdqc, and outlier_flags.

## Related tools

- **mzQuality** (R package that implements batch-corrected ratio calculation, RSD computation, outlier detection via Rosner Test, and internal standard recommendation) — https://github.com/hankemeierlab/mzQuality
- **mzQualityDashboard** (Interactive Shiny application providing user-friendly interface to run mzQuality workflows without programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **SummarizedExperiment** (Bioconductor object class used to store preprocessed data, batch-corrected assays, and sample/compound metadata) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **xcms** (Upstream R-based metabolomics preprocessing pipeline for feature detection and alignment; output can be converted to SummarizedExperiment input for mzQuality)

## Examples

```
exp <- doAnalysis(exp = exp); suggested_is <- rowData(exp)[, c('compound', 'recommended_internal_standard', 'rsdqc')]; outlier_qc <- exp[, !exp$use]
```

## Evaluation signals

- Outlier QC samples identified by Rosner Test show batch-corrected ratio values >2–3 standard deviations from the median; removal should reduce overall RSDQC by >10%.
- For each compound, the minimum RSDQC value is significantly lower than the median or mean RSDQC across all candidate internal standards (typical cutoff RSDQC < 30% for 'high confidence').
- SummarizedExperiment's colData contains a 'use' column with TRUE/FALSE flags; removed outlier QC samples have FALSE; remaining QC samples have TRUE and consistent batch-corrected ratio distributions.
- Internal standard recommendation table contains no duplicate compounds; each compound maps to exactly one recommended internal standard with the lowest RSDQC.
- Batch-corrected ratio assay shows reduced batch effects relative to uncorrected ratios when visualized as PCA plot grouped by batch; batch separation should be minimal.

## Limitations

- Method assumes QC samples are representative of the matrix and that batch effects are primarily driven by SQC variation; if matrix composition differs substantially between sample groups, batch correction may be ineffective.
- Rosner Test for outlier detection is sensitive to the choice of significance level; conservative settings may retain subtle batch drifts, while aggressive settings may remove valid biological replicates.
- If an internal standard is absent or unreliably measured in some QC samples, the corresponding RSDQC will be artificially inflated; missing or low-quality internal standard measurements should be filtered before analysis.
- Recommendation of a single 'best' internal standard per compound assumes linearity and stability of ionization response; compounds with non-linear response across concentration ranges or those affected by ion suppression may not benefit from this approach.

## Evidence

- [other] For each compound, extract all QC sample measurements and their corresponding internal standard areas. Compute batch-corrected compound-to-internal-standard ratios for each QC sample, accounting for batch effects.: "For each compound, extract all QC sample measurements and their corresponding internal standard areas. Compute batch-corrected compound-to-internal-standard ratios for each QC sample, accounting for"
- [intro] The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio"
- [intro] mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's"
- [other] Calculate the Relative Standard Deviation (RSD) of the batch-corrected ratios for each compound–internal-standard pair. Identify the internal standard with the minimum RSDQC for each compound.: "Calculate the Relative Standard Deviation (RSD) of the batch-corrected ratios for each compound–internal-standard pair. Identify the internal standard with the minimum RSDQC for each compound."
- [readme] Perform batch correction using the pooled study quality control samples (SQC): "Perform batch correction using the pooled study quality control samples (SQC)"
