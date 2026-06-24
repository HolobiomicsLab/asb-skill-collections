---
name: internal-standard-optimization-selection
description: Use when you have preprocessed metabolomics data with multiple candidate
  internal standards and QC (Quality Control) sample replicates, and you need to assign
  a single internal standard per compound that will minimize measurement variability
  across batches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
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

# internal-standard-optimization-selection

## Summary

Selects the optimal internal standard for each compound in metabolomics studies by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) across batch-corrected compound-to-internal-standard ratios, then recommending the internal standard yielding the lowest RSDQC. This minimizes analytical variability and improves quantification reliability.

## When to use

Apply this skill when you have preprocessed metabolomics data with multiple candidate internal standards and QC (Quality Control) sample replicates, and you need to assign a single internal standard per compound that will minimize measurement variability across batches. Use it after batch correction has been applied to pooled study QC samples and you have at least 3 QC replicates per batch.

## When NOT to use

- You have only one candidate internal standard per compound (no optimization possible).
- Your QC samples are not replicated across batches (insufficient statistical basis for RSD calculation).
- Internal standards have not been pre-assigned to compounds (this skill assumes a set of candidates, not de novo assignment).

## Inputs

- SummarizedExperiment object with assay slot containing raw compound areas
- assay slot containing raw internal standard areas
- colData slot with sample type annotations (QC, study sample, calibration line)
- rowData slot with compound identifiers and internal standard assignments
- batch metadata (e.g., injection order or plate identifier)

## Outputs

- Tab-delimited table with columns: compound, recommended_internal_standard, min_rsdqc
- Updated SummarizedExperiment with recommended internal standard assignments in rowData
- Numerical RSDQC values for all compound–internal-standard pairs (for inspection)

## How to apply

Load the SummarizedExperiment object containing preprocessed metabolomics data (compound measurements, internal standard areas, and sample type metadata). For each compound, extract all QC sample measurements and compute batch-corrected ratios for every candidate internal standard, accounting for batch effects using pooled QC samples. Calculate the Relative Standard Deviation (RSD) of the batch-corrected ratios for each compound–internal-standard pair. Identify the internal standard with the minimum RSDQC for each compound and compile results into a recommendation table. The rationale is that the internal standard with the lowest RSD best corrects for analytical drift and matrix effects specific to that compound, yielding the most precise quantification.

## Related tools

- **mzQuality** (Core R package that implements exhaustive RSDQC calculation and internal standard recommendation via the doAnalysis wrapper function) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor data container storing compound measurements, internal standard areas, batch metadata, and sample annotations required as input) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny application providing a graphical interface to execute internal standard selection without R programming) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp); is_recommendations <- rowData(exp)[, c('compound', 'internal_standard_recommended', 'rsdqc_recommended')]
```

## Evaluation signals

- All compounds in the output table have a recommended internal standard with a non-null RSDQC value.
- The min_rsdqc for each compound is strictly lower than the RSDQC of all other candidate internal standards for that compound (verify by cross-checking against the full candidate matrix).
- RSDQC values fall within a realistic range for batch-corrected metabolomics data (typically 5–40% for well-behaved compounds; flagged as caution/low SNR if >40%).
- The number of compounds with recommended internal standards equals the total number of unique compounds in the input assay.
- Recommended internal standards are not uniformly concentrated in a single standard (diversity check: verify that multiple internal standards are recommended across the compound set).

## Limitations

- RSDQC calculation is sensitive to the quality and coverage of QC samples; sparse or non-representative QC replicates will yield unreliable recommendations.
- The method assumes internal standard candidates have already been pre-assigned to compounds; it does not perform de novo internal standard discovery or multi-to-many matching.
- Compounds with very low abundance or high background noise may produce inflated or unstable RSDQC values; mzQuality flags these as unreliable based on thresholds for background percentage and QC presence.
- Batch correction quality depends on the representativeness of pooled study QC samples; if QC samples do not span the chemical diversity or matrix complexity of study samples, correction may be incomplete.

## Evidence

- [intro] exhaustive RSDQC calculation: "mzQuality exhaustively calculates the Relative Standard Deviation of QC samples (RSDQC) for batch-corrected ratios across candidate internal standards"
- [intro] selection logic: "then selects the internal standard yielding the lowest RSDQC for each compound as the recommended standard"
- [intro] batch correction accounting: "Compute batch-corrected compound-to-internal-standard ratios for each QC sample, accounting for batch effects"
- [intro] output format: "Compile and export results as a tab-delimited table with columns: compound, recommended_internal_standard, min_rsdqc"
- [readme] workflow automation: "The `doAnalysis` function will perform the following steps... Suggest Internal Standards based on the calculated values"
