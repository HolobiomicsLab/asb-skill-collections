---
name: quality-control-sample-integration-in-normalization
description: Use when your multi-class metabolomic peak table includes quality control samples (technical replicates) but no internal standards, and you need to compare the performance of multiple preprocessing workflows (normalization, imputation, transformation methods) to select the optimal pipeline for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NOREVA
  - devtools
  - BiocManager
  - pcaMethods
  - multtest
  - limma
  - impute
  - statTarget
  - ProteoMM
  - BiocManager / Biobase / pcaMethods / limma / impute / statTarget / ProteoMM
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- devtools::install_github("idrblab/NOREVA")
- '![installed with devtools](https://img.shields.io/badge/installed%20with-devtools-blueviolet.svg)'
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
- BiocManager::install("pcaMethods")
- BiocManager::install("multtest")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
---

# quality-control-sample-integration-in-normalization

## Summary

Integrate quality control (QC) samples into metabolomic data normalization workflows to assess and rank preprocessing methods across multiple performance criteria. This skill enables systematic evaluation of which preprocessing workflows best preserve data integrity and biological signal in multi-class metabolomic datasets.

## When to use

Your multi-class metabolomic peak table includes quality control samples (technical replicates) but no internal standards, and you need to compare the performance of multiple preprocessing workflows (normalization, imputation, transformation methods) to select the optimal pipeline for biomarker discovery or differential profiling.

## When NOT to use

- Input dataset lacks quality control samples—use normulticlassnoall() instead for multi-class data without QC samples
- Dataset includes internal standards but no QC samples—use normulticlassisall() for internal-standard normalization assessment
- Data is time-course rather than multi-class—use nortimecourseqcall() for temporal metabolomic studies with QC samples

## Inputs

- Peak intensity matrix (samples × metabolites) in standardized NOREVA format or compatible software format (12 supported tools)
- Class label file indicating sample group membership (multi-class)
- QC sample identifiers (technical replicates mixed into the peak table)

## Outputs

- OUTPUT-NOREVA-Overall.Ranking.Data.csv (ranked preprocessing workflows with performance scores across four primary assessment dimensions)
- Per-workflow performance metrics quantifying QC reproducibility and biological signal preservation
- Comparative rankings enabling objective selection of optimal preprocessing method

## How to apply

First, prepare your peak table and QC sample labels using PrepareInuputFiles() with the appropriate data format specification. Then execute normulticlassqcall() on the prepared dataset, specifying study assumptions (SAalpha, SAbeta, SAgamma) that reflect whether all metabolites are equally important, whether metabolite abundance is constant across samples, and whether most metabolite intensities are unchanged under study conditions. The function systematically applies five integrated assessment criteria—each with distinct underlying theory—to evaluate all available preprocessing workflows. The function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv that ranks workflows by composite performance across assessment dimensions, allowing you to identify which preprocessing pipeline minimizes QC sample variance while preserving biological signals for your specific dataset characteristics.

## Related tools

- **NOREVA** (Core package providing normulticlassqcall() function for QC-integrated multi-class workflow ranking and five integrated assessment criteria) — https://github.com/idrblab/NOREVA
- **R** (Runtime environment (≥3.5) for NOREVA package execution) — https://www.r-project.org/
- **BiocManager / Biobase / pcaMethods / limma / impute / statTarget / ProteoMM** (Bioconductor dependencies providing normalization, dimensionality reduction, statistical testing, and imputation methods embedded in NOREVA workflows) — https://bioconductor.org
- **devtools** (Installation utility for NOREVA package from GitHub repository) — https://github.com/r-lib/devtools

## Examples

```
library(NOREVA); normulticlassqcall(fileName='prepared_multiclass_qc_data', SAalpha='Y', SAbeta='Y', SAgamma='Y')
```

## Evaluation signals

- OUTPUT-NOREVA-Overall.Ranking.Data.csv file is generated and contains all preprocessing workflows with non-null performance scores
- Ranking table includes scores for each of the four primary assessment dimensions; all workflows have comparable dimensional coverage
- QC sample reproducibility metrics (e.g., intra-QC variance or relative standard deviation) show expected low values for top-ranked workflows
- Biological signal preservation metrics (e.g., separation between multi-class groups in PCA or OPLS-DA) are not artificially inflated by QC bias
- Top-ranked workflows exhibit lower QC sample variance compared to low-ranked workflows, validating that ranking reflects QC reproducibility

## Limitations

- normulticlassqcall() applies five criteria simultaneously; individual criterion weighting is not user-configurable, which may not suit study-specific priorities
- Study assumptions (SAalpha, SAbeta, SAgamma) are binary (Y/N) and must be pre-specified; misspecification could lead to suboptimal or misleading workflow rankings
- Function scans all available preprocessing workflows; computational cost and memory requirements scale with dataset size and number of workflows evaluated
- Quality control samples must be true technical replicates; the method does not distinguish between instrumental drift and biological variation if QC samples are not independent runs
- Output ranking is based on integrated criteria; individual metabolites with poor QC reproducibility are not flagged separately for removal or investigation

## Evidence

- [other] The normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality control samples.: "normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality"
- [intro] Five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion.: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation"
- [readme] This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan thousands of processing workflows and rank them based on their performances.: "performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan thousands of processing"
- [other] Execute normulticlassqcall function to process the multiclass data with quality control samples. Apply the five integrated assessment criteria (each with distinct underlying theory) to evaluate all preprocessing workflows.: "Execute normulticlassqcall function to process the multiclass data with quality control samples. Apply the five integrated assessment criteria to evaluate all preprocessing workflows"
- [intro] NOREVA provides guidelines for researchers who will engage in biomarker discovery or other differential profiling 'omics' studies with respect selecting the most appropriate preprocessing method: "guidelines for researchers who will engage in biomarker discovery or other differential profiling 'omics' studies with respect selecting the most appropriate preprocessing method"
