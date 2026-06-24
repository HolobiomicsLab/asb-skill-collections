---
name: qc-sample-variability-assessment
description: Use when after batch correction of a metabolomics dataset using pooled
  study quality control (SQC) samples, when you have multiple candidate internal standards
  and need to systematically evaluate which one produces the most stable compound
  quantification (lowest QC variability) for each compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# qc-sample-variability-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Exhaustively calculate Relative Standard Deviation (RSDQC) of batch-corrected compound/internal-standard ratios across all internal standard candidates to identify which internal standard minimizes QC sample variability for each compound. This identifies the most reliable internal standard choice for normalizing each metabolite.

## When to use

After batch correction of a metabolomics dataset using pooled study quality control (SQC) samples, when you have multiple candidate internal standards and need to systematically evaluate which one produces the most stable compound quantification (lowest QC variability) for each compound. This is especially critical when the assignment of internal standards to compounds is not predetermined or when you wish to validate current assignments.

## When NOT to use

- Your internal standards are already assigned by design and you do not need to validate or optimize them.
- You have only one internal standard candidate per compound—RSDQC assessment requires multiple IS options to compare.
- QC samples are absent, too few (n < 3–4), or not representative of study batch structure, making RSD calculation unreliable.

## Inputs

- SummarizedExperiment object with batch-corrected ratio assays (compound / internal standard)
- QC sample metadata (sample type annotations)
- Internal standard candidate list for each compound

## Outputs

- RSDQC matrix (compounds × internal standards)
- Internal standard recommendation table (compound, recommended IS, min RSDQC)
- Filtered or ranked compound list based on RSDQC thresholds

## How to apply

Load the batch-corrected SummarizedExperiment object containing QC sample assays with compound/internal-standard ratios and their batch-correction metadata. For each compound, iterate over all candidate internal standards and calculate the relative standard deviation (RSD) of the batch-corrected QC sample ratios for that compound-IS pair. Tabulate RSDQC values in a matrix with compounds as rows and internal standards as columns. For each row (compound), identify the column (internal standard) with the minimum RSDQC value—this is the recommended internal standard for that compound. The recommendation is grounded in the principle that lower variability in QC samples indicates better instrumental stability and more reliable quantification across the analytical batch. Construct and export a recommendation table listing each compound, its recommended internal standard, and the corresponding minimum RSDQC value for downstream reporting and threshold filtering.

## Related tools

- **mzQuality** (Computes RSDQC values across all internal standard candidates, identifies minimum RSDQC for each compound, and generates recommendation tables) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Data structure to store batch-corrected compound/IS ratios, QC sample assays, and batch-correction metadata)
- **mzQualityDashboard** (Interactive Shiny interface for viewing and exporting RSDQC metrics and IS recommendations without coding) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp); recommendations <- getInternalStandardRecommendations(exp)
```

## Evaluation signals

- RSDQC matrix is complete (no NAs except where data is genuinely missing) and has expected dimensions (n compounds × m internal standards).
- Recommended internal standard for each compound has the lowest RSDQC value in its row; no row contains a lower RSDQC for a different IS.
- Recommendation table is exportable as a tab-delimited or Excel file with columns: compound name, recommended IS, RSDQC value; matches the structure described in the workflow.
- Compounds with RSDQC above user-defined threshold (e.g., >20–30%) are correctly flagged for manual review or exclusion in downstream reporting.
- When compared against pre-existing IS assignments, newly recommended IS entries show either confirmation of current practice or justified deviations (typically accompanied by lower RSDQC).

## Limitations

- mzQuality currently supports only one sample type for calculating concentrations; if multiple study populations or sample types need separate IS optimization, analyses must be run separately.
- RSDQC calculation depends on QC sample size and representativeness; sparse QC sampling or QC samples not spanning the full analytical batch may yield misleading IS rankings.
- The method does not account for matrix effects or ion suppression beyond what is captured in the batch-corrected ratios; compounds with severe matrix interference may still show low RSDQC despite poor absolute quantification.
- Recommendation is purely statistical (lowest RSD); it does not consider practical constraints such as IS cost, availability, or chemical similarity to compound classes.

## Evidence

- [other] mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound and identifies the internal standard yielding the lowest RSDQC as the recommended choice.: "mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound and identifies the internal standard yielding the lowest RSDQC as"
- [other] For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD) of the batch-corrected QC sample ratios.: "For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD) of the batch-corrected QC sample ratios."
- [other] Tabulate RSDQC values in a matrix with compounds as rows and internal standards as columns.: "Tabulate RSDQC values in a matrix with compounds as rows and internal standards as columns."
- [intro] mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's.: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's."
- [readme] batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds, various plots for inspecting, and generating reports for further processing.: "batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds, various plots for inspecting, and generating reports for further processing."
