---
name: relative-standard-deviation-computation
description: Use when when you have preprocessed metabolomics data with pooled QC
  samples and assigned internal standards, and need to select the optimal internal
  standard for each compound by comparing ratio stability across candidate standards.
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
  license_tier: open
  provenance_tier: literature
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

# relative-standard-deviation-computation

## Summary

Compute the Relative Standard Deviation (RSD) of batch-corrected compound-to-internal-standard ratios across QC samples to quantify measurement reproducibility and identify the most stable internal standard for each metabolite.

## When to use

When you have preprocessed metabolomics data with pooled QC samples and assigned internal standards, and need to select the optimal internal standard for each compound by comparing ratio stability across candidate standards. This is critical after batch correction but before final compound reporting, especially when multiple internal standard options exist for a single metabolite.

## When NOT to use

- Input lacks QC samples or batch metadata — RSD computation requires replication across conditions to estimate variance.
- Batch correction has not been performed — RSDQC must be computed on batch-corrected, not raw, ratios to reflect true analytical stability.
- Only a single internal standard is available per compound — exhaustive comparison across candidates is the core mechanism.

## Inputs

- SummarizedExperiment object containing preprocessed metabolomics data with compound and internal standard areas
- QC sample subset with batch assignment metadata
- Batch effect matrix or correction factors from pooled study QC (SQC) samples
- Candidate internal standard assignments per compound

## Outputs

- Tab-delimited results table with columns: compound, recommended_internal_standard, min_rsdqc
- Updated SummarizedExperiment rowData with recommended internal standard and RSDQC values for each compound
- Batch-corrected ratio assay for downstream analysis

## How to apply

For each compound–internal standard pair, extract all QC sample measurements and their corresponding internal standard areas from a SummarizedExperiment object. Compute batch-corrected compound-to-internal-standard ratios for each QC sample, accounting for batch effects using pooled study QC (SQC) samples as reference. Calculate the Relative Standard Deviation of these batch-corrected ratios as RSD = (standard deviation / mean) × 100%. Repeat for all candidate internal standards. Select the internal standard yielding the minimum RSDQC for each compound. The rationale is that lower RSD indicates more consistent normalization and better correction of analytical variation, making it the most reliable standard for that metabolite.

## Related tools

- **mzQuality** (Primary R package that implements RSDQC calculation and internal standard recommendation via exhaustive comparison of batch-corrected ratio variability) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container object that stores compound assays, internal standard areas, QC sample metadata, and batch assignments required for RSDQC workflow)
- **R** (Programming environment for executing RSDQC calculations, batch correction, and statistical analysis)

## Examples

```
exp <- doAnalysis(exp = exp); results <- data.frame(compound = rownames(exp), recommended_internal_standard = rowData(exp)$recommended_is, min_rsdqc = rowData(exp)$rsdqc_min)
```

## Evaluation signals

- RSDQC values are non-negative percentages; verify all values fall in valid range [0, ∞) and are unitless or explicitly labeled as %.
- Each compound has exactly one recommended internal standard; verify no compounds lack a selection and no duplicates exist.
- Recommended internal standard always corresponds to the minimum RSDQC among all candidates for that compound; spot-check 5–10 compounds by sorting candidate RSDQC values.
- Batch-corrected ratio distributions are tighter (lower variance) than raw ratios; compare raw and corrected ratio standard deviations to confirm batch effect removal.
- Results table is properly formatted with no missing values in compound, recommended_internal_standard, and min_rsdqc columns; validate schema via data type and completeness checks.

## Limitations

- RSDQC assumes QC samples are homogeneous and representative of true analytical variability; if QC samples contain outliers or systematic drift, RSD estimates will be inflated and recommendations unreliable.
- Batch correction accuracy depends on sufficient SQC replication per batch; sparse batches or missing SQC samples in some batches will compromise ratio correction and RSDQC validity.
- Selection of the minimum RSDQC is greedy and does not account for co-correlation or cross-talk between internal standards; a compound may benefit from a non-minimum but more orthogonal standard in complex matrices.
- RSDQC does not capture other internal standard properties (e.g., retention time stability, isotopic purity, cost); final selection should be validated in downstream assays.

## Evidence

- [other] Exhaustive RSDQC calculation and internal standard selection: "mzQuality exhaustively calculates the Relative Standard Deviation of QC samples (RSDQC) for batch-corrected ratios across candidate internal standards, then selects the internal standard yielding the"
- [other] Batch-corrected ratio computation workflow: "Compute batch-corrected compound-to-internal-standard ratios for each QC sample, accounting for batch effects."
- [intro] Internal standard recommendation capability in mzQuality: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's"
- [intro] SummarizedExperiment as core data container: "Internally, mzQuality uses Bioconductors' SummarizedExperiment object to store the data"
- [intro] QC-based outlier detection and batch correction rationale: "mzQuality was developed to perform outlier detection, batch correction and other quality control steps without the need for defined phenotypes"
