---
name: multiclass-biomarker-quality-assessment
description: Use when you have a multi-class metabolomic peak table with quality control (QC) samples included, and you need to select an optimal preprocessing workflow for downstream biomarker discovery or differential profiling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
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

# multiclass-biomarker-quality-assessment

## Summary

Rank all preprocessing workflows for multi-class metabolomic data with quality control samples across five integrated assessment criteria to identify the best-performing method for biomarker discovery. This skill applies NOREVA's comprehensive evaluation framework to systematically compare thousands of workflow combinations and surface the optimal preprocessing pipeline.

## When to use

You have a multi-class metabolomic peak table with quality control (QC) samples included, and you need to select an optimal preprocessing workflow for downstream biomarker discovery or differential profiling. Use this skill when you want to evaluate all available preprocessing workflows (normalization, imputation, transformation, and scaling combinations) rather than committing to a single method a priori.

## When NOT to use

- Input data lacks quality control samples (use normulticlassnoall instead)
- Data is time-course rather than multi-class (use nortimecourseqcall or nortimecoursenoall)
- Input includes internal standards but no QC samples (use normulticlassisall instead)

## Inputs

- peak table (standardized format or software-generated format)
- label file for multi-class sample grouping
- quality control (QC) sample intensities embedded in peak table

## Outputs

- OUTPUT-NOREVA-Overall.Ranking.Data.csv (workflow rankings with scores across all assessment criteria)
- assessment scores for each workflow across five integrated evaluation criteria
- comparative performance metrics by assessment dimension

## How to apply

First, prepare your input files using PrepareInuputFiles() with dataformat='1' (standardized NOREVA format) or '2' (software-generated format). Then execute normulticlassqcall(fileName, SAalpha='Y'/'N', SAbeta='Y'/'N', SAgamma='Y'/'N'), specifying which study assumptions your data satisfies: alpha (all metabolites equally important), beta (metabolite abundance constant across samples), and gamma (majority of metabolite intensities unchanged under studied conditions). The function applies five well-established criteria, each with distinct underlying theory, to rank all workflows. The output file OUTPUT-NOREVA-Overall.Ranking.Data.csv ranks workflows by their performance across four primary assessment dimensions. Validate by confirming the ranking table contains all workflows with numerical scores and comparative rankings.

## Related tools

- **NOREVA** (executes multi-class QC-sample workflow assessment and ranking via normulticlassqcall function) — https://github.com/idrblab/NOREVA
- **R** (runtime environment (version >3.5 required)) — https://www.r-project.org/
- **BiocManager** (dependency manager for Bioconductor packages (Biobase, pcaMethods, multtest, limma, impute, statTarget, ProteoMM))
- **statTarget** (provides batch effect and QC correction preprocessing methods evaluated within NOREVA workflows)
- **limma** (provides differential expression assessment criterion for workflow ranking)
- **pcaMethods** (provides PCA-based assessment and dimensionality reduction for workflow evaluation)

## Examples

```
library(NOREVA); normulticlassqcall(fileName="Multiclass_with_QCS", SAalpha="Y", SAbeta="Y", SAgamma="Y")
```

## Evaluation signals

- OUTPUT-NOREVA-Overall.Ranking.Data.csv is generated and contains all preprocessing workflow combinations
- Ranking table includes numerical scores for each workflow across all five assessment criteria
- Each workflow has a comparative rank assignment (e.g., rank 1–N) indicating relative performance
- No missing values in critical ranking columns; all workflows evaluated consistently
- Study assumptions (alpha, beta, gamma) specified in function call are reflected in output metadata or filtering logic

## Limitations

- Function requires multi-class study design with explicit QC samples; cannot be applied to single-class data or datasets lacking QC samples
- Five integrated criteria assume distinct underlying theories that may not align with all research goals (e.g., biomarker discovery vs. metabolic pathway stability)
- Ranking output does not prescriptively select one 'best' workflow; practitioner judgment required to choose among top-ranked candidates based on downstream analysis needs
- Computational time scales with number of workflows evaluated; large-scale searches may require parallel computing and memory management features available in NOREVA ≥2.1.1

## Evidence

- [other] Execute normulticlassqcall function: "Execute normulticlassqcall function to process the multiclass data with quality control samples."
- [other] Five integrated assessment criteria: "Apply the five integrated assessment criteria (each with distinct underlying theory) to evaluate all preprocessing workflows."
- [other] Overall ranking output: "Generate OUTPUT-NOREVA-Overall.Ranking.Data.csv ranking all workflows by their performance across the four primary assessment dimensions."
- [readme] Function purpose for multi-class QC data: "This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan"
- [readme] Five well-established criteria integration: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion."
- [readme] Provides biomarker discovery guidelines: "This study provides guidelines for researchers who will engage in biomarker discovery or other differential profiling "omics" studies with respect selecting the most appropriate preprocessing method"
- [readme] Study assumption alpha definition: "Study assumption alpha represents that all metabolites are assumed to be equally important."
