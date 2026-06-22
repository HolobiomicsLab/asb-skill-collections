---
name: internal-standard-selection-optimization
description: Use when after batch correction of metabolomics QC samples using pooled study quality control (SQC) samples, when you have multiple candidate internal standards and need to determine which one stabilizes the compound/internal standard ratio for each compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality is a user-friendly R package
- mzQuality requires a specific format for the input data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# internal-standard-selection-optimization

## Summary

Identify the optimal internal standard for each compound by exhaustively calculating Relative Standard Deviation of QC samples (RSDQC) across all internal standard candidates on batch-corrected metabolomics data. This skill selects the internal standard that minimizes measurement variance, improving data quality and downstream quantification reliability.

## When to use

After batch correction of metabolomics QC samples using pooled study quality control (SQC) samples, when you have multiple candidate internal standards and need to determine which one best stabilizes the compound/internal standard ratio for each compound. Apply this skill before final compound filtering and reporting to ensure each compound uses the internal standard that produces the lowest technical variance in QC samples.

## When NOT to use

- Input data has not undergone batch correction; RSDQC values on uncorrected ratios do not reflect the true benefit of internal standard selection.
- No QC samples are available; RSDQC calculation requires replicate QC measurements to estimate variance.
- Only one internal standard candidate is available; exhaustive comparison requires ≥2 candidates to identify the best choice.

## Inputs

- SummarizedExperiment object with batch-corrected assay (e.g., 'ratio_corrected') containing QC sample compound/internal standard ratios
- metadata specifying QC sample identifiers and batch assignments
- vector of internal standard candidate names

## Outputs

- matrix of RSDQC values (compounds × internal standards)
- recommendation table with columns: compound name, recommended internal standard, minimum RSDQC value
- tab-delimited or Excel export of recommendations

## How to apply

Load the batch-corrected SummarizedExperiment object containing QC sample ratios (compound divided by each internal standard candidate) and their batch-correction metadata. For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD = 100 × standard deviation / mean) of the batch-corrected QC sample ratios for that compound–internal standard pair. Tabulate all RSDQC values in a matrix with compounds as rows and internal standards as columns. For each compound row, identify the internal standard column with the minimum RSDQC value. Construct a recommendation table listing each compound, its recommended internal standard, and the corresponding minimum RSDQC. Export this table for downstream use in concentration calculations and compound filtering.

## Related tools

- **mzQuality** (Performs batch correction, calculates RSDQC across internal standard candidates, and tabulates internal standard recommendations via the doAnalysis wrapper function) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor object class used to store batch-corrected assays, compound metadata (rowData), and sample metadata (colData) required for RSDQC calculation) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny application providing visual inspection and tabular export of internal standard recommendations without requiring R programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **R** (Computing environment for iterating over internal standard candidates, computing RSD statistics, and exporting recommendation tables)

## Examples

```
exp <- doAnalysis(exp = exp); recommendations <- rowData(exp)[, c('compound', 'recommended_IS', 'RSDQC_min')]
```

## Evaluation signals

- RSDQC matrix is complete (no NA values) with one column per internal standard candidate and one row per compound
- For each compound, the recommended internal standard has the strictly minimum RSDQC value across all candidates for that compound
- Recommendation table has exactly one internal standard per compound with a corresponding positive RSDQC numeric value
- RSDQC values are within expected ranges for metabolomics QC data (typically 5–50% for well-behaved compounds); outliers > 50% flag problematic compounds or internal standards
- When exported and compared to prior recommendations or literature values, the selected internal standards are chemically plausible (e.g., not a metabolite of the target compound or a compound with known stability issues)

## Limitations

- In the current version of mzQuality, only one sample type (e.g., plasma or urine) can be used for calculating concentrations; internal standard recommendations are sample-type-specific and cannot be pooled across sample types.
- RSDQC calculation assumes batch correction has already been performed; if batch correction is poor or the SQC pool is non-representative, RSDQC values may not reflect true biological or technical variance.
- The skill selects the internal standard with minimum RSDQC for each compound independently; it does not account for trade-offs where a single internal standard might be 'good enough' (RSDQC within 5% of the global minimum) for multiple compounds, which could reduce assay complexity.

## Evidence

- [other] mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound and identifies the internal standard yielding the lowest RSDQC as the recommended choice.: "mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound and identifies the internal standard yielding the lowest RSDQC as"
- [intro] mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's.: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's."
- [other] For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD) of the batch-corrected QC sample ratios.: "For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD) of the batch-corrected QC sample ratios."
- [readme] batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds: "batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds"
- [intro] Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data.: "Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data."
- [other] Note that in the current version of mzQuality, only one sample type can be used for calculating concentrations.: "Note that in the current version of mzQuality, only one sample type can be used for calculating concentrations."
